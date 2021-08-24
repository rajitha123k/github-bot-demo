@ECHO OFF
SETLOCAL EnableDelayedExpansion 
SETLOCAL EnableExtensions

SET /A ecode=0

:: verify
SET /P conf="About to delete all global and local npm modules and clear the npm cache. Continue (y/[n])?
IF /I NOT "%conf%"=="y" (
  ECHO operation aborted
  SET /A ecode=!ecode!+1
  GOTO END
)

:: wipe global and local npm root
FOR %%a IN ("" "-g") DO (

  :: get root path into var
  SET cmd=npm root %%~a
  FOR /f "usebackq tokens=*" %%r IN (`!cmd!`) DO (SET npm_root=%%r)

  :: paranoid
  ECHO valida