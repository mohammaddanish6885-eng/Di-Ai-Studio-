# DI-Ai-Studio — Flow-inspired Android creative workspace

This project has been updated to remove the private owner login and owner-only authentication. The app opens directly to its creative workspace; there is no sign-in or public registration screen.

## Current package contents
- Android app built with Kotlin and Jetpack Compose.
- Flow-inspired dark creative workspace with Create, Library, Scenes and Tools sections.
- Text-to-video interface with Community/Premium provider selection, prompt assistant toggle, reference image picker, start/end frame pickers, aspect ratio, duration, camera motion and output count controls.
- Local list of generated videos and a basic scene clip collection.
- FastAPI backend with no owner login or bearer-token requirement.
- GitHub Actions workflow to build a debug APK and upload it as an artifact.

## Important feature status
This is an updated project/source package, not a finished APK. The connected backend currently implements text-to-video only. Image generation, true prompt-agent behavior, reference/start/end-frame conditioning, image/video editing, background removal, upscaling, timeline trimming/reordering/export, and the other Tools screens need their respective provider/model adapters and processing modules. The UI surfaces those workflows but does not pretend they are already operational. Provider API compatibility must be checked against the exact model selected.

## Configure backend
1. Copy `backend/.env.example` to `backend/.env`.
2. Add your provider credentials to the server environment only.
3. Deploy the FastAPI app using `uvicorn app:app --host 0.0.0.0 --port 8000` behind HTTPS.
4. In `android/app/build.gradle.kts`, replace `https://YOUR-PRIVATE-BACKEND.example/` with your HTTPS backend URL, ending in `/`.

**Security note:** Because login has been removed, protect the backend using server-side rate limits, usage quotas, and/or network/API gateway controls. Never expose provider keys inside the APK.

## Build APK from GitHub on Android
1. Upload the complete contents of this folder to the root of your GitHub repository.
2. Open the repository's **Actions** tab.
3. Select **Build DI-Ai-Studio APK**, then tap **Run workflow**.
4. When the run succeeds, open it and download the `DAN-AI-STUDIO-debug-apk` artifact.
5. Extract the downloaded artifact ZIP and install `app-debug.apk`.

The APK must be built after the backend URL and provider setup are configured if you want generation to work.
