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
