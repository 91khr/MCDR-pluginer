from enum import Enum

class PluginStatus(Enum):
    """ Present the state of a plugin """
    NotInstalled = -2
    Diverged = -1
    UpToDate = 0
    NeedUpdate = 1

class PluginAction(Enum):
    """ The action should be taken to synchronize the plugin """
    Update = 0
    Install = 1

