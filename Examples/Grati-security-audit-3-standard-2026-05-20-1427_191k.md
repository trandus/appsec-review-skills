# Repository Context

Grati to POC aplikacji ASP.NET Core MVC (.NET 10) z Microsoft Entra External ID, cookie session, Dapper/MS SQL, publicznym anonymous recognition flow, prywatnym panelem profilu, uploadem avatarow do Azure Blob Storage oraz logowaniem Console + Seq. Granice zaufania: anonimowe slug/profile/recognition routes, zalogowane operacje profilu i moderation/hide, publiczny Blob Storage, SQL persistence, endpointy health/doctor, Azure App Service/IaC oraz zewnetrzny Seq.

# Executive Summary

Najistotniejsze ryzyka to brak kontroli wlasciciela przy ukrywaniu rozpoznan, usuwanie blobow na podstawie edytowalnego URL profilu, anonimowy `/internal/doctor`, oraz produkcyjno-devowe logowanie danych profilu/recognition do Seq po `http://` z wlaczonym obejściem walidacji certyfikatow. Nie uruchamialem skanerow ani testow runtime; review opiera sie na lokalnym kodzie i konfiguracji.

# Summary

| Type | Count |
|---|---:|
| Findings | 5 |
| Candidate Findings | 1 |
| Observations | 1 |
| Follow-up | 4 |

# Final Findings Overview

| Type | ID | Severity / Candidate Severity | Area | Decision |
|---|---|---|---|---|
| Finding | F-01 | high | Authorization / object ownership | fix |
| Finding | F-02 | medium | Blob ownership / profile photo lifecycle | fix |
| Finding | F-03 | medium | Diagnostics exposure | fix |
| Finding | F-04 | high | Logging transport / sensitive data | fix |
| Finding | F-05 | medium | Unsafe outbound redirect | fix |
| Candidate Finding | C-01 | medium | Key Vault recovery posture | validate |
| Observation | O-01 | low | Tip destination visibility contract | observe |
| Follow-up | FU-01 | n/a | Runtime route exposure | follow-up |
| Follow-up | FU-02 | n/a | Seq access controls | follow-up |
| Follow-up | FU-03 | n/a | Rate limiting behind proxy | follow-up |
| Follow-up | FU-04 | n/a | Dependency advisories | follow-up |

# Findings

## F-01 - Zalogowany uzytkownik moze ukryc cudze rozpoznanie po GUID

Type: Finding  
Severity: high  
Location: `Grati.Web/Controllers/ProfileController.cs:601`, `Grati.Web/Controllers/ProfileController.cs:606`, `Grati.Web/Grains/RecognitionGrainAdapter.cs:42`, `Grati.Sql.Repository/Recognition/SqlRecognitionRepository.cs:15`, `Grati.Web/Services/Profile/ProfileViewService.cs:137`

Evidence: `POST /me/recognitions/{id}/hide` pobiera `id` z trasy i tworzy `IRecognition` bez sprawdzenia, czy `Recognition.RecipientUserId` nalezy do aktualnego `UserId`. Adapter laduje rekord po samym `RecognitionIdentity` i wykonuje `recognition.Hide(hiddenAt)`. Prywatny feed filtruje po aktualnym uzytkowniku przy wyswietlaniu, ale mutacja hide nie powtarza tego warunku.

Exploit/Risk Path: zalogowany uzytkownik zdobywa lub odgaduje GUID rozpoznania innego pracownika z logow, testowych danych, eksportu, bledu lub innego kanalu. Wysyla `POST /me/recognitions/{victimRecognitionId}/hide` z poprawnym CSRF i timezone. Serwer ukrywa cudze rozpoznanie, mimo ze atakujacy nie jest jego recipientem.

Impact: nieautoryzowana moderacja cudzych danych, usuniecie pozytywnego wpisu z publicznego profilu ofiary, naruszenie integralnosci feedu i zaufania do workflow.

Remediation Requirement: przy mutacji rozpoznania wymagaj server-side ownership check: przed `Hide` zaladuj recognition i porownaj `RecipientUserId` z `currentUserAccessor.RequireCurrentUserId`, albo wystaw metode repozytorium/command `HideForRecipient(recognitionId, recipientUserId, ...)`, ktora aktualizuje tylko rekord pasujacy do obu identyfikatorow.

