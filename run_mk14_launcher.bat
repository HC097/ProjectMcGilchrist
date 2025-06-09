@echo off
echo Starting Mk14 - The Threefold Engine...

start cmd /k "python logos_api.py"
start cmd /k "python mythos_api.py"
start cmd /k "python sophion_router.py"

echo All agents launched in separate terminals.
pause
