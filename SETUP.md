# Setup

## Backend
- Python 3.11+
- Copy `backend/.env.example` to `backend/.env` and set provider credentials.
- Run `pip install -r requirements.txt` then `uvicorn app:app --host 0.0.0.0 --port 8000`.
- Deploy behind HTTPS.

## Android
- Set `BASE_URL` in `android/app/build.gradle.kts` to your deployed HTTPS API URL, ending with `/`.
- Build with Android Studio or the included GitHub Actions workflow.

## No login
Owner login, email/password authentication, JWT sessions and owner-only endpoint checks have been removed. The app opens directly. Secure the backend with rate limits and quotas because unauthenticated generation endpoints can be abused.

## Feature integration status
Text-to-video has a backend adapter. Image generation and the advanced creative tools are UI entry points only until matching providers and processing modules are configured. Frame/reference selections are currently UI selections and are not yet passed to the video provider adapter.
