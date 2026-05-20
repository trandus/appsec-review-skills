# Repository Context

Grati to POC aplikacji ASP.NET Core MVC/.NET 10 z Microsoft Entra External ID, Dapper/MS SQL, publicznymi profilami pracownikow, anonimowym flow rozpoznania/tipow i Azure Blob Storage dla avatarow. Review byl offline, lokalny, bez runtime, internetu i zewnetrznych skanerow. Najwazniejsze granice zaufania: anonimowy klient publicznego sluga, zalogowany wlasciciel profilu, cudze recognition/profile/tip destinations, diagnostyka operatora, SQL, Blob Storage i Seq.

# Executive Summary

Potwierdzono 5 podatnosci. Najbardziej ryzykowne sa: brak kontroli wlasciciela przy ukrywaniu recognition, mozliwosc usuniecia cudzego bloba avatara przez edytowalny `PhotoUrl`, anonimowy `/internal/doctor`, logowanie PII do zdalnego Seq po `http://` z globalnym `Debug`, oraz dopuszczenie `http://` przekierowan PayPal. Dodatkowo 3 obszary wymagaja walidacji produktu lub srodowiska.

# Summary

| Type | Count |
|---|---:|
| Findings | 5 |
| Candidate Findings | 3 |
| Observations | 1 |
| Follow-up | 4 |

# Final Findings Overview

| Type | ID | Severity / Candidate Severity | Area | Decision |
|---|---|---|---|---|
| Finding | F-01 | medium | Authorization / recognition ownership | fix |
| Finding | F-02 | medium | Blob authorization / profile photo | fix |
| Finding | F-03 | medium | Diagnostics exposure | fix |
| Finding | F-04 | high | Logging transport / sensitive data | fix |
| Finding | F-05 | medium | Payment redirect / plaintext handoff | fix |
| Candidate Finding | C-01 | medium | Tip destination privacy | validate |
| Candidate Finding | C-02 | low | Account deletion consistency | validate |
| Candidate Finding | C-03 | low | Public slug enumeration | validate |
| Observation | O-01 | low | Browser auth hygiene | observe |
| Follow-up | FU-01 | n/a | Runtime exposure | follow-up |
| Follow-up | FU-02 | n/a | Seq controls | follow-up |
| Follow-up | FU-03 | n/a | Ownership regression tests | follow-up |
| Follow-up | FU-04 | n/a | Product privacy contract | follow-up |

# Findings

## F-01 - Zalogowany uzytkownik moze ukryc cudze recognition przez znany GUID

Type: Finding

Severity: medium

Location: `Grati.Web/Controllers/ProfileController.cs:603`, `Grati.Web/Controllers/ProfileController.cs:606`, `Grati.Web/Controllers/ProfileController.cs:607`; `Grati.Recognition/Recognition/Recognition.cs:97`

Evidence: `POST /me/recognitions/{id}/hide` jest pod `[Authorize]`, ale kontroler tworzy `IRecognition` po samym `RecognitionIdentity(id)` i od razu wywoluje `Hide`. Dopiero po ukryciu pobiera `currentUserAccessor.RequireCurrentUserId`, a pobrany `userId` sluzy tylko do logu. Agregat `Recognition.Hide` nie przyjmuje ani nie sprawdza wlasciciela/recipienta.

Exploit/Risk Path: zalogowany uzytkownik A zdobywa GUID recognition uzytkownika B z UI, logow, odpowiedzi prywatnej/publicznej, auditow albo innego przecieku. A wysyla `POST /me/recognitions/{victimId}/hide` z wlasnym tokenem antiforgery. Serwer ukrywa recognition B z publicznego feedu bez filtra `RecipientUserId = currentUserId`.

Impact: nieuprawniona modyfikacja cudzego profilu reputacyjnego i usuwanie publicznej widocznosci pozytywnych opinii. Wplyw jest ograniczony do ukrywania, ale dotyka integralnosci danych innego uzytkownika.

