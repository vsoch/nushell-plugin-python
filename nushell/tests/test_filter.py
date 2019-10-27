#!/usr/bin/python

# Copyright (C) 2019-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from nushell.filter import FilterPlugin
from .helpers import (
    assert_good_response,
    check_plugin_config,
    check_remove_help
)
from .plugin_requests import (
    config_request,
    filter_begin_request,
    filter_end_request,
    filter_string_request,
    filter_int_request,
    filter_custom_request
)

import os
import pytest


def func(plugin, params):
    '''func will be executed by the calling FilterPlugin when method is "filter"
       instead of printing responses, we return them to the caller for testing
    '''
    return params


def test_filter_plugin(tmp_path):
    '''test creation of a simple sink plugin
    '''
    plugin_name = "filter"
    usage = "A dummy filter plugin to print to the terminal"
    plugin = FilterPlugin(name=plugin_name, usage=usage, logging=False)

    # Before config, we haven't cached any params
    for attr in ['params', 'args']:
        assert not getattr(plugin, attr, None)

    # Test request for config
    response = plugin.test(func, config_request)
    assert_good_response(response)
    assert plugin.get_config() == response['params']['Ok']

    # After config, we have empty params / args
    for attr in ['params', 'args']:
        assert getattr(plugin, attr) in [[], {}]

    # Check begin_filter
    response = plugin.test(func, filter_begin_request)
    assert_good_response(response)
    assert response['params'] == {'Ok': []}

    # Now params should be populated
    assert 'args' in plugin.params
    assert 'help' in plugin.args and '_positional' in plugin.args

    # Testing the filter method with string request
    response = plugin.test(func, filter_string_request)
    assert plugin.get_string_primitive() == 'pancakes'

    # Filters differ from sinks in tha they don't return _pipe
    for key in ['help', '_positional']:
        assert key in response

    # Testing the filter method with int request
    response = plugin.test(func, filter_int_request)
    assert plugin.get_int_primitive() == 'imanumber'

    # Testing the filter method with custom request
    response = plugin.test(func, filter_custom_request)
    assert plugin.get_primitive("Any") == 'imathing'

    # Test end_filter request     
    response = plugin.test(func, filter_end_request)
 


def test_filter_config(tmp_path):
    '''test configure of a simple sink plugin
    '''
    plugin_name = "filter"
    usage = "A dummy filter plugin to print to the terminal"
    plugin = FilterPlugin(name=plugin_name, usage=usage, logging=False)
    check_plugin_config(plugin, plugin_name, usage, is_filter=True)

    # Test without adding help
    plugin = FilterPlugin(name=plugin_name, usage=usage, logging=False, add_help=False)
    check_remove_help(plugin, plugin_name, usage, is_filter=True)
