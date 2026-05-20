# AppSec Review: Grati

Data: 2026-05-14  
Scope: cale repo  
Review Depth: standard  
ASVS Level: L2  
Tryb: offline, bez internetu, GitHuba, SaaS, runtime access i zewnetrznych skanerow

## Repository Context

Grati to POC aplikacji ASP.NET Core MVC dla worker-controlled recognition: publiczny customer flow, prywatny profil pracownika, profile photos w Azure Blob Storage, MS SQL/Dapper oraz Microsoft Entra External ID. Review objelo aplikacje webowa, domeny, repozytoria SQL, Azure/Pulumi IaC, pipeline i lokalna dokumentacje.

| Technology | Role |
| --- | --- |
| ASP.NET Core MVC / .NET 10 | Web host, routing, auth, controllers, Razor UI |
| Microsoft Entra External ID / Microsoft.Identity.Web | Sign-in/sign-out i zewnetrzna tozsamosc uzytkownika |
| MS SQL / Dapper / sqlproj | Persistencja users, recognitions, tip destinations i audit events |
| Azure Blob Storage | Publiczne przechowywanie avatarow profilu |
| Serilog / Seq | Logowanie aplikacyjne i diagnostyczne |
| Pulumi Azure Native | Dev App Service, storage, Key Vault i runtime app settings |

## Executive Summary

- Najmocniejszy potwierdzony problem to IDOR/BOLA w usuwaniu profile-photo blob: zalogowany uzytkownik moze ustawic wlasny `PhotoUrl` na publiczny blob innego profilu i skasowac cudzy avatar przez `/me/photo/remove`.
- Anonymous recognition flow automatycznie zatwierdza kazda tresc jako `Approved`, co pozwala publikowac niepozadane wpisy na publicznym profilu ofiary mimo zalozenia positive-only.
- `/internal/doctor` jest anonymous i mapowany poza development gate; lokalne testy dodatkowo utrwalaja oczekiwane anonymous 200.
- Dev deployment wysyla logi zawierajace PII i recognition text do plaintext Seq endpointu, przy globalnym `MinimumLevel.Debug()`.
- Ograniczenie review: nie sprawdzano runtime, realnej konfiguracji Azure/Entra/Seq, zewnetrznych advisory dla zaleznosci ani live reachability.

## Summary

| Typ | Liczba |
| --- | ---: |
| Findings | 4 |
| Candidate Findings | 2 |
| Observations | 5 |
| Follow-up | 5 |

## Final Findings Overview

| Type | ID | Severity / Candidate Severity | Area | Decision |
| --- | --- | --- | --- | --- |
| Finding | F-01 | high | Blob/object authorization | fix |
| Finding | F-02 | medium | Public content integrity / moderation | fix |
| Finding | F-03 | medium | Diagnostics exposure | fix |
| Finding | F-04 | medium | Logging / data protection | fix |
| Candidate Finding | C-01 | medium | Recognition object authorization | validate |
| Candidate Finding | C-02 | low | Outbound redirect / tip provider URL | validate |
| Observation | O-01 | low | Logout CSRF hardening | observe |
| Observation | O-02 | low | Profile enumeration | observe |
| Observation | O-03 | low | Security headers | observe |
| Observation | O-04 | low | Blob retention/orphan cleanup | observe |
| Observation | O-05 | low | External profile photo URL trust | observe |
| Follow-up | FU-01 | n/a | Dependency vulnerabilities | follow-up |
| Follow-up | FU-02 | n/a | Runtime route exposure | follow-up |
| Follow-up | FU-03 | n/a | Azure/Seq access controls | follow-up |
| Follow-up | FU-04 | n/a | Entra tenant policy | follow-up |
| Follow-up | FU-05 | n/a | Automated abuse controls | follow-up |

## Findings

### F-01

Type: Finding  
Title: IDOR w usuwaniu profile-photo blob pozwala skasowac cudzy publiczny avatar  
Severity: high

Location:

