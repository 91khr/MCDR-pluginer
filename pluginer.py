#!/usr/bin/python3
import helper
import os
from pathlib import Path
from status import PluginInfo
from subplugin import Subplugin, SyncInfo
from typing import Iterable



class Pluginer:
    def init(self):
        conf = helper.load_conf('config.yaml', pattern = {
            'plugins_dir': '../MCDR/plugins',
            'repo_dir': '../plugin_repl',
            'plugins': [],
            })
        self.repo_dir : Path = Path(conf.repo_dir)
        self.plugins_dir : Path = Path(conf.plugins_dir)
        self.plgs : [Subplugin] = [
                (lambda plg: Subplugin(
                    self.repo_dir / plg.name,
                    PluginInfo.parse(plg)))(it) for it in conf.plugins ]



    def query(self):
        return [ it.query() for it in self.plgs ]



    def sync(self):
        proc_plg = self.plgs
        while not proc_plg:
            next_plg = []
            for plg in proc_plg:
                helper.log("info", "sync", f"Synchronizing plugin {plg.name}")

                # Synchronize the plugin itself
                info = plg.sync()
                if info.status != SyncInfo.SyncStatus.Succeed:
                    helper.log("warning", "sync", f"Error synchronizing {plg.name}:" + {
                        SyncInfo.SyncStatus.NoContent: f"no plugin content",
                        SyncInfo.SyncStatus.SyncRepoFailed: f"failed to synchronize the repository",
                        }[info.status])
                    continue

                # Link its contents to output dir
                for ctnt in plg.content if isinstance(plg.content, Iterable) else [ plg.content ]:
                    dstfile = self.plugins_dir / ctnt
                    if dstfile.exists():
                        os.remove(dstfile)
                    if not dstfile.parent.exists():
                        dstfile.parent.mkdir(parent=True)
                    os.symlink(plg.path / ctnt, dstfile)

                next_plg.extend(info.dependencies)



if __name__ == "__main__":
    plgs = Pluginer()
    plgs.init()
    plgs.query()
    plgs.sync()

