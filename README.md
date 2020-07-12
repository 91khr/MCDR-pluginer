# MCDR-pluginer

A plugin manager for MCDR

## Requirements

Almost everything MCDR-pluginer requires is also required by MCDR.
By default, MCDR-pluginer uses git to manage plugins,
but this can be changed by replacing the `handle.py`.

## Usage

Just run `./pluginer.py`, and MCDR-pluginer will synchronize all,
this action includes installing and updating all plugins configurated,
and remove all plugins that are not configurated.

**WARNING**: MCDR-pluginer would remove all unrecognized symlinks in the plugins directory.

## Configuration

All configurations are in the `config.yaml`, it's with comment defaultly.
Since the file is added to the ignore list, changing it wouldn't affect remote repository.

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

### `plugins_dir`

The directory for MCDR to read plugins.

type: string

### `repo_dir`

The directory to store plugin repository

type: string

### `plugins`

The plugin list.

type: list

Each of the item of the list describes a plugin,
which can be either a string or an object.
In the case when it's a string, it stands for the `url` field of the object.
Unnecessary fields of the object would be generated from the necessary fields.

#### `url`

The URL of the plugin repository.
When the repository is hosted in github, it needn't have to be complete.

The field is necessary.

type: string

example: `https://github.com/TISUnion/Here` can be abbreviated to `TISUnion/Here`.

#### `content`

The filename of the plugin file.
Defaultly the same as the plugin name.
If there's only one python source file(recognized by the suffix) is the repository base,
the file would also be used, in spite of its name.
Can also be a list containing all essential files (and folders) of the plugin ---
that's why the field is not named `filename`.

type: string | list[string]

