# MeeTube TV: Claude Code context

MeeTube TV is MeeTube for Android TV and Google TV: app id `io.yash.meetube.tv`, name "MeeTube TV",
flavor `ststable`, app module `smarttubetv/` (Java packages keep their upstream names; those are code,
leave them). It started from SmartTube master `b8fbe00` (2026-11-03) and this repo's history starts there.
Gradle 7.5, JDK 17.

**This repo is TV only.** The phone app is a separate repo (github.com/yashoncode/meetube, its own
folder and CLAUDE.md). Never change it from here, and nothing done here may affect it: not its APK,
code, resources, dependencies, manifest, build, CI or behaviour.

## Repos
- `origin` = github.com/yashoncode/meetube-tv, branch `main`. `upstream` = yuliskov/SmartTube.
  `legacy` = yashoncode/meetube branch `tv`, where the TV app lived until 2026-11-14; releases
  tv-v0.0.1-beta to tv-v1.1.0 are on that repo.
- Submodules: `MediaServiceCore` = yashoncode/MediaServiceCore branch `tv` (origin = yashoncode,
  upstream = yuliskov; never mix it with the phone's `master`). `SharedModules` = yuliskov/SharedModules
  (no TV changes). settings.gradle resolves `./SharedModules` and `./MediaServiceCore` only, never `../`.
  Commit inside the submodule first, push `origin tv`, then commit the pointer bump here.

## Build
```
JAVA_HOME=<jdk17> ANDROID_HOME=<sdk> ./gradlew :smarttubetv:assembleStstableRelease -PtvAbi=armeabi-v7a
# -> smarttubetv/build/outputs/apk/ststable/release/MeeTubeTV_<ver>_universal.apk
```
- `-PtvAbi=<abi>` (our switch in smarttubetv/build.gradle) turns ABI splits off and builds one APK
  holding only that ABI. Real TVs: `armeabi-v7a`. The x86_64 TV emulator (AVD `tv_1080p`): `x86_64`.
  Without it you get the release set: armeabi-v7a, arm64-v8a and universal (no x86).
- With `keystore.properties` present the release build is signed with the release key (cert SHA-256
  b2f94a9a...). Every TV release must use that key or installed TVs refuse the update.
- Test on release builds: debug cold start is ~10 s, release 1.8 to 3.3 s. Judge speed only on release.
- Install: `adb -s <serial> install -r <apk>`, force-stop, then launch with
  `monkey -p io.yash.meetube.tv -c android.intent.category.LEANBACK_LAUNCHER 1`.

## Releases
- Bump versionName / versionCode in smarttubetv/build.gradle, put `## X.Y.Z` on top of CHANGELOG.md and,
  for a stable release, bump meetube_tv.json (version, versionCode, tv-vX.Y.Z APK links).
- Release commit subject is exactly `MeeTube TV X.Y.Z` (`MeeTube TV X.Y.Z Beta` for a beta): the Actions
  run is named after it. No provenance in commit titles; that lives in the README's Credits only.
- Tag `tv-vX.Y.Z` (or `-beta`) on main: release-tv.yml builds the signed APKs and publishes the release.
  Repo secrets: SIGNING_KEY (the .jks in base64), KEY_STORE_PASSWORD, ALIAS, KEY_PASSWORD.
- TVs on 1.1.0 or older read `raw.githubusercontent.com/yashoncode/meetube/tv/meetube_tv.json`. Until
  those have updated, each stable release also bumps that file on `legacy/tv` to the new APK links, or
  they never see the update.
- The README's Release badge and Download table still point at tv-v1.1.0 on yashoncode/meetube; at the
  first release from this repo, point them here (and add a Downloads badge like the phone README's).
- The phone app's "Install on TV" and its release notes look for `tv-v` releases on yashoncode/meetube.
  Once a TV release ships only here, the phone repo has to read this repo instead (a phone change).

## Keeping up with SmartTube beta
Beta builds come from yuliskov/SmartTube master; keep MeeTube TV current with their fixes and check for
new ones when starting TV work. `git fetch upstream master`, then
`git diff <last synced> upstream/master -- . ':!MediaServiceCore' ':!SharedModules' ':!README.md' ':!smarttubetv/build.gradle' | git apply -3`
and `git reset` (apply stages). Last synced: SmartTube 32.74 (`ab04c75f`, 2026-11-12). MediaServiceCore:
merge `upstream/master` into its branch `tv` (at least SmartTube's pointer), push `origin tv`, bump here.

## Rules
- Wording: MeeTube TV is MeeTube for Android TV and Google TV with its own design and tuning. Never
  "SmartTube with...", "a fork of", or "everything SmartTube does" in README, changelog, release notes or
  commits. Upstream credit lives in the README's Credits and LICENSE only.
- No `--` or em dashes in README, changelog or docs.
- Keep the TV UI light: no live per-frame blur (the reference TV is Android 14, armeabi-v7a, 1280x720).
- Before any MeeTube TV vs SmartTube benchmark, match settings: Card previews = muted boots ExoPlayer plus
  a Chromium WebView about 4 s after launch (+50 MB). Check `WebViews:` in `dumpsys meminfo`.
- logcat dumps contain NUL bytes: always `grep -a`. Always pin the adb serial (`adb -s <serial>`).