| File | Lines / Symbols / Routes |
| --- | --- |
| `Grati.Web/Controllers/ProfileController.cs` | `OnboardingProfile` zapisuje `form.PhotoUrl`, lines 152-153; `Edit`, lines 291-292; `RemovePhoto`, lines 518-527 |
| `Grati.Users/User/UserValidators.cs` | `SetProfilePhotoInputValidator`, lines 38-50 |
| `Grati.Web/Services/Profile/Photo/AzureBlobProfilePhotoStorage.cs` | `StoreAvatar`, lines 25-28; `DeleteAvatarByPublicUrl`, lines 45-52; `TryGetBlobPath`, lines 65-87 |
| `Infrastructure/Grati.Infrastructure.Azure/Resources/ProfilePhotoStorage.cs` | public blob container, `AllowBlobPublicAccess = true`, `PublicAccess = Blob` |

Evidence: upload zapisuje avatary pod `avatars/{userId:N}/{guid}.jpg`, ale kontroler pozwala zapisac dowolny absolutny `PhotoUrl` z formularza profilu. Domain validator wymaga tylko absolutnego URI. `DeleteAvatarByPublicUrl` parsuje dowolny publiczny URL z tego samego kontenera i usuwa wynikowy `blobPath` bez porownania z prefiksem aktualnego uzytkownika. Public profile renderuje `PhotoUrl`, wiec publiczny URL avatara ofiary jest latwy do zdobycia.

Exploit/Risk Path: zalogowany uzytkownik A otwiera publiczny profil B i kopiuje URL avatara, np. `https://.../profile-photos/avatars/{BUserId:N}/{guid}.jpg`. A wysyla edycje swojego profilu z `PhotoUrl` ustawionym na ten URL. Walidacja akceptuje absolutny URL. Nastepnie A wywoluje `POST /me/photo/remove`; kontroler pobiera `current.Profile.PhotoUrl`, usuwa go z profilu A, a storage usuwa blob ofiary B. Profil B zostaje z uszkodzonym wskazaniem na nieistniejacy avatar.

Impact: authenticated cross-user object deletion w publicznym storage, utrata integralnosci profilu ofiary i mozliwy defacement jej publicznej obecnosci.

Security Goal: operacje delete na blobach profilu musza byc ograniczone do blobow nalezacych do aktualnego `UserIdentity`.

Remediation Requirement: profil powinien przechowywac tylko zaufane, wygenerowane przez upload referencje albo storage delete musi przyjmowac `UserIdentity` i odrzucac sciezki poza `avatars/{userId:N}/`. Manualny `PhotoUrl` powinien byc usuniety albo ograniczony do owner-checked internal storage.

Implementation Hint: zmien `DeleteAvatarByPublicUrl` na owner-aware API, np. `DeleteAvatarByPublicUrl(UserIdentity userId, string publicUrl, ...)`, i wymagaj prefiksu `avatars/{userId.Id:N}/`.

Regression Test: test powinien ustawic `PhotoUrl` atakujacego na URL `avatars/{victimId:N}/x.jpg` i potwierdzic, ze `RemovePhoto` nie usuwa blobu poza prefiksem atakujacego oraz zwraca kontrolowany blad albo ignoruje obcy blob.

ASVS Mapping: `v5.0.0-8.2.2` data-specific access / IDOR/BOLA.  
OWASP Web/API Top 10 Category: API1:2023 Broken Object Level Authorization.

### F-02

Type: Finding  
Title: Anonymous recognition flow automatycznie zatwierdza i publikuje dowolna tresc na publicznym profilu  
Severity: medium

Location:

| File | Lines / Symbols / Routes |
| --- | --- |
| `Grati.Web/Controllers/RecognitionFlowController.cs` | `[AllowAnonymous]`, route `/{publicSlug}`, submit lines 64-70, auto-approval lines 167-169 |
| `Grati.Sql.Repository/Recognition/SqlRecognitionQueries.cs` | public feed wymaga `ModerationOutcome = Approved`, lines 32-51 |
| `Grati.Web/Views/PublicProfile/Index.cshtml` | public feed rendering, lines 85-107 |

Evidence: anonymous `POST /{publicSlug}` przyjmuje message o dlugosci co najmniej 2 znaki albo tagi. Po `grain.Submit(...)` kontroler ma TODO dla real moderation pipeline i natychmiast wykonuje `grain.Moderate(ModerationOutcome.Approved, occurredAt)`. Publiczny feed wybiera tylko `IsHidden = 0` i `ModerationOutcome = Approved`, a view renderuje `item.Message`.

