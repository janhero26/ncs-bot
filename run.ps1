while ($true) {
    Write-Host "Starting NCS bot..."
    .\.venv\Scripts\python.exe bot.py
    Write-Host "Bot exited. Restarting in 5 seconds..."
    Start-Sleep -Seconds 5
}