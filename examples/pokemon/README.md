# Nushell Plugin in Python

This is an example implementation of a Pokemon plugin for Nushell in Python,
based on [vsoch/nushell-plugin-pokemon](https://www.github.com/vsoch/nushell-plugin-pokemon) 
but instead using the [nushell](https://pypi.org/project/nushell/)
plugin package.  The final executable needs to be called `nu_plugin_pokemon` and
on the path.

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
  > pokemon {flags} (avatar) 

flags:
  --catch
  --list
  --list-sorted
  --avatar <String>
  --pokemon <String>
  --help
```

Notice how (avatar) can be provided as an optional positional argument OR a flag?
That means these two commands do the same thing:

```bash
> pokemon --avatar Dinosaur
> pokemon Dinosaur
```

As a helper, the plugin library automatically adds a `--help` function that also shows
usage for each argument, if the creator provided it:

```bash
> pokemon --help
poke: Catch an asciinema pokemon on demand.

avatar AVATAR       generate avatar
--catch             catch a random pokemon
--list              list pokemon names
--list-sorted       list sorted names
--avatar AVATAR     generate avatar
--pokemon POKEMON   get pokemon
--help              show this usage
```

Again, notice that this function also shows avatar as both a positional and optional argument.
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

And then interact the same as previously! We can't build a single binary here because
the data needed for the pokemons is an external file provided by the pokemon module.
