# Nushell Plugin in Python

This is an example implementation of a Pokemon plugin for Nushell in Python,
based on [vsoch/nushell-plugin-pokemon](https://www.github.com/vsoch/nushell-plugin-pokemon) 
but instead using the [nushell](https://pypi.org/project/nushell/)
plugin package. There are two options for creating a plugin in Python

 - installing all Python module dependencies to your system, and using a Python file
 - compiling your plugin to generate one package

In both cases, the final executable needs to be called `nu_plugin_pokemon` and
on the path. If you don't create a single executable, the other module dependencies
 (e.g., pokemon) need to be installed as well. You can build the two Dockerfiles
provided to see the difference.

## Run Locally

If you want to run the plugin locally, you will nead nushell installed, along
with the pokemon and nushell modules:

```bash
$ pip install pokemon
$ pip install nushell
```

You can then start nushell, and interact with the plugin. Make sure your present
working directory with the file is added to the PATH. Here are some examples:

```bash
export PATH=$PWD:$PATH
$ nu
```

This is the default help provided by nushell, given that it finds the plugin on the
path and it's valid.

```bash
> help pokemon
Catch an asciinema pokemon on demand.

Usage:
  > pokemon {flags} 

flags:
  --catch
  --list
  --list-sorted
  --avatar <String>
  --pokemon <String>
  --help
```

As a helper, the plugin library automatically adds a `--help` function that also shows
usage for each argument, if the creator provided it:

```bash
> pokemon --help
pokemon: Catch an asciinema pokemon on demand.
--catch             catch a random pokemon
--list              list pokemon names
--list-sorted       list sorted names
--avatar AVATAR     generate avatar
--pokemon POKEMON   get pokemon
--help             show this usage
```

And then have fun!


```bash
> pokemon --catch
> pokemon --avatar dinosaur
> pokemon --list
> pokemon --list-sorted
> pokemon --pokemon Dedenne
```

If you print an invalid argument it will print the usage. See the [nu_plugin_pokemon](nu_plugin_pokemon)
script for how the plugin should be created.


## Logging

Logs are printed to `/tmp/nu_plugin_pokemon.log` unless you set logging=False when
you initialize the plugin.

```bash
 cat /tmp/nu_plugin_pokemon.log
root - INFO - REQUEST {"jsonrpc":"2.0","method":"config","params":[]}
root - INFO - METHOD config
root - INFO - plugin-config: {"name": "pokemon", "usage": "Catch an asciinema pokemon on demand.\n\n  --avatar AVATAR    generate a pokemon avatar for some unique id.\n  --pokemon POKEMON  generate ascii for a particular pokemon (by name)\n  --catch            catch a random pokemon!\n  --list             list pokemon available\n  --list-sorted      list pokemon available (sorted)\n  --help             show this usage\n", "positional": [], "rest_positional": null, "named": {"avatar": {"Optional": "String"}, "pokemon": {"Optional": "String"}, "catch": "Switch", "help": "Switch", "list": "Switch", "list-sorted": "Switch"}, "is_filter": false}
root - INFO - Printing response {'name': 'pokemon', 'usage': 'Catch an asciinema pokemon on demand.\n\n  --avatar AVATAR    generate a pokemon avatar for some unique id.\n  --pokemon POKEMON  generate ascii for a particular pokemon (by name)\n  --catch            catch a random pokemon!\n  --list             list pokemon available\n  --list-sorted      list pokemon available (sorted)\n  --help             show this usage\n', 'positional': [], 'rest_positional': None, 'named': {'avatar': {'Optional': 'String'}, 'pokemon': {'Optional': 'String'}, 'catch': 'Switch', 'help': 'Switch', 'list': 'Switch', 'list-sorted': 'Switch'}, 'is_filter': False}
```

## Build Python

You can optionally build the container:

```bash
make
# docker build -t vanessa/nu-plugin-pokemon .
```

## Build Single Binary

We can use Cython to generate a single binary, and that example is built as follows:

```bash
make standalone
# docker build -f Dockerfile.standalone -t vanessa/nu-plugin-pokemon .
```
