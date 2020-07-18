from status import PluginStatus, PluginAction, PluginInfo
import handle
import helper
import os
from pathlib import Path
from enum import Enum



class SyncInfo:
    """ Information gathered during synchronizing subplugins """

    class SyncStatus(Enum):
        """ The status of a syhchronization """
        Succeed = 0
        NoContent = 1
        SyncRepoFailed = 2

    def _Dump_members(self):
        """ Show the members to language server, and give an example to them """
        self.code : int = 0
        self.status : SyncStatus = SyncStatus.Succeed
        self.dependencies : [PluginInfo] = []



class Subplugin:
    def __init__(self, path : str | Path, info: PluginInfo):
        self.path : Path = Path(path)
        self.url : str = info.url
        self.name : str = info.name
        self.content : [str] | str = info.content
        self.dependencies : [PluginInfo] = info.dependencies
        self._depnames : [str] = [ it.name for it in self.dependencies ]



    def query(self) -> PluginStatus:
        self.status = handle.query(self.path)
        return self.status



    def sync(self) -> SyncInfo:
        res = SyncInfo()

        # Perform operation
        res.code = handle.sync(self.path, {
            PluginStatus.NotInstalled: PluginAction.Install,
            PluginStatus.NeedUpdate: PluginAction.Update,
            }[self.status or self.query()], self.url)
        if res.code != 0:
            res.status = SyncInfo.SyncStatus.SyncRepoFailed
            return res

        # Scan plugin repository for configuration
        conf = helper.load_conf(self.path / 'config.yaml', {
            'content': '',
            'dependencies': [],
            })
        res.dependencies = dict([
            (it.name, PluginInfo.parse(it)) for it in conf['dependencies']
            if it.name not in self._depnames
            ]).values()
        self.dependencies.extend(res.dependencies)

        # Process the content
        # In fact if: while can break elegantally
        while self.content == '':
            # Guess from the plugin name
            if (self.path / f"{self.name}.py").exists():
                self.content = f"{self.name}.py"
                break
            # Guess from the files
            filelist = [ it for it in os.scandir(self.path) if it.suffix == '.py' ]
            if len(filelist) != 0:
                res.status = SyncInfo.SyncStatus.NoContent
            else:
                self.content = filelist[0]
            break

        return res

