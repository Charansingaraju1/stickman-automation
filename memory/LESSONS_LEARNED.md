# LESSONS LEARNED

- **2026-11-28 — EdgeTTS Multilingual Voice Failures:** `en-US-AndrewMultilingualNeural` raised `NoAudioReceived` on punctuation-heavy lines. Keep `Christopher`, `Guy`, `Brian` with multi-voice retry fallback.
- **2026-11-28 — GitHub Runner Dependency Drift:** Eager module-level imports of Google OAuth libraries broke `cloud_auto_stock.yml` where OAuth dependencies weren't installed (`8056fba`). Keep publisher clients lazy-imported or clearly isolated.
- **2026-11-28 — Title & Template Spams Hurt YPP Safety:** Repeated `"Why You Should NEVER..."` prefixes and generic outros (`"So next time..."`) hurt retention and YPP originality checks. Keep `<38` char unique hooks and mid-clause Frame-0 loop bridges.
- **2026-11-29 — PowerShell UTF-8 BOM & File URL Gotcha:** Windows PowerShell `Set-Content -Encoding UTF8` writes a `\ufeff` BOM (breaking `.env` key matching), and `import.meta.url === "file://" + process.argv[1]` fails on Windows backslashes (`pathToFileURL()` fixes it cleanly).
- **2026-11-29 — Secret Scanning Regex Gap:** `audit_security()` originally missed Telegram `BOT_TOKEN` patterns, allowing a token in `upload_to_youtube.py` to commit unflagged. Always audit all secret formats across workflows and Python files.
