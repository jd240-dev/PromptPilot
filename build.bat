@echo off
REM Simple launcher script for PromptPilot
cd /d %~dp0

echo Installing dependencies...
pip install -r requirements.txt

echo Pulling model (phi3:mini) from Ollama...
ollama pull phi3:mini

echo Launching PromptPilot...
python main_cmd.py
pause
