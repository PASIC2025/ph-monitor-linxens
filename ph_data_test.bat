@echo off
setlocal EnableDelayedExpansion

set URL=https://ph-monitor-m9fw.onrender.com/api/ph-data

:loop
for %%P in (3.0 3.5 4.0 4.5 5.0 5.5 6.0 6.5 7.0 7.5 8.0 8.5 9.0 9.5 10.0) do (
    rem Get current UTC timestamp in ISO format
    for /f %%T in ('powershell -NoLogo -NoProfile -Command "(Get-Date).ToUniversalTime().ToString(\"yyyy-MM-ddTHH:mm:ssZ\")"') do set TS=%%T

    echo Sending pH %%P at !TS!

    rem Send JSON body: {"ph": <value>, "timestamp": "<ISO time>"}
    curl -X POST "%URL%" ^
      -H "Content-Type: application/json" ^
      -d "{\"ph\": %%P, \"timestamp\": \"!TS!\"}"

    echo.
    timeout /t 5 /nobreak >nul
)
goto loop
