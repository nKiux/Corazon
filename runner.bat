@echo off
echo initialize...
echo installing requirements
start /wait requirements.bat
echo Running...
start /wait python.exe UI_Beta2.py 