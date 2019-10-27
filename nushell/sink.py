
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from nushell.plugin import PluginBase

import fileinput
import json


class SinkPlugin(PluginBase):
    '''A sink plugin is identified by is_filter set to false in the
       configuration, and interacts with nushell by way of nushell
       asking for the configuration upon discovery on the path (method "config")
       and then passing a temporary file as argument (method "sink")
    '''
    is_filter = False
    parse_pipe = True

    def get_sink_params(self, input_params):
        '''The input params (under ["params"] is a list, with the first entry
           being the args dictionary (that we pass to self.parse_params) and
           the remaining being entries that are passed if the sink is used as 
           a pipe. If not, it looks like an empty list, like below:

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

        # Args are always the first entry
        args = input_params.pop(0)
        params = self.parse_params(args)

        # The pipe entries are the rest (pass as _pipe)
        params["_pipe"] = self._parse_pipe(input_params)
        return params


    def _parse_pipe(self, pipeList):
        '''parse the list of piped input, typically this means string that
           have come from the terminal. To disable this, set the client
           parse_pipe to False.

           Parameters
           ==========
           pipeList: is the second index of the "params" dict from the request
        '''
        # No pipe will produce empty list
        if not pipeList or not self.parse_pipe:
            return pipeList

        pipeList = pipeList.pop(0)
        return self.parse_primitives(pipeList)


    def test(self, sinkFunc, line):
        '''test is akin to run, but instead of printing a result for the user,
           we return to the calling function. A line to parse is also required.
           since it's coming from Python, we also assume that we don't need to
           json.loads() the line from a string (it's a dictionary)
        '''
        method = line.get("method")

        # Case 1: Nu is asking for the config to discover the plugin
        if method == "config":
            plugin_config = self.get_config()
            return self.get_good_response(plugin_config)
            
        # Case 3: A filter must return the item filtered with a tag
        elif method == "sink":

            # Parse parameters for the calling sink, _pipe included
            params = self.get_sink_params(line['params'])

            # The only case of not running is if the user asks for help
            if params.get('help', False):
                return self.get_help()

            # Run the sink, and provide the user with plugin and params
            return sinkFunc(self, params)


    def run(self, sinkFunc):
        '''the main run function is required to take a user sinkFunc.
        '''
        for line in fileinput.input():

            x = json.loads(line)
            method = x.get("method")

            # Keep log of requests from nu
            self.logger.info("REQUEST %s" % line)
            self.logger.info("METHOD %s" % method)

            # Case 1: Nu is asking for the config to discover the plugin
            if method == "config":
                plugin_config = self.get_config()
                self.logger.info("plugin-config: %s" % json.dumps(plugin_config))
                self.print_good_response(plugin_config)
                break

            # Case 2: A sink passes execution to the sink function
            elif method == "sink":

                # Parse parameters for the calling sink, _pipe included
                params = self.get_sink_params(x['params'])
                self.logger.info("PARAMS %s" % params)

                # The only case of not running is if the user asks for help
                if params.get('help', False):
                    print(self.get_help())

                # Run the sink, and provide the user with plugin and params
                else:
                    sinkFunc(self, params)
                break
