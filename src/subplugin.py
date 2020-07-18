from status import PluginStatus, PluginAction
import handle

class Subplugin:
    def __init__(self, path, url):
        self.path = path
        self.url = url



    def query(self):
        self.status = handle.query(self.path)
        return self.status



    def sync(self):
        # Perform operation
        operation = {
                PluginStatus.NotInstalled: PluginAction.Install,
                PluginStatus.NeedUpdate: PluginAction.Update,
                }
        handle.sync(self.path, operation[self.status], self.url)

        # Scan plugin repository for configuration

