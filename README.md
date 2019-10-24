# Nushell Plugin Python

[![PyPI version](https://badge.fury.io/py/nushell.svg)](https://badge.fury.io/py/nushell)

This is a python module to allow for easy creation of plugins. It's
already fairly easy, but this can improve upon that! Each of the examples provided comes with:

 - the full example in a python file (without the .py extension)
 - containers with nushell to run with regular Python or (for some) a standalone binary (via pyinstaller)
 - README.md files to walk through the usage

Quick start examples for a filter and sink plugin are included below, and you
should see the [examples](examples) folder for the complete code, makefiles, and Dockerfiles.
Please contribute new examples along with tweaks to the code! I developed this in
under a day, so we can likely make it much better, and will need to as nushell
is developed.

## Filter Plugin

A basic filter plugin will instantiate the `FilterPlugin` class, and then
provide a function to run for the filter.

```python
#!/usr/bin/env python3

from nushell.filter import FilterPlugin

# Your filter function will be called by the FilterPlugin, and should
# accept the plugin and the dictionary of params
def runFilter(plugin, params):
    '''runFilter will be executed by the calling SinkPlugin when method is "sink"
    '''
    # Get the string primitive passed by the user
    value = plugin.get_string_primitive()

    # Calculate the length
    intLength = len(value)

    # Print an integer response (can also be print_string_response)
    plugin.print_int_response(intLength)


# The main function is where you create your plugin and run it.
def main():

    # Initialize a new plugin
    plugin = FilterPlugin(name="len", 
                          usage="Return the length of a string")


    # Run the plugin by passing your filter function
    plugin.run(runFilter)


if __name__ == '__main__':
    main()
```

Notably, your filter function should taken a plugin and parsed command line
parameters (dictionary) as arguments. You can use the plugin to perform
several needed functions to send responses back to nushell, or log to `/tmp/nushell-plugin-<name>.log`:

```python
plugin.logger.<level>
plugin.get_string_primitive()
plugin.get_int_primitive()
plugin.print_int_response()
plugin.print_string_response()
```

### Examples

 - [len](examples/len) is a basic function to return the length of a string


## Sink Plugin

A sink plugin will instantiate the `SinkPlugin` class, and then hand off
stdin (via a temporary file) to a sink function that you write.
Here is a dummy example.

```python
#!/usr/bin/env python3

from nushell.sink import SinkPlugin

# Your sink function will be called by the sink Plugin, and should
# accept the plugin and the dictionary of params
def sink(plugin, params):
    '''sink will be executed by the calling SinkPlugin when method is "sink"
    '''
    message = "Hello"
    excited = params.get("excited", False)
    name = params.get("name", "")
    
    # If we have a name, add to message
    message = "%s %s" %(message, name)
    
    # Are we excited?
    if excited:
        message += "!"

    print(message)


# The main function is where you create your plugin and run it.
def main():

    # Initialize a new plugin
    plugin = SinkPlugin(name="hello", 
                        usage="A friendly plugin")


    # Add named arguments (notice we check for in params in sink function)
    # add_named_argument(name, argType, syntaxShape=None, usage=None)
    plugin.add_named_argument("excited", "Switch", usage="add an exclamation point!")
    plugin.add_named_argument("name", "Optional", "String", usage="say hello to...")

    # Run the plugin by passing your sink function
    plugin.run(sink)


if __name__ == '__main__':
    main()
```


### Examples

 - [pokemon](examples/pokemon) ascii pokemon on demand!
 - [hello](examples/hello) say hello using a sink!

## Single Binary

In that you are able to compile your module with [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/operating-mode.html) (e.g., see [examples/len](examples/len)) you can build your python script as a simple binary, and one that doesn't even need nushell installed as a module anymore. Why might you want to do this? It will mean that your plugin is a single file (binary) and you don't need to rely on modules elsewhere in the system. I suspect there are other ways to compile
python into a single binary (e.g., cython) but this was the first I tried, and fairly straight forward.
If you find a different or better way, please contribute to this code base!

**Important** I've found that modules with added data files don't do well (an example is [pokemon](examples/pokemon) here!)
and that's why we can't uninstall pokemon or nushell. However, I think you would have luck with most text based,
simple modules. And of course, you don't have to do this! It's totally ok to keep your Python modules
installed alongside nushell, and used when your plugin is executed.

## License

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).

## Help and Contribution

Please contribute to the package, or post feedback and questions as <a href="https://github.com/vsoch/nushell-plugin-python/issues" target="_blank">issues</a>.