Remediation Requirement: przed `Hide` zaladowac recognition i potwierdzic, ze `RecipientUserId == currentUserId`, albo wprowadzic metode repozytorium/komende `HideForRecipient(recognitionId, currentUserId)` wykonujaca sprawdzenie w transakcji. Nie polegac na tym, ze endpoint znajduje sie pod `/me`.

Regression Test: test kontrolera lub integracyjny, w ktorym current user A probuje ukryc recognition z `RecipientUserId = B`; oczekiwane 404/403 i brak zmiany `IsHidden`.

## F-02 - Edytowalny `PhotoUrl` pozwala usunac cudzy blob avatara w tym samym kontenerze

Type: Finding

Severity: medium

Location: `Grati.Web/Models/Profile/EditProfileForm.cs:26`, `Grati.Web/Models/Profile/OnboardingProfileForm.cs:28`, `Grati.Users/User/UserValidators.cs:42`, `Grati.Web/Controllers/ProfileController.cs:291`, `Grati.Web/Controllers/ProfileController.cs:527`, `Grati.Web/Services/Profile/Photo/AzureBlobProfilePhotoStorage.cs:45`

Evidence: formularze profilu zawieraja ukryte `PhotoUrl`, a walidacja domenowa wymaga tylko absolutnego URL-a. `Edit`/`OnboardingProfile` zapisuje `form.PhotoUrl.Trim()` do profilu. `RemovePhoto` pobiera aktualny `current.Profile.PhotoUrl` i wywoluje `DeleteAvatarByPublicUrl`. Storage usuwa dowolna sciezke bloba, jezeli URL ma ten sam scheme/server i prefiks kontenera; nie sprawdza prefiksu `avatars/{currentUserId:N}/`.

Exploit/Risk Path: uzytkownik A znajduje publiczny URL avatara B, np. `https://.../profile-photos/avatars/{BUserId:N}/{guid}.jpg`. A wysyla edycje profilu z `PhotoUrl` ustawionym na ten URL. Nastepnie wywoluje `/me/photo/remove`; aplikacja usuwa wskazany blob B, bo nalezy do tego samego kontenera.

Impact: nieuprawnione usuniecie cudzych avatarow, uszkodzone odwolania na profilach ofiar i naruszenie integralnosci user-owned blobow.

Remediation Requirement: traktowac `PhotoUrl` jako server-owned wartosc. Nie przyjmowac go z formularza poza wynikiem kontrolowanego uploadu. `DeleteAvatarByPublicUrl` powinno wymagac `UserIdentity` i usuwac tylko blob pod `avatars/{userId:N}/`; odrzucac albo ignorowac URL spoza tego prefiksu.

Regression Test: ustaw profil A na URL z prefiksem `avatars/{BUserId:N}/...` i potwierdz, ze `RemovePhoto` nie wywoluje usuniecia tego bloba. Dodac test storage dla prefiksu wlasciciela.

## F-03 - `/internal/doctor` jest anonimowy i ujawnia diagnostyke srodowiska

Type: Finding

Severity: medium

Location: `Grati.Web/Controllers/InternalDoctorController.cs:9`, `Grati.Web/Controllers/InternalDoctorController.cs:10`, `Grati.Web/Diagnostics/EntraConfigurationDoctorCheck.cs:25`, `Grati.Web/Diagnostics/EntraConfigurationDoctorCheck.cs:41`, `Grati.Web/Diagnostics/BlobStorageDoctorCheck.cs:53`, `Grati.Web/Diagnostics/SqlConnectivityDoctorCheck.cs:53`, `Grati.Web.IntegrationTests/HealthAndDoctorTests.cs:84`

Evidence: kontroler `/internal/doctor` ma `[AllowAnonymous]`. Test integracyjny wprost oczekuje anonimowego 200. Raport doctor zwraca statusy komponentow SQL/blob/Entra/time, host authority, callback paths, typy wyjatkow oraz metadane sekretow jako `configured`, dlugosc i 8-hex fingerprint.

