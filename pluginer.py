#!/usr/bin/python3
import src.helper as helper

class Pluginer:
    def init(self):
        helper.load_conf('config.yaml', pattern = {
            'plugins_dir': '../MCDR/plugins',
            'repo_dir': '../plugin_repl',
            'plugins': [],
            })

if __name__ == "__main__":
    pass

