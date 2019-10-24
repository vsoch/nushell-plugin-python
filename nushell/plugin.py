
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from nushell.logger import NushellLogger

import fileinput
import json
import os
import sys
import tempfile


class PluginBase:
    '''a PluginBase includes a name, usage, and is the base class for both
       a sink and filter plugin
    '''
    def __init__(self, name, usage, logging=True, add_help=True):
        '''Set the name and usage to generate the configuration

           Parameters
           ==========
           name: the name provided by the user
           usage: the plugin usage, should be one line
           logging: if True, will output logfile to /tmp/nu_plugin_<name>.log
           add_help: if True, adds a custom --help command (unless defined)
        '''
        self.name = self._clean_name(name)
        self.usage = usage
        self.positional = []
        self.rest_positional = None
        self.named = {}
        self.argUsage = {}
        self.logger = self.get_logger(logging)
        self.add_help = add_help


# Arguments


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
        name = self._clean_name(name)
        argType = self._camel_case(argType)

        # Syntax shape must be provided for Optional/Mandatory
        if argType in ["Optional", "Mandatory"] and not syntaxShape:
            self.logger.exit("SyntaxShape is required for Optional/Mandatory")

        # If syntaxShape provided, ensure is valid (warn user if not)
        if syntaxShape:
            syntaxShape = self._get_syntax_shape(syntaxShape)

        if argType == "Switch":
            self.named[name] = "Switch"
        elif argType in ["Optional", "Mandatory"]:
            self.named[name] = {argType: syntaxShape}

        # Add usage, if provided
        if usage:
            self.argUsage[name] = usage

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


    def print_good_response(self, response):
        '''a good response confirms to jsonprc 2.0, we include a method "response" and
           params, which should be a dict with key "Ok" and value as the json config,
           (config) an empty list (begin_filter or end_filter) or a list of dict
           responses (filter).
        '''
        json_response = {
            "jsonrpc": "2.0",
            "method": "response",
            "params": {"Ok": response}
        }
        self.logger.info("Printing response %s" % response)
        print(json.dumps(json_response))
        sys.stdout.flush()


# Configuration

 
    def get_config(self):
        '''return configuration object, is_filter must be defined by subclass
        '''
        # If help not in named, add it.
        if "help" not in self.named and self.add_help:
            self.named['help'] = "Switch"

        return {
            "name": self.name,
            "usage": self.usage,
            "positional": self.positional,
            "rest_positional": self.rest_positional,
            "named": self.named,
            "is_filter": self.is_filter}


# Parsing, Help and Tags

    def getTag(self):
        '''for local testing without Nu, we provide a function to return
           a dummy tag
        '''
        return {"anchor":None, "span":{"end":0,"start":0}}


    def parse_params(self, input_params):
        '''parse the parameters into an easier to parse object. An example looks 
           like the following (I'm not sure why an empty list is passed as a second
           entry)

          [{'args': {'positional': None,
	     'named': {'switch': {'tag': {'anchor': None,
	        'span': {'start': 58, 'end': 64}},
	       'item': {'Primitive': {'Boolean': True}}},
	      'mandatory': {'tag': {'anchor': None, 'span': {'start': 20, 'end': 32}},
	       'item': {'Primitive': {'String': 'MANDATORYARG'}}},
	      'optional': {'tag': {'anchor': None, 'span': {'start': 44, 'end': 55}},
	       'item': {'Primitive': {'String': 'OPTIONALARG'}}}}},
	    'name_tag': {'anchor': None, 'span': {'start': 0, 'end': 7}}},
	   []]
        '''
        if not input_params:
            return input_params 

        # For some reason sink passes a list
        if isinstance(input_params, list):     
            input_params = input_params[0]

        if "args" not in input_params:
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

        return params        


    def get_help(self):
        '''based on the named and positional arguments, we provide a usage
           string that can be used for a custom <name> --help function.
        '''
        args = ""

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

        # Add help, if not already added
        if "help" not in self.named and self.add_help:
            args += "--help              show this usage\n"

        return "%s: %s\n%s\n" %(self.name, self.usage, args)


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
