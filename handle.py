from status import PluginState, PluginAction
from subprocess import getoutput
import os

def query(plg: str) -> PluginState:
    """ Query the state of a plugin """
    local = getoutput(f"git -C {plg} rev-parse @")
    remote = getoutput(f"git -C {plg} rev-parse @{{u}}")
    base = getoutput(f"git -C {plg} merge-base @ @{{u}}")
    if local == remote:
        return PluginState.UpToDate
    elif local == base:
        return PluginState.NeedUpdate
    else:
        return PluginState.Diverged

def sync(path: str, action: PluginAction, url: str = None) -> bool:
    """ Synchronize a plugin to the plugin repo """
    if action == PluginAction.Install:
        if url == None:
            raise ValueError("Expected a non-null url")
        os.system(f"git clone --progress {url} {path}")
    elif action == PluginAction.Update:
        os.system(f"git -C {path} pull --ff-only --progress --rebase=false")

