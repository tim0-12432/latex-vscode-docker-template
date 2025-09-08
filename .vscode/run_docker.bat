@echo off
if "%1"=="" (
    echo Fehler: Kein Befehl angegeben. Bitte pdflatex, makeindex oder bibtex und Datei als Argument übergeben.
    exit /b 1
)

set "WORKSPACE_FOLDER=%~dp0/../src/"

docker run --rm -v "%WORKSPACE_FOLDER%:/workdir" -w /workdir texlive/texlive:latest %*