Exploit/Risk Path: anonimowy klient odpytuje `/internal/doctor` na publicznym hostingu i zbiera informacje o stanie SQL, Blob Storage i Entra, rozroznia bledy konfiguracji, potwierdza obecnosc sekretow oraz koreluje fingerprinty/dlugosci z innymi przeciekami.

Impact: operator-only diagnostyka jest publiczna. Nie ma surowych sekretow, ale endpoint pomaga fingerprintowac srodowisko, zaleznosci i awarie.

Remediation Requirement: wymagac autoryzacji operatora/admina albo ograniczyc endpoint do sieci wewnetrznej. Usunac fingerprinty i dlugosci sekretow z odpowiedzi HTTP; takie dane moga pozostac w lokalnych narzedziach operatora, jezeli sa chronione.

Regression Test: anonimowe `GET /internal/doctor` powinno zwracac 401/403 w nie-development. Test payloadu powinien potwierdzic brak `Fingerprint` i `Length` dla sekretow.

## F-04 - Dane profilu i recognition trafiaja do Seq przez plaintext HTTP z globalnym poziomem Debug

Type: Finding

Severity: high

Location: `Grati.Web/Configuration/ServiceCollectionExtensions.cs:159`, `Grati.Web/Configuration/ServiceCollectionExtensions.cs:215`, `Infrastructure/Grati.Infrastructure.Azure/Pulumi.dev.yaml:21`, `Infrastructure/Grati.Infrastructure.Azure/Pulumi.dev.yaml:24`, `Infrastructure/Grati.Infrastructure.Azure/Pulumi.dev.yaml:25`, `Grati.Web/Controllers/RecognitionFlowController.cs:86`, `Grati.Web/Controllers/ProfileController.cs:107`, `Grati.Web/Controllers/ProfileController.cs:246`

Evidence: Serilog ustawia globalnie `.MinimumLevel.Debug()`. Devowy App Service w Pulumi dziala jako `aspNetCoreEnvironment: Production`, ale `seq.serverUrl` to `http://20.117.48.74:5341`, a `ignoreCertificateErrors: true` aktywuje handler z `ServerCertificateCustomValidationCallback = true`. Logi debug zawieraja pelne pola: recognition `RawMessage`, `NormalizedMessage`, `RawCustomerDisplayName`, profil `FirstName`, `Role`, `Bio`, `PhotoUrl`, slug oraz tip handle.

Exploit/Risk Path: publiczny/dev deployment obsluguje realne dane POC. Kazdy submit recognition albo edycja profilu wysyla PII i tresci opinii do zdalnego Seq po plaintext HTTP; ruch moze byc podslyuchany lub zmodyfikowany w sieci. Globalny Debug zwieksza zakres danych, a bypass certyfikatu utrwala zly wzorzec transportu.

Impact: materialne ujawnienie danych osobowych, tresci recognition i identyfikatorow/tip metadata poza aplikacje i SQL. To jest ryzyko wyzsze niz zwykle nadmiarowe logowanie, bo lokalna konfiguracja laczy PII, zdalny endpoint i plaintext transport.

Remediation Requirement: nie logowac pelnych payloadow uzytkownika; zamienic je na dlugosci, liczniki, kategorie albo korelacyjne identyfikatory. Dla publicznych deploymentow wymagac HTTPS do Seq, wylaczyc certificate bypass i ustawic `Information` lub wyzej. Jezeli Seq wymaga auth, uzyc sekretu API key z Key Vault.

Regression Test: test konfiguracji IaC/startup odrzuca `Logging__Seq__ServerUrl` zaczynajacy sie od `http://` oraz `IgnoreCertificateErrors=true` dla publicznego/Production. Test log templates potwierdza brak pelnych `RawMessage`, `Bio`, `PhotoUrl`, `Handle`.

## F-05 - PayPal tip redirect akceptuje `http://` i przekierowuje klienta na plaintext

Type: Finding

Severity: medium

