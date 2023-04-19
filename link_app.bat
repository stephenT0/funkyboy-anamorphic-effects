
call "%~dp0tools\packman\python.bat" "C:\Users\Studio 4\Documents\USD\code\funkyboy-anamorphic-effects/link_app.bat" %*
if %errorlevel% neq 0 ( goto Error )

:Success
exit /b 0

:Error
exit /b %errorlevel%
