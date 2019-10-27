
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from nushell.plugin import PluginBase

import copy
import fileinput
import json


class FilterPlugin(PluginBase):
    '''A filter plugin is identified by is_filter set to true in the
       configuration, and interacts with nushell by way of nushell
       asking for the configuration upon discovery on the path (method "config")
       and then returning responses to begin_filter, end_filter, and filter.
    '''
    args = {}
    params = {}
    is_filter = True

    # Filter functions work by way of getting primities from the input item

    def get_string_primitive(self):
        return self.get_primitive("String")

    def get_int_primitive(self):
        return self.get_primitive("Int")

    def get_primitive(self, primitive_type=None):
        '''get a primitive from an item, expected to be of a type (String
           or Int typically). We get this from last passed params.
        '''
        if primitive_type:
            return self.params["item"]["Primitive"][primitive_type]
        else:
            return list(self.params["item"]["Primitive"].values())[0]


    def print_primitive_response(self, value, primitive_type, 
                                       return_response=False):
        '''a base function to print a good response with an updated
           value for a primitive type.
           Parameters
           ==========
           value: The primitive value, expected to match the type
           primitive_type: one of Int or String
           return_response: if True, just return (don't print)
        '''
        primitive_type = self._camel_case(primitive_type)
        item = {"Primitive": {primitive_type: value}}

        # Get the original complete passed parameters to update
        response = copy.deepcopy(self.params)
        response["item"] = item
        response = [{"Ok": {"Value": response}}]

        # For testing, we might just want to return response
        if return_response:
            return response

        self.print_good_response(response)


    def print_int_response(self, value):
        return self.print_primitive_response(value, "Int")
        
    def print_string_response(self, value):
        return self.print_primitive_response(value, "String")

    def test(self, runFilter, line):
        '''given a line, test the response
        '''
        method = line.get("method")

        # Store raw parameters for the plugin memory, only if not end filter
        if method != "end_filter":
            self.params = line.get('params', {})

        # Case 1: Nu is asking for the config to discover the plugin
        if method == "config":
            plugin_config = self.get_config()
            return self.get_good_response(plugin_config)

        elif method == "begin_filter":

            # Arguments only show up for begin_filter
            self.args = self.parse_params(self.params)
            return self.get_good_response([])

        # End filter can end the filter, OR call a custom sink function
        elif method == "end_filter":

            # If the user wants help, return the help and break
            if "help" in self.args:

                # We need to update so name_tag is tag (not logical I know)
                self.params['tag'] = self.params.get('name_tag', self.getTag())
                return self.print_primitive_response(self.get_help(), "String", True)

            return self.get_good_response([])

        # Run the filter, passing the unparsed params
        elif method == "filter":
            return runFilter(self, self.args)


    def run(self, runFilter):
        '''the main run function is required to take a user runFilter function.
        '''
        for line in fileinput.input():

            x = json.loads(line)
            method = x.get("method")

            # Keep log of requests from nu
            self.logger.info("REQUEST %s" % line)
            self.logger.info("METHOD %s" % method)

            # Store raw parameters for the plugin memory, only if not end filter
            if method != "end_filter":
                self.params = x.get('params', {})

            # Case 1: Nu is asking for the config to discover the plugin
            if method == "config":
                plugin_config = self.get_config()
                self.logger.info("plugin-config: %s" % json.dumps(plugin_config))
                self.print_good_response(plugin_config)
                break

            elif method == "begin_filter":

                # Arguments only show up for begin_filter
                self.args = self.parse_params(self.params)
                self.logger.info("Begin Filter Args: %s" % self.args)
                self.print_good_response([])

            # End filter can end the filter, OR call a custom sink function
            elif method == "end_filter":

                # If the user wants help, return the help and break
                if "help" in self.args:

                    # We need to update so name_tag is tag (not logical I know)
                    self.params['tag'] = self.params.get('name_tag', self.getTag())
                    self.logger.info("User requested --help")
                    self.print_string_response(self.get_help())
                else:
                    self.print_good_response([])
                break

            # Run the filter, passing the unparsed params
            elif method == "filter":
 
                self.logger.info("RAW PARAMS: %s" % self.params)
                runFilter(self, self.args)

            else:
                break