Location: `Grati.Web/Services/Common/PaypalTipProviderHandler.cs:26`, `Grati.Web/Services/Common/PaypalTipProviderHandler.cs:39`, `Grati.Web/Controllers/RecognitionFlowController.cs:142`, `Grati.Web/Controllers/RecognitionFlowController.cs:186`

Evidence: `PaypalTipProviderHandler.IsValidHandle` dopuszcza absolutne URL-e z `http` albo `https` dla `paypal.me`, `www.paypal.me`, `paypal.com`, `www.paypal.com`. `BuildOutboundUrl` zwraca `AppendAmount(asUri.ToString(), amount)` bez normalizacji schematu. Recognition flow zwraca `Redirect(tipSelection.Url)`.

Exploit/Risk Path: pracownik ustawia tip destination jako `http://paypal.me/alice` albo `http://paypal.com/...`. Klient wysylajacy tip-only lub recognition+tip dostaje 302 na plaintext HTTP, co ujawnia sciezke, kwote i referer oraz pozwala na network tampering przed ewentualnym upgrade po stronie PayPal.

Impact: oslabienie integralnosci i poufnosci platniczego handoffu. Atak wymaga, zeby pracownik skonfigurowal niebezpieczny URL albo zostal do tego nakloniony, ale dotyka klientow korzystajacych z publicznego flow.

Remediation Requirement: akceptowac tylko `https://` dla absolutnych PayPal URL-i albo normalizowac poprawne hosty do kanonicznego `https://paypal.me/{handle}`. Rozwazyc ograniczenie do `paypal.me` zamiast calego `paypal.com`.

Regression Test: `http://paypal.me/alice` i `http://paypal.com/x` sa odrzucane; bare handle i `https://paypal.me/alice` przechodza; `RecognitionFlowController` nigdy nie zwraca redirectu do `http://`.

# Candidate Findings

## C-01 - Recognition flow pokazuje niepubliczne tip destinations anonimowym odwiedzajacym slug

Type: Candidate Finding

Title: Niepubliczne tip handles sa dostepne na publicznym recognition flow

Candidate Severity: medium

Confidence: medium

Location: `Grati.Web/Services/RecognitionFlow/RecognitionFlowViewService.cs:43`, `Grati.Web/Services/PublicProfile/PublicProfileViewService.cs:44`, `Grati.Web/Services/PublicProfile/PublicProfileViewService.cs:45`, `Grati.Web.Tests/Controllers/RecognitionFlowControllerTests.cs:463`

Evidence: publiczny profil filtruje `TipDestinations` po `IsPublic`, ale recognition form dla anonimowego sluga bierze wszystkie `profile.TipDestinations`. Test potwierdza przekierowanie PayPal nawet dla `IsPublic = false`.

Missing Confirmation: czy `IsPublic=false` ma oznaczac tylko "nie pokazuj na publicznym profilu", czy ogolnie "nie ujawniaj bez dodatkowego kontekstu". Test sugeruje obecny zamiar produktowy, ale nazwa i rozdzial public profile vs recognition flow tworza ryzyko prywatnosci.

Potential Exploit/Risk Path: kazdy, kto zna publiczny slug, otwiera `/{slug}` i widzi albo uzywa tip destination ukrytego z `/{slug}/profile`, w tym potencjalny payout handle.

Validation Test: ustalic kontrakt produktu i dodac test: gdy destination jest niepubliczne, czy `GET /{slug}` ma je zawierac. Jezeli nie, filtrowac rowniez recognition flow.

## C-02 - Kasowanie konta wykonuje usuniecie blobow przed SQL, co moze zostawic czesciowo aktywne konto po awarii

Type: Candidate Finding

Title: Account deletion nie jest atomowe miedzy Blob Storage i SQL

Candidate Severity: low

Confidence: medium

Location: `Grati.Web/Controllers/ProfileController.cs:681`, `Grati.Web/Controllers/ProfileController.cs:682`, `Grati.Web/Controllers/ProfileController.cs:683`, `Grati.Sql.Repository/Users/SqlUserDataDeletionService.cs:33`

