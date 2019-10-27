#!/usr/bin/python

# Copyright (C) 2019-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

def assert_good_response(response):
    '''ensure that a response is good, meaning jsonrpc 2.0 and method response
    '''
    for key in ['jsonrpc', 'method', 'params']:
        assert key in response

    assert isinstance(response['params'], (dict, list))
    assert response['method'] == 'response'


def check_plugin_config(plugin, plugin_name, usage, is_filter):
    '''a helper function to test a general plugin configuration
    '''
 
    # Before adding args or getting help, we don't have any parameters
    assert not plugin.argUsage
    assert not plugin.positional
    assert not plugin._positional
    assert not plugin.named

    # Help shouldn't be in current help
    assert "--help" not in plugin.get_help()

    # Once we generate a config (like the first call) we should have help
    plugin_config = plugin.get_config()
    assert "help" in plugin.named

    for key in ['name', 'usage', 'positional', 'rest_positional', 'named', 'is_filter']:
        assert key in plugin_config

    assert plugin_config["is_filter"] == is_filter
    assert plugin_config["usage"] == usage
    assert plugin_config["name"] == plugin_name
    assert plugin.name == plugin_name
    assert plugin.usage == usage

    # The name and usage should be included, and now --help is added too
    for contender in [usage, plugin_name, '--help', 'show this usage']:
        assert contender in plugin.get_help()

def check_remove_help(plugin, plugin_name, usage, is_filter):
    '''similar checks, but remove the help parameters
    '''
    # But if we requested to not add help, shouldn't be there
    plugin_config = plugin.get_config()
    assert "help" not in plugin.named
    assert "--help" not in plugin.get_help()

    # Now add named arguments
    plugin.add_named_argument("greet", "Switch", usage="say hello")
    assert "greet" in plugin.argUsage
    assert "greet" in plugin.named

    # The user can optionally just give a name (a positional argument)
    plugin.add_positional_argument("avatar", "Optional", "String")
    assert "avatar" in plugin._positional
    assert plugin.positional # len > 0
