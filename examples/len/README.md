# Nu Plugin Len

This is an example length plugin based on [the nushell len example](https://github.com/nushell/contributor-book/blob/master/en/plugins.md#creating-a-plugin-in-python) but instead using the [nushell](https://pypi.org/project/nushell/)
plugin package. There are two options for creating a plugin in Python

 - installing all Python module dependencies to your system, and using a Python file
 - compiling your plugin to generate one package

## Run Locally

If you want to run the plugin locally, you will nead nushell installed.

```bash
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
> help len
Return the length of a string

Usage:
  > len {flags} 

flags:
  --help
```

Here is a basic example to use it:

```bash
> echo four | len
━━━━━━━━━━━
 <unknown> 
───────────
         4 
━━━━━━━━━━━
```

And a slightly more complex one, showing the length of the names of the files in
the present working directory.

```bash
 ls | get name | len
━━━┯━━━━━━━━━━━
 # │ <unknown> 
───┼───────────
 0 │        13 
 1 │         9 
━━━┷━━━━━━━━━━━
```

As a helper, the plugin library automatically adds a `--help` function that also shows
usage for each argument, if the creator provided it.

```bash
> len --help
len: Return the length of a string

--help              show this usage
```

## Logging

Logs are printed to `/tmp/nu_plugin_len.log` unless you set logging=False when
you initialize the plugin.

## Build Python

You can optionally build the container, doing a regular make will build a container
with nu and the installed python modules:

```bash
make
# docker build -t vanessa/nu-plugin-len .
```
```bash
$ docker run -it vanessa/nu-plugin-len
root@c7235d999a44:/code# nu
/code> help len
Return the length of a string

Usage:
  > len {flags} 

flags:
  --help

/code> echo four | len
━━━━━━━━━
 <value> 
─────────
       4 
━━━━━━━━━
```

You can also make a container with a standalone binary - we use [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/operating-mode.html) to do this.

```bash
make standalone
$ docker run -it vanessa/nu-plugin-len
```

And execution proceeds as before. We can prove that we don't need the modules anymore because
the [Dockerfile.standalone](Dockerfile.standalone) does `pip3 uninstall -y nushell` and it still works.
Why might you want to do this? It will mean that your plugin is a single file (binary) and you don't
need to rely on modules elsewhere in the system. I suspect there are other ways to compile
python into a single binary (e.g., cython) but this was the first I tried, and fairly straight forward.
If you find a different or better way, please contribute to this code base!
