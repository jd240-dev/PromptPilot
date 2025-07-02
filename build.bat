@echo off
echo Building PromptPilot executable...
pyinstaller --onefile --noconsole main_cmd.py
pyinstaller --noconsole main_gui.py
