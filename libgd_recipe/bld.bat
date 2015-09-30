REM Build script for Windows

REM Build step

nmake /f %RECIPE_DIR%\Makefile.vc build_libs
if errorlevel 1 exit 1

REM Install step
copy %PREFIX%\libgd.dll %LIBRARY_BIN%\
if errorlevel 1 exit 1
copy %PREFIX%\libgd.lib %LIBRARY_LIB%\
if errorlevel 1 exit 1
copy %PREFIX%\libgd.lib %LIBRARY_LIB%\gd.lib
if errorlevel 1 exit 1
copy %PREFIX%\libgd_a.lib %LIBRARY_LIB%\
if errorlevel 1 exit 1
copy src\*.h %LIBRARY_INC%\	
if errorlevel 1 exit 1