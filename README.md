# MCDR-pluginer

A plugin manager for MCDR

# Requirements

Almost everything MCDR-pluginer requires is also required by MCDR.
By default, MCDR-pluginer uses git to manage plugins,
but this can be changed by replacing the `handle.py`.

# Installation

Just clone the repo, and it's ready for use.

# Usage

Just run `./pluginer.py`, and MCDR-pluginer will synchronize everything,
including installing and updating all plugins configurated,
and removing all non-configurated plugins.

**WARNING**: MCDR-pluginer would remove all unrecognized symlinks in the plugins directory.

# Configuration(for server operators)

All configurations are in the `config.yaml`, it's with comment defaultly.
The file is ignored by default, therefore changing it wouldn't affect remote repository.

In fact, our default configuration assume that
you have such a directory structure in your server:

```
server/
| MCDR/
| | plugins/
| | server/ -> ../server
| server/
| MCDR-pluginer/
| plugin_repo/
```

## `plugins_dir`

The directory for MCDR to read plugins.

type: string

## `repo_dir`

The directory to store plugin repository

type: string

## `plugins`

The plugin list.
Each of the item of the list describes a plugin,
which can be either a string or an object.
In the case when it's a string, it stands for the `url` field of the object.
Unnecessary fields of the object would be generated from the necessary fields.

type: list

example:
```yaml
plugins:
  - TISUnion/Here
  - url: 91khr/QuickBackupM
    content: QuickBackupM.py
```

### `url`

The URL of the plugin repository.
When the repository is hosted in github, it needn't have to be complete.

The field is necessary.

type: string

example: `https://github.com/TISUnion/Here` can be abbreviated to `TISUnion/Here`.

### `content`

The filename of the plugin file.
Defaultly the same as the plugin name.
If there's only one python source file(recognized by the suffix) is the repository base,
the file would also be used, in spite of its name.
Can also be a list containing all essential files (and folders) of the plugin ---
that's why the field is not named `filename`.

type: string | list[string]

### `dependencies`

The dependencies of the plugin.
Usually this is done by the plugin author
(as long as there is a `plugin_info.yaml` in the plugin directory),
but in case when this isn't done, you should declare this manually.

type: list, each of the items has the same type as items in [`plugins`](#plugins)

# Configuration(for plugin developers)

Some configurations may be made in plugin repository,
thus the installation of the plugin for MCDR-pluginer users can be simplified.

The keys are the same as those of any item in the key `plugins` of the main configuration.

## `content`

The filename of the plugin file, or a list of plugin files.
Would be overrided by the main configuration

## `dependencies`

The dependencies of the plugin.
The dependencies configurated in the main configuration would be used to update this list.