Regression Test: test kontrolera lub integration test: uzytkownik A probuje ukryc recognition nalezace do uzytkownika B i dostaje `Forbid`/`NotFound`, a `IsHidden` pozostaje `false`.

## F-02 - Edytowalny `PhotoUrl` pozwala usuwac cudze avatary z publicznego kontenera

Type: Finding  
Severity: medium  
Location: `Grati.Web/Views/Profile/Edit.cshtml:27`, `Grati.Web/Models/Profile/EditProfileForm.cs:26`, `Grati.Web/Controllers/ProfileController.cs:291`, `Grati.Users/User/UserValidators.cs:42`, `Grati.Web/Controllers/ProfileController.cs:527`, `Grati.Web/Services/Profile/Photo/AzureBlobProfilePhotoStorage.cs:45`, `Grati.Web/Services/Profile/Photo/AzureBlobProfilePhotoStorage.cs:65`, `Infrastructure/Grati.Infrastructure.Azure/Resources/ProfilePhotoStorage.cs:21`

Evidence: formularz edycji ma hidden `Form.PhotoUrl`, model akceptuje dowolny URL, a domenowy validator wymaga tylko absolutnego URI. `Edit` zapisuje ten URL jako zdjecie profilu. `RemovePhoto` pozniej usuwa blob przez `DeleteAvatarByPublicUrl`, ktory sprawdza tylko scheme/server/container path, nie prefix `avatars/{currentUserId}`. IaC i runtime tworza publiczny kontener blob (`AllowBlobPublicAccess=true`, `PublicAccess=Blob`, `PublicAccessType.Blob`).

Exploit/Risk Path: uzytkownik A kopiuje publiczny URL avatara uzytkownika B, podstawia go do ukrytego `Form.PhotoUrl` w swoim `POST /me/edit`, a nastepnie wywoluje `POST /me/photo/remove`. Storage rozpoznaje URL jako nalezacy do kontenera i wykonuje `DeleteIfExistsAsync` na blobie ofiary.

Impact: nieautoryzowane kasowanie cudzych avatarow, zepsute publiczne profile i utrata user-owned blob data. Ryzyko jest ograniczone do blobow w tym kontenerze.

Remediation Requirement: nie ufaj `PhotoUrl` z formularza jako dowodowi wlasnosci. Zapisuj w domenie/storage wlasny `BlobPath` lub sprawdzaj, ze usuwany blob ma prefix `avatars/{currentUserId:N}/`. Najlepiej usuwaj stare avatary przez `DeleteAvatarsForUser(userId)` albo przez storage-owned identifier zwrocony z uploadu.

Regression Test: test, w ktorym profil A ma `PhotoUrl` wskazujacy `avatars/{B}/...`; `RemovePhoto` nie moze wywolac delete dla prefixu B i powinien usunac tylko referencje profilu A albo zwrocic blad walidacji.

## F-03 - Anonimowy `/internal/doctor` ujawnia szczegoly zaleznosci i wymusza probe backendow

Type: Finding  
Severity: medium  
Location: `Grati.Web/Controllers/InternalDoctorController.cs:9`, `Grati.Web/Controllers/InternalDoctorController.cs:23`, `Grati.Web/Diagnostics/DoctorService.cs:14`, `Grati.Web/Diagnostics/SqlConnectivityDoctorCheck.cs:22`, `Grati.Web/Diagnostics/BlobStorageDoctorCheck.cs:29`, `Grati.Web/Diagnostics/EntraConfigurationDoctorCheck.cs:25`, `Grati.Web.IntegrationTests/HealthAndDoctorTests.cs:83`

Evidence: kontroler `internal/doctor` ma `[AllowAnonymous]` i zwraca pelny `doctorService.RunAsync`. Service uruchamia checki SQL, Blob, Entra i czasu. Metadane obejmuja fingerprint/dlugosc sekretow, status connection stringa, service URI blob storage i szczegoly konfiguracji. Test integracyjny potwierdza, ze endpoint jest tymczasowo anonimowy i zwraca 200.

Exploit/Risk Path: anonimowy atakujacy odpytuje `/internal/doctor`, poznaje stan zaleznosci, nazwy uslug/URI, obecnosc sekretow i problemy integracji. Moze tez wielokrotnie wywolywac checki wymagajace polaczen SQL/Blob, wspierajac rekonesans i lekki resource abuse.

