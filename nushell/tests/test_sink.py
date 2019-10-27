#!/usr/bin/python

# Copyright (C) 2019-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from nushell.sink import SinkPlugin
from .helpers import (
    assert_good_response,
    check_plugin_config,
    check_remove_help
)
from .plugin_requests import (
    config_request,
    sink_named_request,
    sink_help_request
)

import os
import pytest


def sink(plugin, params):
    '''sink will be executed by the calling SinkPlugin when method is "sink"
       instead of just printing, we return params to test
    '''
    return params


def test_sink_name(tmp_path):
    '''ensure that a plugin's name is made all lowercase, with spaces removed
       note that the user is allowed to use special characters.
    '''
    # Name must be made all lowercase
    plugin_name = "sink"
    usage = "A dummy sink plugin to print to the terminal"
    plugin = SinkPlugin(name=plugin_name, usage=usage, logging=False)

    assert plugin._clean_name("a a a") == "a-a-a"
    assert plugin._clean_name("SINK") == "sink"

def test_sink_plugin(tmp_path):
    '''test creation of a simple sink plugin
    '''
    plugin_name = "sink"
    usage = "A dummy sink plugin to print to the terminal"
    plugin = SinkPlugin(name=plugin_name, usage=usage, logging=False)

    # Test request for config
    response = plugin.test(sink, config_request)
    assert_good_response(response)
    assert plugin.get_config() == response['params']['Ok']

    # Test help request (should return help)
    response = plugin.test(sink, sink_help_request)
    assert plugin.name in response and plugin.usage in response
 
    # Test "sink" named arg request (should return params from sink())
    # {'sink': True, '_positional': [], '_pipe': []}
    response = plugin.test(sink, sink_named_request)
    for key in ['sink', '_positional', "_pipe"]:
        assert key in response

    
def test_sink_config(tmp_path):
    '''test configure of a simple sink plugin
    '''
    plugin_name = "sink"
    usage = "A dummy sink plugin to print to the terminal"
    plugin = SinkPlugin(name=plugin_name, usage=usage, logging=False)
    check_plugin_config(plugin, plugin_name, usage, is_filter=False)

    # Test without adding help
    plugin = SinkPlugin(name=plugin_name, usage=usage, logging=False, add_help=False)
    check_remove_help(plugin, plugin_name, usage, is_filter=False)