Exploit/Risk Path: anonimowy atakujacy pobiera formularz dla `/{victimSlug}`, uzywa tokena antiforgery z formularza i wysyla negatywny albo naduzyciowy tekst. Aplikacja zapisuje wpis, oznacza go jako `Approved`, a publiczny profil ofiary pokazuje go w sekcji `What customers are saying`. Rate limit 5/min per IP+slug ogranicza tempo, ale nie zatrzymuje publikacji.

Impact: public profile defacement, naruszenie positive-only integrity model i reputacyjne szkody dla worker-controlled profilu.

Security Goal: publiczny feed powinien zawierac tylko tresci, ktore przeszly realna kontrole positive-only/moderation albo pozostawac niewidoczne do czasu zatwierdzenia.

Remediation Requirement: nie ustawiaj `Approved` dla user-generated message bez realnej decyzji moderacyjnej. Minimum dla POC: `PendingReview` dla message submissions albo deterministic positive-only filter; public feed nie moze wyswietlac tresci bez zatwierdzenia.

Regression Test: anonymous submission z negatywnym tekstem nie pojawia sie w `GetPublicRecognitionFeed` i nie jest renderowana na `/{publicSlug}/profile`; status powinien byc `PendingReview` albo `Rejected`.

ASVS Mapping: brak precyzyjnego L2 match dla product-specific content moderation; najblizszy cel to trusted server-side workflow decision.  
OWASP Web/API Top 10 Category: business logic abuse; pomocniczo API4:2023 Unrestricted Resource Consumption.

### F-03

Type: Finding  
Title: `/internal/doctor` jest anonymous i ujawnia stan oraz metadane konfiguracji srodowiska  
Severity: medium

Location:

| File | Lines / Symbols / Routes |
| --- | --- |
| `Grati.Web/Controllers/InternalDoctorController.cs` | `[AllowAnonymous]`, route `internal/doctor`, lines 9-20 |
| `Grati.Web/Program.cs` | `app.MapControllers()`, line 55 |
| `Grati.Web/Diagnostics/SqlConnectivityDoctorCheck.cs` | SQL status and connection-string configured fingerprint, lines 19-41 |
| `Grati.Web/Diagnostics/BlobStorageDoctorCheck.cs` | blob service/container metadata, lines 29-35 and 67-74 |
| `Grati.Web/Diagnostics/EntraConfigurationDoctorCheck.cs` | Entra callback paths, authority host and client-secret state, lines 25-41 |
| `Grati.Web/Diagnostics/SecretDiagnosticValue.cs` | secret length and fingerprint, lines 6-19 |
| `Grati.Web.IntegrationTests/HealthAndDoctorTests.cs` | anonymous `/internal/doctor` expected 200, lines 83-92 |

Evidence: controller is explicitly `[AllowAnonymous]` and mapped through `app.MapControllers()` in all environments. Integration test states `GET /internal/doctor is temporarily anonymous and returns 200`. Doctor checks return component status, exception type, authority host, callback paths, storage service authority, configured flags, secret length and 8-hex SHA-256 fingerprints.

Exploit/Risk Path: unauthenticated internet client requests `GET /internal/doctor` on the deployed app. The response reveals whether SQL/blob/Entra/time checks are healthy, which dependencies are configured, endpoint hostnames/callback paths, and whether secrets exist. An attacker can use this for environment fingerprinting, outage timing, dependency probing and correlation with other leaked secret fingerprints.

Impact: internal diagnostic surface exposed to unauthenticated users. Raw secrets are not returned, but operational state and configuration metadata should be operator-only.

Security Goal: detailed diagnostics must require operator authorization or network restriction. Public health endpoints should expose only minimal liveness/readiness.

Remediation Requirement: protect `/internal/doctor` with auth/role, environment gate or network gate. Keep `/health/live` and `/health/ready` minimal and anonymous only where platform probes require it.

Regression Test: unauthenticated `GET /internal/doctor` returns 401/403 outside local development; authorized operator request still receives sanitized JSON.

ASVS Mapping: `v5.0.0-8.2.1` for function-level access restriction; information-disclosure control mapping not found quickly in local L2 dataset.  
OWASP Web/API Top 10 Category: API5:2023 Broken Function Level Authorization; Web A05 Security Misconfiguration.

### F-04

Type: Finding  
Title: Dev deployment wysyla PII i tresci recognitions do plaintext Seq endpointu  
Severity: medium

