# Nu Plugin Plus

There is already an [add](https://github.com/nushell/nushell/blob/master/src/plugins/add.rs) plugin (so we can't define that) but this simple plugin is instead called "plus" and shows how to use a filter with
positional arguments to add two numbers (integers).  You can watch an example here:

[![asciicast](https://asciinema.org/a/277050.svg)](https://asciinema.org/a/277050?speed=2)

Or here are simple examples of how it works!

```bash
Add a number to what is passed to the filter.

Usage:
  > plus {flags} <number> 

flags:
  --help
```

Add two integers:

```bash
> echo 4 | plus 4
━━━━━━━━━━━
 <unknown> 
───────────
         8 
━━━━━━━━━━━
```

Another!

```bash
> echo 4 | plus 4 | plus 4
12
```

If you give the wrong type, no go!

```bash
> echo boo | plus 8
boo is not a number
```

Combine with other plugins too. Here is an example of listing files, getting the name,
calculating the length, and adding 100 to it.

```bash
> ls | get name | len | plus 100
━━━┯━━━━━━━━━━━
 # │ <unknown> 
───┼───────────
 0 │ 114 
 1 │ 108 
 2 │ 109 
 3 │ 109 
 4 │ 110 
 5 │ 121 
━━━┷━━━━━━━━━━━
```

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

And then proceed to interact with the plugin, as shown above.

## Logging

Logs are printed to `/tmp/nu_plugin_plus.log` unless you set logging=False when
you initialize the plugin.

## Build Python

You can optionally build the container, doing a regular make will build a container
with nu and the installed python modules:

```bash
make
# docker build -t vanessa/nu-plugin-plus .
```
```bash
$ docker run -it vanessa/nu-plugin-plus
root@c7235d999a44:/code# nu
/code> help plus
```

You can also make a container with a standalone binary - we use [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/operating-mode.html) to do this.

```bash
make standalone
$ docker run -it vanessa/nu-plugin-plus
```

And execution proceeds as before. We can prove that we don't need the modules anymore because
the [Dockerfile.standalone](Dockerfile.standalone) does `pip3 uninstall -y nushell` and it still works.
Why might you want to do this? It will mean that your plugin is a single file (binary) and you don't
need to rely on modules elsewhere in the system. I suspect there are other ways to compile
python into a single binary (e.g., cython) but this was the first I tried, and fairly straight forward.
If you find a different or better way, please contribute to this code base!
