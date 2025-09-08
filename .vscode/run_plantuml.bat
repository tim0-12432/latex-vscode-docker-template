@echo off
setlocal

set INPUT_DIR=%~dp0\..\src\figures\plantuml
set OUTPUT_DIR=%~dp0\..\src\figures\plantuml\output

if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

for %%f in ("%INPUT_DIR%\*.plantuml") do (
    echo Generiere Diagramm für %%~nxf...

    type "%%f" | docker run --rm -i ashleycaselli/plantuml -tpng > "%OUTPUT_DIR%\%%~nf.png"
)

echo Fertig!
endlocal
