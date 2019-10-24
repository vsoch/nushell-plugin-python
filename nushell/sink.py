
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from nushell.plugin import PluginBase

import fileinput
import json
import sys


class SinkPlugin(PluginBase):
    '''A sink plugin is identified by is_filter set to false in the
       configuration, and interacts with nushell by way of nushell
       asking for the configuration upon discovery on the path (method "config")
       and then passing a temporary file as argument (method "sink")
    '''
    is_filter = False

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

            # Case 3: A filter must return the item filtered with a tag
            elif method == "sink":

                # Parse parameters for the calling sink
                params = self.parse_params(x['params'])
                self.logger.info("PARAMS %s" % params)

                # The only case of not running is if the user asks for help
                if params.get('help', False):
                    print(self.get_help())

                # Run the sink, and provide the user with plugin and params
                else:
                    sinkFunc(self, params)
                break