Location:

| File | Lines / Symbols / Routes |
| --- | --- |
| `Infrastructure/Grati.Infrastructure.Azure/Pulumi.dev.yaml` | `serverUrl: http://20.117.48.74:5341`, `ignoreCertificateErrors: true`, lines 24-25 |
| `Infrastructure/Grati.Infrastructure.Azure/Resources/GratiWebApp.cs` | app settings for Seq, lines 41-42 |
| `Grati.Web/Configuration/ServiceCollectionExtensions.cs` | `MinimumLevel.Debug()`, `WriteTo.Seq(...)`, certificate bypass branch, lines 159-171 and 210-215 |
| `Grati.Web/Controllers/RecognitionFlowController.cs` | logs raw/normalized message and customer display name, lines 86-103 and 157-164 |
| `Grati.Web/Controllers/ProfileController.cs` | logs profile bio/photo URL/tip handles, representative lines 107-113, 246-252, 430-436 |

Evidence: Pulumi dev stack config wires Seq to `http://20.117.48.74:5341` and sets `ignoreCertificateErrors: true`; `GratiWebApp` emits those values as runtime app settings. Application logging uses `MinimumLevel.Debug()` for all environments and writes to Seq. Logged event templates include recognition `RawMessage`, normalized `Message`, `CustomerDisplayName`, profile `FirstName`, `Bio`, `PhotoUrl`, tip handles and user IDs.

Exploit/Risk Path: any network position between App Service and the Seq host, or any compromised/plaintext log collector path, can read or tamper with application logs containing PII and user-generated recognition content. Because the repo documents a public dev deployment, this can affect real POC validation users if dev is used with real data.

Impact: disclosure of PII and user-generated recognition content outside primary app/database controls. Certificate bypass also weakens authenticity if endpoint changes to HTTPS with an invalid certificate.

Security Goal: sensitive logs must be minimized and transmitted only over authenticated, encrypted channels to an approved sink with access control.

Remediation Requirement: use HTTPS with certificate validation for Seq or remove remote Seq from deployed environments; stop logging raw recognition messages, customer names, emails, bio, tip handles and full photo URLs at Debug/Information levels. Keep IDs/counts/hashes where needed.

Regression Test: configuration test rejects non-HTTPS Seq URL or `IgnoreCertificateErrors=true` for deployed environments; logging tests assert recognition submit and provisioning/profile logs do not include raw message/email/name/bio values.

ASVS Mapping: `v5.0.0-14.2.4` for data protection controls including logging, `v5.0.0-16.2.3` for documented log sinks, `v5.0.0-16.4.3` for secure log transmission.  
OWASP Web/API Top 10 Category: Web A02 Cryptographic Failures / A09 Logging and Monitoring Failures.

## Candidate Findings

### C-01

Type: Candidate Finding  
Title: Authenticated user can hide any recognition by GUID without owner check  
Candidate Severity: medium  
Confidence: high  
Location: `Grati.Web/Controllers/ProfileController.cs`, `HideRecognition`, lines 601-611; `Grati.Sql.Repository/Recognition/SqlRecognitionRepository.cs`, `GetById` selects by recognition id only, lines 103-116.

Evidence: `POST /me/recognitions/{id}/hide` is authenticated by controller-level `[Authorize]`, but then calls `grainClient.GetGrain<IRecognition>(new RecognitionIdentity(id))` and `grain.Hide(occurredAt)` before resolving/logging the current user. No code compares `recognition.RecipientUserId` with `currentUserId`. Existing test `HideRecognition_should_call_IRecognition_Hide` only verifies that the method invokes `IRecognition.Hide`.

Missing Confirmation: local public views do not render recognition GUIDs for other users, so practical exploitation requires a leaked/known UUID from logs, screenshots, browser state, database exposure or another endpoint.

Potential Exploit/Risk Path: logged-in attacker obtains another worker's recognition GUID and posts to `/me/recognitions/{victimRecognitionId}/hide` with a valid antiforgery token. The system hides the victim recognition from public feed without checking recipient ownership.

Validation Test: create two users and one recognition for victim; authenticated as attacker, post hide for victim recognition; expected fixed behavior is 403/404 and unchanged `IsHidden`.

Remediation Requirement: enforce owner check at trusted service/controller/domain boundary before mutating a recognition.

