@echo off
echo ready to setup...
PAUSE
pip install PyQt5 scipy opencv-python
echo:
echo setup done!
choice /c:YN /m:"would you like to launch the app now?"
echo %ERRORLEVEL%
goto setup%errorlevel%

:setup1
start HRMonitor2.0.exe


:setup2