Impact: ulatwiony rekonesans, przeciek metadanych operacyjnych i niepotrzebna publiczna powierzchnia diagnostyczna. Sekrety sa maskowane, ale sama obecnosc, dlugosc i fingerprint sa informacjami administracyjnymi.

Remediation Requirement: chron `internal/doctor` autoryzacja administracyjna, ograniczeniem sieciowym albo warunkiem `Development`. Publiczne `/health/live` i `/health/ready` powinny zostac syntetyczne i minimalne.

Regression Test: integration test dla non-development config: anonymous GET `/internal/doctor` zwraca 401/403/404; admin/scoped access nadal dostaje zsanityzowany raport.

## F-04 - Dane osobowe i recognition content sa logowane na poziomie Debug do Seq po plaintext HTTP

Type: Finding  
Severity: high  
Location: `Infrastructure/Grati.Infrastructure.Azure/Pulumi.dev.yaml:24`, `Infrastructure/Grati.Infrastructure.Azure/Pulumi.dev.yaml:25`, `Grati.Web/Configuration/ServiceCollectionExtensions.cs:159`, `Grati.Web/Configuration/ServiceCollectionExtensions.cs:168`, `Grati.Web/Configuration/ServiceCollectionExtensions.cs:215`, `Grati.Web/Controllers/RecognitionFlowController.cs:86`, `Grati.Web/Controllers/RecognitionFlowController.cs:158`, `Grati.Web/Controllers/ProfileController.cs:106`, `Grati.Web/Controllers/ProfileController.cs:245`, `Grati.Web/Controllers/ProfileController.cs:366`

Evidence: dev Pulumi ustawia `serverUrl: http://20.117.48.74:5341` i `ignoreCertificateErrors: true`, a App Service dziala jako `Production`. Serilog ustawia globalnie `.MinimumLevel.Debug()` i wysyla do Seq. Kontrolery loguja pelne pola formularzy: recognition `RawMessage`, `NormalizedMessage`, `CustomerDisplayName`, dane profilu `FirstName`, `Bio`, `PhotoUrl`, oraz tip `Handle`.

Exploit/Risk Path: uzytkownicy wpisuja dane osobowe i wiadomosci recognition; aplikacja zapisuje je jako debug logs i wysyla do zewnetrznego Seq po HTTP. Kazdy podmiot na trasie sieciowej lub z dostepem do Seq moze odczytywac tresci, a brak TLS uniemozliwia integralna ochrone transportu.

Impact: powazne ryzyko poufnosci PII i tresci rozpoznan, ekspozycja handle'i platnosci i profili, naruszenie oczekiwan prywatnosci. W dev deployment z publicznym App Service nadal sa to realne dane POC.

Remediation Requirement: nie loguj pelnych payloadow uzytkownika; zastap je dlugoscia, hashami lub licznikami. W deployment config wymagaj HTTPS dla Seq, nie dopuszczaj plaintext `http://`, a certificate bypass ogranicz do lokalnego developmentu bez realnych danych. Ustaw produkcyjne minimum logowania na `Information` lub wyzej.

Regression Test: test konfiguracji IaC/startup: `ASPNETCORE_ENVIRONMENT=Production` nie moze miec `Logging__Seq__ServerUrl` zaczynajacego sie od `http://` ani `IgnoreCertificateErrors=true`; test logowania potwierdza brak pelnych `RawMessage`, `Bio`, `PhotoUrl`, `Handle` w templates.

## F-05 - PayPal redirect akceptuje `http://` URL i przekierowuje klienta na plaintext

Type: Finding  
Severity: medium  
Location: `Grati.Web/Services/Common/PaypalTipProviderHandler.cs:26`, `Grati.Web/Services/Common/PaypalTipProviderHandler.cs:39`, `Grati.Web/Controllers/RecognitionFlowController.cs:142`, `Grati.Web/Controllers/RecognitionFlowController.cs:186`

Evidence: `PaypalTipProviderHandler.IsValidHandle` akceptuje absolutne URL-e ze schematem `http` lub `https` dla `paypal.me`, `www.paypal.me`, `paypal.com`, `www.paypal.com`. `BuildOutboundUrl` zwraca `asUri.ToString()` z opcjonalnie doklejana kwota. Recognition flow wykonuje `Redirect(tipSelection.Url)`.