ASVS Mapping: `v5.0.0-8.2.2`.

### C-02

Type: Candidate Finding  
Title: PayPal tip redirect accepts `http://paypal.com` URLs, enabling plaintext outbound handoff  
Candidate Severity: low  
Confidence: medium  
Location: `Grati.Web/Services/Common/PaypalTipProviderHandler.cs`, `IsValidHandle` lines 21-28 and `BuildOutboundUrl` lines 33-39; redirects in `RecognitionFlowController.cs` lines 142 and 186.

Evidence: absolute PayPal URL is accepted when scheme is `http` or `https` and host is exact `paypal.me`, `www.paypal.me`, `paypal.com`, or `www.paypal.com`. The recognition flow redirects customers to the built URL when tip-only or recognition+tip is submitted.

Missing Confirmation: runtime/browser and PayPal redirect behavior were not validated offline; actual customer impact depends on whether the endpoint upgrades to HTTPS and whether arbitrary PayPal paths can mislead users.

Potential Exploit/Risk Path: worker configures `http://paypal.com/...`; customer choosing a tip is redirected through plaintext HTTP, exposing path/amount/referrer metadata and allowing network tampering before any PayPal upgrade.

Validation Test: configure a PayPal destination with `http://paypal.com/...`, submit tip-only flow, and confirm whether app emits a 302 to HTTP. Fixed behavior should reject non-HTTPS absolute URLs or canonicalize to HTTPS PayPal.me.

Remediation Requirement: accept only HTTPS PayPal URLs, preferably canonical `https://paypal.me/{handle}`.

ASVS Mapping: no precise L2 match found quickly; map to secure URL/protocol validation rationale.

## Observations

### O-01

`GET /account/sign-out` signs the user out without antiforgery protection. This is not a data-changing integrity finding because it logs the victim out rather than changing stored data, but it remains a logout-CSRF hardening gap. Location: `Grati.Web/Controllers/AccountController.cs`, `[HttpGet("sign-out")]`.

### O-02

`GET /api/slugs/availability?value=...` is `[AllowAnonymous]` and returns `taken` versus `available`. Public slugs are public by design, so this is not a confirmed privacy finding, but it enables low-cost enumeration of profile addresses. Location: `Grati.Web/Controllers/Api/SlugsController.cs`.

### O-03

No explicit CSP, Referrer-Policy, Permissions-Policy, or frame-ancestors policy was found in `Program.cs` or response middleware. Razor encoding is generally used, so this is hardening rather than a confirmed XSS finding.

### O-04

Uploading a new avatar stores a new blob and sets `PhotoUrl`, but the previous avatar is not deleted on replacement; account deletion later deletes all blobs under the user's prefix. This is not an immediate exploit path, but it increases retained user-owned blobs and should stay visible because account deletion has a strict hard-delete rule.

### O-05

Profile edit/onboarding accepts a user-controlled absolute `PhotoUrl` and public views render it as `<img src="@photoUrl">`. Razor encoding reduces XSS risk, but this allows external image hosts and can leak visitor IP/referrer to a user-selected third party. This is not a confirmed app compromise because the profile owner controls their own public profile content.

## Follow-up

### FU-01

Run dependency vulnerability checks for NuGet packages and vendored `wwwroot/lib/cropperjs` with approved controlled tooling or current advisories. This review did not use external scanners or internet.

### FU-02

Validate live route exposure for `https://grati-dev-web.azurewebsites.net/internal/doctor`, `/swagger`, `/redoc`, `/openapi/v1.json`, `/health/live`, and `/health/ready`. Repo evidence says doctor is anonymous, but runtime reachability was out of scope.

### FU-03

Validate Azure/Seq access controls: who can reach `http://20.117.48.74:5341`, whether ingestion/UI auth is enforced, whether logs are retained, and whether network restrictions exist outside this repo.

### FU-04

Validate Microsoft Entra External ID tenant-side controls that repo cannot prove offline: redirect URI allowlist, issuer validation behavior, PKCE/state/nonce behavior from middleware/runtime, session lifetime, MFA/conditional access, and provider configuration.

### FU-05

Validate abuse controls for anonymous recognition flow under realistic traffic: App Service forwarded IP handling for the rate limiter, distributed IP/bot behavior, CAPTCHA or adaptive throttling needs, and moderation workflow latency.
