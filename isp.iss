; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "MemorizeMe"
#define MyAppVersion "1.0"
#define MyAppPublisher "Rifat"
#define MyAppURL "https://ismailhrifat.wordpress.com/"
#define MyAppExeName "meme.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{98D81B01-F40E-46D1-A2E7-AF229F4A941B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableDirPage=yes
DisableProgramGroupPage=yes
LicenseFile=C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\liscense.txt
InfoBeforeFile=C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\inforfirst.txt
InfoAfterFile=C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\infosecond.txt
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
OutputDir=C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe
OutputBaseFilename=MemorizeMe setup
SetupIconFile=C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\data.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\font.ttf"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\icon.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\ismai\OneDrive - BUET\My App\MemorizeMe\keyfile.json"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

