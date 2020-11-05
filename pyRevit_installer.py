import clr
clr.AddReference("System")
import System
clr.AddReference("System.Collections")
from System.Collections.Generic import List
clr.AddReference("LibGit2Sharp")
from LibGit2Sharp import Repository, Commands, FetchOptions
from pathlib import Path
import colorful as col


def clone_repo(name, url):
    print(f"INFO: git clone: {name}")
    target_path = PROG_DATA / name
    if target_path.exists():
        print(f"INFO: repo {name} already exists at: {target_path}")
        return
    Repository.Clone(url, str(target_path))
    print(f"successfully cloned repo: {name}")


def fetch_repo(name):
    print(f"INFO: git fetch: {name}")
    target_path = PROG_DATA / name
    repo = Repository(str(target_path))
    #ref_specs = List[System.String]()
    #remote = repo.Network.Remotes["origin"]
    #ref_specs = remote.get_RefSpecs()
    Commands.Fetch(
        repo,
        "origin",
        List[System.String](),
        FetchOptions(),
        "",
    )


def create_rvt_addins(overwrite=False):
    for node in RVT_ADDINS_ROOT.iterdir():
        rvt_version = node.name
        pyrvt_addin = node / "pyRevit.addin"
        if not pyrvt_addin.exists():
            print(f"INFO: installing addin for rvt {rvt_version}")
            write_config(pyrvt_addin, pyrevit_addin_txt)
        elif overwrite:
            print(f"INFO: re-installing addin for rvt {rvt_version}")
            write_config(pyrvt_addin, pyrevit_addin_txt)
        else:
            print(f"INFO: pyRevit addin for rvt {rvt_version} exists already")


def create_pyrevit_config():
    PYREVIT_CONFIG_DIR.mkdir(exist_ok=True, parents=True)
    pyrevit_config = PYREVIT_CONFIG_DIR / "pyRevit_config.ini"
    if not pyrevit_config.exists():
        print(f"INFO: creating pyrevit config: {pyrevit_config}")
        write_config(pyrevit_config, pyrevit_config_txt)
    else:
        print(f"INFO: pyRevit config {pyrevit_config} exists already")


def write_config(path, content):
    with open(path, "w") as config:
        config.write(content)


REPOS = {
    "rvt_detector" :"https://github.com/frederic-beaupere/rvt_detector",
    "pyrevit":      "https://github.com/erneagholzbau/pyrevit",
    "pyRevit_erne": "https://github.com/erneagholzbau/pyrevit_erne",
}

pyrevit_addin_txt = r"""<?xml version="1.0" encoding="utf-8" standalone="no"?>
<RevitAddIns>
    <AddIn Type = "Application">
        <Name>PyRevitLoader</Name>
        <Assembly>C:\ProgramData\pyrevit\bin\engines\2710\pyRevitLoader.dll</Assembly>
        <AddInId>B39107C3-A1D7-47F4-A5A1-532DDF6EDB5D</AddInId>
        <FullClassName>PyRevitLoader.PyRevitLoaderApplication</FullClassName>
        <VendorId>eirannejad</VendorId>
    </AddIn>
</RevitAddIns>
"""
pyrevit_config_txt = """
[core]
outputstylesheet = "C:\\ProgramData\\pyrevit\\pyrevitlib\\pyrevit\\output\\outputstyles.css"
bincache = true
checkupdates = false
rocketmode = true
debug = false
verbose = false
filelogging = false
startuplogtimeout = 10
minhostdrivefreespace = 10
loadbeta = false
cpyengine = 385
userextensions = ["C:\\ProgramData\\pyRevit_erne"]
user_locale = "de_de"
tooltip_debug_info = false

[environment]
clones = {"pyrevit_erne":"C:\\ProgramData\\pyrevit"}
"""

PROG_DATA = Path("C:/ProgramData")
RVT_ADDINS_ROOT = PROG_DATA / "Autodesk" / "Revit" / "Addins"
PYREVIT_CONFIG_DIR = Path().home() / "AppData" / "Roaming" / "pyRevit"

print(col.bold_green("\nwelcome to Erne Holzbau pyRevit installer!"))

for repo_name, url in REPOS.items():
    print(f"\n_____ {col.cyan(repo_name)}")
    clone_repo(repo_name, url)
    fetch_repo(repo_name)

create_pyrevit_config()
create_rvt_addins()

print(col.bold_green("\ninstall successful!"))
input("press enter key to end script")
