@echo off
pip install -r requirements.txt
pyinstaller --onefile --noconsole main_gui.py --name PromptPilot
