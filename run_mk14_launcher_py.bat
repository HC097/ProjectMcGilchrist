@echo off
echo Starting Mk14 - The Threefold Engine with 'py' launcher...

start cmd /k "py logos_api.py"
start cmd /k "py mythos_api.py"
start cmd /k "py sophion_router.py"

echo All agents launched in separate terminals.
pause
