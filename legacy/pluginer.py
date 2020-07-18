#!/usr/bin/python3
from ruamel.yaml import YAML
import handle
import os.path as path
import os
import shutil
import typing
from status import PluginState, PluginAction



class Pluginer:
    # {{{ Init
    def _load_conf(self, default, location = "config.yaml"):
        """ Load the pluginer configuration """
        # Read config file
        try:
            with open(location, "r") as f:
                self.conf = YAML(typ="safe").load(f)
        except FileNotFoundError:
            self.conf = {}

        # Set default values for the key
        def touch_key(key):
            if key not in self.conf:
                self.conf[key] = default[key]
        touch_key('plugins_dir')
        touch_key('repo_dir')
        touch_key('plugins')



    def _init_plg(self, plg_key = 'plugins'):
        """ Init the plugins """
        self.plgs = {}
        plg_list = self.conf[plg_key]
        plg_next = []
        while plg_list:
            for nowplg in plg_list:
                if isinstance(nowplg, dict):
                    it = { 'url': nowplg['url'] }
                    if 'content' in nowplg:
                        it['content'] = nowplg['content']
                    if 'dependencies' in nowplg:
                        deps = nowplg['dependencies']
                        if not isinstance(deps, list):
                            raise TypeError("Dependencies must be a list!")
                        plg_next += deps
                elif isinstance(nowplg, str):
                    it = { 'url': nowplg }
                else:
                    raise TypeError("The type of a plugin item can only be str or dict")

                # Process the url
                if not (it['url'].startswith('http://')
                        or it['url'].startswith('https://')) and ('/' in it['url']):
                    it['url'] = "https://github.com/" + it['url']

                name = it['url'][it['url'].rfind('/') + 1:]
                if name in self.plgs:
                    raise ValueError("There cannot be two plugins with the same name!")
                self.plgs[name] = it
            plg_list = plg_next
            plg_next = []



    def init(self) -> None:
        """ Init the pluginer """
        self._load_conf({
            'plugins_dir': '../MCDR/plugins',
            'repo_dir': '../plugin_repo',
            'plugins': [],
            })
        self._init_plg()
    # }}} End init



    # {{{ Query
    def query(self) -> typing.Mapping[str, PluginState]:
        """ Query the state of all plugins """
        res = {}
        for name in self.plgs:
            repopath = path.join(self.conf['repo_dir'], name)
            if not path.exists(repopath):
                res[name] = PluginState.NotInstalled
            else:
                res[name] = handle.query(repopath)
        return res
    # }}} End query



    # {{{ Synchronize
    def _link_files(self, state) -> None:
        for name in state:
            repopath = path.join(self.conf['repo_dir'], name)
            def linkfile(name):
                dstfile = path.join(self.conf['plugins_dir'], name)
                if path.exists(dstfile): os.remove(dstfile)
                os.symlink(path.join(repopath, name), dstfile)
            nowplg = self.plgs[name]
            if 'content' not in nowplg:
                # Gauss one: is it the same as name
                if path.exists(path.join(repopath, f"{name}.py")):
                    linkfile(f"{name}.py")
                    nowplg['content'] = f"{name}.py"
                    continue
                # That's it if there's only one file...
                filelist = list(filter(lambda f: path.splitext(f.name),
                    os.scandir(repopath)))
                if len(filelist) == 1:
                    linkfile(filelist[0])
                    nowplg['content'] = filelist[0]
                else:
                    print(f"Dont know what's the plugin, alternatives: {filelist}")
                # Normal cases: content is given
            elif isinstance(nowplg['content'], list):
                for it in nowplg['content']:
                    linkfile(it)
            else:
                linkfile(nowplg['content'])

    def sync(self) -> typing.Mapping[PluginState, typing.List[str]]:
        """ Sync all plugins, return all non operated plugins """
        state = self.query()
        sub_state = {}

        for name in state:
            # Perform operation
            if state[name] in [PluginState.Diverged, PluginState.UpToDate]:
                continue
            operation = {
                    PluginState.NotInstalled: PluginAction.Install,
                    PluginState.NeedUpdate: PluginAction.Update,
                    }
            repopath = path.join(self.conf['repo_dir'], name)
            handle.sync(repopath, operation[state[name]], self.plgs[name]['url'])

            # Scan plugin repository for configuration
            sub = Pluginer()
            sub._load_conf(self.conf, repopath)
            sub._init_plg('dependencies')
            self.plgs.update(sub.plgs)
            sub_state += sub.sync()
            if 'content' in sub.conf and 'content' not in self.plgs[name]:
                self.plgs[name]['content'] = sub.conf['content']

        self._link_files(state)

        state.update(sub_state)
        return state
    # }}} End synchronize



    def clean(self) -> None:
        # Remove all symlinks
        with os.scandir(self.conf['plugins_dir']) as diriter:
            for it in diriter:
                if it.is_symlink():
                    os.remove(it.path)
        # Remove all non installed plugins
        with os.scandir(self.conf['repo_dir']) as diriter:
            for it in diriter:
                if it.name not in self.plgs:
                    shutil.rmtree(path.realpath(it.path))



if __name__ == "__main__":
    def main():
        plg = Pluginer()
        plg.init()
        plg.clean()
        state = plg.sync()
        for [nowstat, prompt] in [
                (PluginState.UpToDate, "up to date"),
                (PluginState.Diverged, "diverged with upstream")]:
            print("these plugins are {}, so they're not synchronized: {}".format(prompt,
                list(filter(lambda name: state[name] == nowstat, state))))

    main()

# vim: fdm=marker
