
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from nushell.logger import NushellLogger

import json
import os
import sys
import tempfile


class PluginBase:
    '''a PluginBase includes a name, usage, and is the base class for both
       a sink and filter plugin
    '''
    def __init__(self, name, usage, 
                 logging=True, add_help=True, parse_params=True):

        '''Set the name and usage to generate the configuration

           Parameters
           ==========
           name: the name provided by the user
           usage: the plugin usage, should be one line
           logging: if True, will output logfile to /tmp/nu_plugin_<name>.log
           add_help: if True, adds a custom --help command (unless defined)
           parse_params: extract values from "args" (don't return raw)
        '''
        self.name = self._clean_name(name)
        self.usage = usage
        self.positional = []
        self._positional = [] # list of names
        self.rest_positional = None
        self.named = {}
        self.argUsage = {}
        self.logger = self.get_logger(logging)
        self.add_help = add_help
        self._parse_params = parse_params

# Arguments

    def _check_argument(self, name, argType, syntaxShape):
        '''check an argument (named or positional) to ensure that the name
           is lowercase without spaces, and the syntaxShape is valid
           return the cleaned values.
        '''
        name = self._clean_name(name)
        argType = self._camel_case(argType)

        # If syntaxShape provided, ensure is valid (warn user if not)
        if syntaxShape:
            syntaxShape = self._get_syntax_shape(syntaxShape)

        # Return the parse argument
        arg = {"name": name,
               "type": argType,
               "shape": syntaxShape}

        return arg


    def add_positional_argument(self, name, argType, syntaxShape=None, usage=None):
        '''a positional argument doesn't require a flag, but is provided
           based on a positional index
        '''
        # includes name, type, shape
        arg = self._check_argument(name, argType, syntaxShape)

        # Syntax shape must be provided for Optional/Mandatory
        if arg['type'] not in ["Optional", "Mandatory"]:
            self.logger.exit("positional type can only be Optional/Mandatory")

        # Mandatory can have no syntax shape, Any or Block
        if not arg['shape']:
            self.positional.append({arg["type"]: [arg["name"]]})
        else:
            self.positional.append({arg["type"]: [arg["name"], arg["shape"]]})

        # Add to list of names, we use this to add to --help
        self._positional.append(arg['name'])

        # Add the usage, if defined
        if usage is not None:
            self.argUsage[arg['name']] = usage

        self.logger.debug("Updated positional arguments %s" % self._positional)


    def add_named_argument(self, name, argType, syntaxShape=None, usage=None):
        '''adding a named argument comes down to one of:
           Switch: akin to a boolean, doesn't require a SyntaxShape
           Optional: an optional argument (requires Syntax Shape)
           Mandatory: required! (also requires a SyntaxShape)

           Parameters
           ==========
           name: the name of the argument, should be lowercase without spaces
           argType: the arg type, must be one of Switch, Optional, Mandatory 
           syntaxShape: if not Switch, must provide syntaxShape.
           usage: if provided, is added to argUsage for custom --help
        '''
        # Syntax shape must be provided for Optional/Mandatory
        if argType in ["Optional", "Mandatory"] and not syntaxShape:
            self.logger.exit("SyntaxShape is required for Optional/Mandatory")

        # includes name, type, shape
        arg = self._check_argument(name, argType, syntaxShape)

        if arg['type'] == "Switch":
            self.named[arg['name']] = "Switch"
        elif arg['type'] in ["Optional", "Mandatory"]:
            self.named[arg['name']] = {arg['type']: arg['shape']}

        # Add usage, if provided
        if usage:
            self.argUsage[arg['name']] = usage

        self.logger.debug("Updated named arguments %s" % self.named)


    def _get_syntax_shape(self, shape):
        '''return a valid syntax shape, warn the user if the provided type 
           is not found at see src/parser/hir/syntax_shape.rs
           at https://github.com/nushell/nushell
        '''
        shape = self._camel_case(shape)
        shapes = ["Any", "List", "String", "Member", "ColumnPath", 
                  "Number", "Int", "Path", "Pattern", "Block"]

        if shape not in shapes:
            self.logger.warning("%s is not a valid SyntaxShape" % shape)
            return "String"
        return shape


# Print / Logging

    def get_logger(self, logging):
        '''if logging is not enabled, set to quiet.
        '''
        logname = "nu_plugin_%s.log" % self.name
        logfile = os.path.join(tempfile.gettempdir(), logname)
        if not logging:
            return NushellLogger(logfile, level=0)
        return NushellLogger(logfile)


    def get_good_response(self, response):
        '''generate a good response. Confirming to jsonprc 2.0, we include a 
           method "response" and params that should be a dict with key "Ok" and 
           value as a config, an empty list (begin or end filter) or a list
           of dict responses (for a filter)
        '''
        json_response = {
            "jsonrpc": "2.0",
            "method": "response",
            "params": {"Ok": response}
        }
        return json_response


    def print_good_response(self, response):
        '''generate and print a good response.
        '''
        json_response = self.get_good_response(response)
        self.logger.info("Printing response %s" % response)
        print(json.dumps(json_response))
        sys.stdout.flush()


