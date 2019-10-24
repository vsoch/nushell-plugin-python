# Nu Plugin Hello

A simple hello example for using nushell in Python to create a plugin!

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

Ask for help

```
> help hello
A friendly plugin

Usage:
  > hello {flags} 

flags:
  --excited
  --name <String>
  --help
```

There is also a custom `--help` function provided by the library that also adds argument usage

```bash
> hello --help
hello: A friendly plugin
--excited           add an exclamation point!
--name NAME         say hello to...
--help              show this usage
```

Say hello.
```bash
> hello
Hello
```

Say hello to someone

```bash
> hello --name dinosaur
Hello dinosaur
```

Be excited!
> hello --name dinosaur --excited
Hello dinosaur!
```

## Bulid Containers

You can build a container with nushell and the python module (as it is in the repository)

```bash
make
docker build -t vanessa/nu-plugin-hello .
# nu
/code> help hello
A friendly plugin

Usage:
  > hello {flags} 

flags:
  --excited
  --name <String>
  --help
```

or as a standalone binary:

```bash
make standalone
docker build -f Dockerfile.standalone -t vanessa/nu-plugin-hello .
```

And execution proceeds as before. We can prove that we don't need the modules anymore because
the [Dockerfile.standalone](Dockerfile.standalone) does `pip3 uninstall -y nushell` and it still works.
Why might you want to do this? It will mean that your plugin is a single file (binary) and you don't
need to rely on modules elsewhere in the system. I suspect there are other ways to compile
python into a single binary (e.g., cython) but this was the first I tried, and fairly straight forward.
If you find a different or better way, please contribute to this code base!
