@echo off
setlocal enabledelayedexpansion

REM Set the Maven version
set MAVEN_VERSION=3.9.3

REM Set the download URL
set DOWNLOAD_URL=https://dlcdn.apache.org/maven/maven-3/%MAVEN_VERSION%/binaries/apache-maven-%MAVEN_VERSION%-bin.zip

REM Set default Maven installation directory
set INSTALL_DIR=C:\Program Files\Apache\maven

REM Prompt for confirmation
set /P CONFIRM=This script will install Maven %MAVEN_VERSION%. Do you wish to continue (Y/N)?
if /I not "%CONFIRM%"=="Y" exit /b 0

REM Check for administrative privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires administrative privileges. Please run as administrator.
    exit /b 1
)

REM Check if JAVA_HOME is already set
echo Checking JAVA_HOME...
if not defined JAVA_HOME (
    echo JAVA_HOME not set, attempting to set it...
    for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\JavaSoft\JRE" /v CurrentVersion') do set CURRENT_VERSION=%%b
    for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\JavaSoft\JRE\%CURRENT_VERSION%" /v JavaHome') do set JAVA_HOME=%%b
    REM Set JAVA_HOME permanently
    echo Setting JAVA_HOME...
    setx JAVA_HOME "%JAVA_HOME%"
) else (
    echo JAVA_HOME is already set.
)

REM Check if Maven is already installed
if exist "%INSTALL_DIR%\apache-maven-%MAVEN_VERSION%" (
    echo Maven %MAVEN_VERSION% is already installed at %INSTALL_DIR%\apache-maven-%MAVEN_VERSION%
    exit /b 0
)

REM Download Maven
echo Downloading Maven %MAVEN_VERSION%...
powershell -Command "Invoke-WebRequest %DOWNLOAD_URL% -OutFile apache-maven-%MAVEN_VERSION%-bin.zip"

REM Extract the downloaded zip file to the installation directory
echo Extracting Maven...
powershell -Command "Expand-Archive -Path apache-maven-%MAVEN_VERSION%-bin.zip -DestinationPath '%INSTALL_DIR%' -Force"

REM Set Maven home directory
set MAVEN_HOME=%INSTALL_DIR%\apache-maven-%MAVEN_VERSION%

REM Set MAVEN_HOME permanently
echo Setting MAVEN_HOME...
setx MAVEN_HOME "%MAVEN_HOME%"

REM Adding Maven bin directory to the PATH environment variable permanently
echo Adding Maven to system PATH...
setx Path "%MAVEN_HOME%\bin;%Path%"

REM Output Maven version (Note: May need to restart command prompt to take effect)
echo Maven installation complete! Please restart your command prompt to use Maven.
