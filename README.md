# pyrevit_installer
non-admin installer of Erne Holzbau pyRevit

## build standalone exe with pyinstaller
needed dependencies in directory /deps:
* libgit2sharp:
    * LibGit2Sharp [github file link](https://github.com/eirannejad/pyRevit/blob/master/bin/LibGit2Sharp.dll)
    * git2-106a5f2 [github file link]()
* colorful <br>
    rgb.txt [github file link](https://github.com/timofurrer/colorful/blob/master/colorful/data/rgb.txt)

then this pyinstaller build command:

`pyinstaller --onefile pyRevit_installer.spec`

will build in `/build` and create a single file executable in `/dist`
