from status import PluginStatus, PluginAction
from subprocess import getoutput
import os

def query(plg: str) -> PluginStatus:
    """ Query the state of a plugin """
    local = getoutput(f"git -C {plg} rev-parse @")
    remote = getoutput(f"git -C {plg} rev-parse @{{u}}")
    base = getoutput(f"git -C {plg} merge-base @ @{{u}}")
    if local == remote:
        return PluginStatus.UpToDate
    elif local == base:
        return PluginStatus.NeedUpdate
    else:
        return PluginStatus.Diverged

def sync(path: str, action: PluginAction, url: str = None) -> int:
    """ Synchronize a plugin to the plugin repo """
    if action == PluginAction.Install:
        if url == None:
            raise ValueError("Expected a non-null url")
        return os.system(f"git clone --progress {url} {path}")
    elif action == PluginAction.Update:
        return os.system(f"git -C {path} pull --ff-only --progress --rebase=false")

