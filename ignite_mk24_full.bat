@echo off
echo === IGNITING Mk24 SYSTEM ===

REM Launch all required Ollama models in separate terminals
start "Ollama - Mistral" cmd /k "ollama run mistral"
start "Ollama - OpenHermes" cmd /k "ollama run openhermes"
start "Ollama - TinyLLaMA" cmd /k "ollama run tinyllama"

REM Pause briefly to give models time to warm up
timeout /t 3 > nul

REM Launch SOPHION Mk24 Chat Control Panel
start "SOPHION Control Panel" cmd /k "py sophion_control_panel_mk24_chat.py"
