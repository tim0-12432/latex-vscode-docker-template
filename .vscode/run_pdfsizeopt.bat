@echo off

set "WORKSPACE_FOLDER=%~dp0/../src/"

docker run --rm -v "%WORKSPACE_FOLDER%:/workdir" --platform linux/amd64 ptspts/pdfsizeopt:latest pdfsizeopt --use-pngout=no thesis.pdf thesis_opt.pdf