Evidence: kontroler najpierw wywoluje `photoStorage.DeleteAvatarsForUser`, potem `userDataDeletion.DeleteAllForUser`. SQL ma transakcje i weryfikacje pozostalych rows, ale Blob Storage jest poza ta transakcja.

Missing Confirmation: brak runtime i scenariusza awarii produkcyjnej. To bardziej ryzyko lifecycle/privacy niz typowy atak zewnetrzny.

Potential Exploit/Risk Path: awaria SQL po usunieciu blobow zostawia konto i SQL rows aktywne, ale z usunietymi avatarami; awaria blobow przed SQL blokuje hard-delete mimo poprawnej prosby uzytkownika.

Validation Test: test awarii `DeleteAllForUser` po sukcesie `DeleteAvatarsForUser` i decyzja produktowa: retry job, tombstone deletion request albo kolejnosc SQL->blob z idempotentnym cleanupem.

## C-03 - Anonimowy endpoint slug availability ulatwia enumeracje profili

Type: Candidate Finding

Title: `api/slugs/availability` zwraca `taken` anonimowym klientom

Candidate Severity: low

Confidence: medium

Location: `Grati.Web/Controllers/Api/SlugsController.cs:11`, `Grati.Web/Controllers/Api/SlugsController.cs:25`, `Grati.Web/Services/Profile/SlugAvailabilityService.cs:31`

Evidence: endpoint jest `[AllowAnonymous]` i zwraca `taken`, gdy publiczny profil istnieje. Nie widac rate limitu dla tego endpointu.

Missing Confirmation: publiczne profile sa z zalozenia odkrywalne po slugu, wiec sama informacja `taken` moze byc akceptowalna. Brak runtime telemetry o skali/brute force.

Potential Exploit/Risk Path: atakujacy automatycznie odpytuje popularne imiona/slug patterny i buduje liste aktywnych profili bez pobierania pelnych stron.

Validation Test: potwierdzic wymagania discovery. Jezeli enumeracja jest niepozadana, ograniczyc endpoint do zalogowanych/onboarding albo dodac rate limit i bardziej neutralne odpowiedzi.

# Observations

## O-01 - GET sign-out zmienia stan sesji bez antiforgery, ale wplyw jest ograniczony

`AccountController` obsluguje `GET /account/sign-out` i `POST /account/sign-out` bez tokena na GET. To nie jest pelne finding, bo efektem jest glownie wylogowanie ofiary, a nie przejecie konta lub danych. Warto jednak preferowac POST + antiforgery dla operacji zmieniajacych stan sesji.

# Follow-up

## FU-01 - Sprawdzic runtime exposure endpointow

Zweryfikowac na docelowym hostingu, czy publicznie osiagalne sa `/internal/doctor`, `/api/diagnostics/ping`, `/health/ready`, `/openapi/v1.json`, `/swagger` i `/redoc`. Repo potwierdza anonimowy doctor; runtime exposure nie byl testowany.

## FU-02 - Sprawdzic kontrolki Seq

Zweryfikowac, kto ma dostep sieciowy i UI/API do `http://20.117.48.74:5341`, jaka jest retencja, czy jest auth/API key i czy endpoint nadal przyjmuje logi z aplikacji.

## FU-03 - Dodac cross-user testy dla operacji po identyfikatorach

Przejsc wszystkie endpointy `/{id:guid}` i operacje grain/repository po samym ID. Priorytet: recognition hide, tip destination update/remove, blob deletion. Testy powinny jawnie ustawiac current user A i obiekt nalezacy do B.

## FU-04 - Ustalic publiczny kontrakt tip destinations

Potwierdzic, czy `IsPublic=false` ma ukrywac destination tylko z publicznego profilu, czy rowniez z publicznego recognition flow dostepnego po slugu. Od tej decyzji zalezy, czy C-01 jest podatnoscia wymagajaca poprawki.