# Configuration

 
    def get_config(self):
        '''return configuration object, is_filter must be defined by subclass
           note that get_config is the first call to any kind of plugin,
           so here is where we add a help argument if it's not added.
        '''
        # If help not in named, add it.
        if "help" not in self.named and self.add_help:
            self.named['help'] = "Switch"
            self.argUsage['help'] = "show this usage"

        return {
            "name": self.name,
            "usage": self.usage,
            "positional": self.positional,
            "rest_positional": self.rest_positional,
            "named": self.named,
            "is_filter": self.is_filter}


# Parsing, Help and Tags

    def parse_primitives(self, listing):
        '''given a listing of primitives (e.g., a pipelist from _parse_pipe
           or positional arguments from parse_params) return the content
           of the primitive, regardless of type. Input should look like:
   
            [{"tag":
               {"anchor":null,"span":{"start":5,"end":6}},
               "item":{"Primitive":{"Int":1}}}..]
        '''
        # In case None
        listing = listing or []

        # Return list of values as the pipe content
        entries = []

        # Each entry has a tag and item. We want the Primitive (type)
        for entry in listing:
            item = entry['item'].get('Primitive')
            entries = entries + list(item.values())

        return entries


    def getTag(self):
        '''for local testing without Nu, we provide a function to return
           a dummy tag
        '''
        return {"anchor":None, "span":{"end":0, "start":0}}


    def parse_params(self, input_params):
        '''parse the parameters into an easier to parse object. An example looks 
           like the following. For a sink - this is the first item in a list
           under params. For a filter, it's a dict directly under params.

          {'args': {'positional': None,
	     'named': {'switch': {'tag': {'anchor': None,
	        'span': {'start': 58, 'end': 64}},
	       'item': {'Primitive': {'Boolean': True}}},
	      'mandatory': {'tag': {'anchor': None, 'span': {'start': 20, 'end': 32}},
	       'item': {'Primitive': {'String': 'MANDATORYARG'}}},
	      'optional': {'tag': {'anchor': None, 'span': {'start': 44, 'end': 55}},
	       'item': {'Primitive': {'String': 'OPTIONALARG'}}}}},
	    'name_tag': {'anchor': None, 'span': {'start': 0, 'end': 7}}},
        '''
        if not input_params:
            return input_params 

        if "args" not in input_params:
            return input_params

        # Does the plugin want to skip parsing params?
        if not self._parse_params:
            return input_params

        positional = input_params['args'].get('positional', [])
        named = input_params['args'].get('named', {})

        # We will return lookup dictionary of params
        params = {}

        # Keep a simple dictionary with values we know types for
        for name, values in named.items():

            # is it a String? Boolean?
            value_type = list(values['item']['Primitive'].keys())[0]

            if value_type == "String":
                params[name] = values['item']['Primitive']['String']

            elif value_type == "Boolean":
                params[name] = values['item']['Primitive']['Boolean']

            # If you use other types, add them here
            else:
                self.logger.info("Invalid paramater type %s:%s" %(name, values))

        # Add positional arguments
        params["_positional"] = self.parse_primitives(positional)
        return params        


    def get_help(self):
        '''based on the named and positional arguments, we provide a usage
           string that can be used for a custom <name> --help function.
        '''
        args = ""

        # Positional arguments
        if self._positional:
            for name in self._positional:

                argString = "%s %s" %(name, name.upper())

                spaces = 19 - len(argString)
                args = args + argString + " "*spaces

                # If a usage is defined
                if self.argUsage.get(name) is not None:
                    args += " %s" % self.argUsage.get(name)
                args += "\n"                    

        # Named arguments
        for name, argType in self.named.items():

            # If it's a mandatory or optional
            if isinstance(argType, dict):
                argString = "--%s %s" %(name, name.upper())
            else:
                argString = "--%s" % name         

            # Ensure nice spacing (might need to adjust)
            spaces = 19 - len(argString)
            args = args + argString + " "*spaces
            
            # If a usage is defined
            if self.argUsage.get(name) is not None:
                args += " %s" % self.argUsage.get(name)
            args += "\n"                    

        return "%s: %s\n\n%s\n" %(self.name, self.usage, args)


# Helpers

    def _clean_name(self, name):
        '''the name must be all lowercase, and with no spaces.

           Parameters
           ==========
           name: the name provided by the user
        '''
        return name.replace(' ', '-').lower()


    def _camel_case(self, name):
        '''nushell uses camel case (or all lowercase with capital letters)
        '''
        return name.lower().capitalize()