Exploit/Risk Path: pracownik konfiguruje tip destination jako `http://paypal.com/...` albo `http://paypal.me/...`. Klient po wyslaniu recognition/tip dostaje redirect do plaintext HTTP, co ujawnia sciezke, kwote i referer oraz pozwala na network tampering przed ewentualnym upgrade po stronie PayPal.

Impact: utrata poufnosci i integralnosci outbound handoff dla przeplywu napiwkow, mozliwy phishing/tampering w sieciach niezaufanych. Host jest ograniczony do domen PayPal, wiec nie jest to ogolny open redirect.

Remediation Requirement: akceptuj tylko `https://` dla absolutnych PayPal URL-i albo normalizuj wszystkie poprawne hosty do kanonicznego `https://paypal.me/{handle}`. Rozwaz ograniczenie do `paypal.me` zamiast calego `paypal.com`.

Regression Test: test `PaypalTipProviderHandler`: `http://paypal.me/alice` i `http://paypal.com/...` sa odrzucane; `https://paypal.me/alice` przechodzi i redirect URL pozostaje HTTPS.

# Candidate Findings

## C-01 - Key Vault soft delete jest wylaczone w IaC

Type: Candidate Finding  
Candidate Severity: medium  
Confidence: medium  
Location: `Infrastructure/Grati.Infrastructure.Azure/Resources/KeyVault.cs:35`, `docs/key-vault-halny.md:18`

Evidence: Pulumi ustawia `EnableSoftDelete = false` dla dedykowanego Key Vault. Dokument lokalny rowniez odnotowuje to ustawienie. Vault przechowuje co najmniej sekret `Authentication--MicrosoftEntraExternalId--ClientSecret`.

Missing Confirmation: nie walidowalem zachowania Azure przy deployu ani aktualnej konfiguracji juz istniejacego vaulta. W nowszych Azure Key Vault soft-delete moze byc wymuszane przez platforme, wiec repo evidence nie potwierdza runtime exposure.

Potential Exploit/Risk Path: bledna operacja IaC lub kompromitacja konta z uprawnieniami administracyjnymi kasuje sekret albo vault bez mozliwosci odzyskania, powodujac downtime auth i ryzyko utraty materialu sekretnego/historii.

Validation Test: sprawdz aktualny vault przez Azure Portal/CLI: `softDeleteRetentionInDays`, `enableSoftDelete`, purge protection i role. Test IaC powinien wymagac soft delete/purge protection dla srodowisk z realnymi sekretami.

# Observations

## O-01 - Recognition flow celowo ujawnia tip destination niezaleznie od `IsPublic`

`RecognitionFlowViewService` wystawia wszystkie destinationy w recognition flow, podczas gdy public profile filtruje `IsPublic`. Testy i `docs/plan-1-user.md` opisuja to jako zamierzony kontrakt, wiec nie klasyfikuje tego jako Finding. To nadal wymaga jasnej kopii UI/produktu: uzytkownik moze myslec, ze `IsPublic=false` ukrywa payment handle przed wszystkimi anonimowymi powierzchniami, a nie tylko przed `/profile`.

# Follow-up

## FU-01 - Zweryfikowac runtime exposure endpointow diagnostycznych

Sprawdz w aktywnym dev/prod, czy `/internal/doctor`, `/health/ready`, `/openapi/v1.json`, `/swagger` i `/redoc` sa osiagalne publicznie oraz czy gateway/App Service ma dodatkowe ograniczenia.

## FU-02 - Zweryfikowac kontrole dostepu i retencje Seq

Repo pokazuje wysylke logow do Seq po `http://20.117.48.74:5341`, ale nie potwierdza ACL, auth UI, retencji ani sieciowych ograniczen tego hosta.

## FU-03 - Zweryfikowac rate limiting za reverse proxy

Rate limit recognition flow partycjonuje po `RemoteIpAddress|slug`. Trzeba potwierdzic, czy App Service/proxy przekazuje rzeczywisty adres klienta do aplikacji, czy wszyscy klienci widza adres proxy i limit jest nieskuteczny albo zbyt agresywny.

## FU-04 - Uruchomic autorytatywne sprawdzenie podatnosci zaleznosci

Ten review nie uruchamial zewnetrznych skanerow ani `dotnet list package --vulnerable`. Warto osobno potwierdzic advisories dla SkiaSharp/cropperjs/Microsoft.Identity.Web/Azure SDK/Dapper/Serilog na obecnych wersjach i lockfile/build output.
