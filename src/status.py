from enum import Enum
from urllib.parse import urlparse
from os.path import basename



class PluginStatus(Enum):
    """ Present the state of a plugin """
    NotInstalled = -2
    Diverged = -1
    UpToDate = 1
    NeedUpdate = 2



class PluginAction(Enum):
    """ The action should be taken to synchronize the plugin """
    Update = 1
    Install = 2



class PluginInfo:
    """ Information of a plugin """
    def _Dump_members(self):
        """ Show the members to language server, and give an example to them """
        self.url : str = ''
        self.name : str = ''
        self.content : [str] | str = 'example.py'
        self.dependencies : [PluginInfo] = []

    @staticmethod
    def parse(info : dict) -> PluginInfo:
        """ Parse the info to a plugin's info """
        res = PluginInfo()
        res.url = info.url
        res.name = basename(urlparse(res.url).path)
        res.dependencies = [ res.parse(it) for it in info.get('dependencies', []) ]
        res.content = info.get('content', '')
        return res

