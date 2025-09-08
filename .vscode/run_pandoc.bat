@echo off

set "WORKSPACE_FOLDER=%~dp0/../src/"

docker run --rm -v "%WORKSPACE_FOLDER%:/data" pandoc/minimal:latest-static %*
