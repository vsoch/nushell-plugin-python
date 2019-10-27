#!/usr/bin/python

# Copyright (C) 2019-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

# A config request (for sink or filter)
config_request = {"jsonrpc":"2.0", "method":"config", "params":[]}


## Sinks

# A basic sink without positional arguments
sink_named_request = {
   "jsonrpc":"2.0",
   "method":"sink",
   "params":[
      {
         "args":{
            "positional": None,
            "named":{
               "sink":{
                  "tag":{
                     "anchor": None,
                     "span":{
                        "start":10,
                        "end":14
                     }
                  },
                  "item":{
                     "Primitive":{
                        "Boolean": True
                     }
                  }
               }
            }
         },
         "name_tag":{
            "anchor": None,
            "span":{
               "start":0,
               "end":7
            }
         }
      },
      [] # empty pipe
   ]
}

# A help request changes the sink flag to help
sink_help_request = {
   "jsonrpc":"2.0",
   "method":"sink",
   "params":[
      {
         "args":{
            "positional": None,
            "named":{
               "help":{
                  "tag":{
                     "anchor": None,
                     "span":{
                        "start":10,
                        "end":14
                     }
                  },
                  "item":{
                     "Primitive":{
                        "Boolean": True
                     }
                  }
               }
            }
         },
         "name_tag":{
            "anchor": None,
            "span":{
               "start":0,
               "end":7
            }
         }
      },
      [] # empty pipe
   ]
}


## Filters

# We should save params at begin request
filter_begin_request = {
   "jsonrpc":"2.0",
   "method":"begin_filter",
   "params":{
      "args":{
         "positional": None,
         "named":{
            "help":{
               "tag":{
                  "anchor": None,
                  "span":{
                     "start":6,
                     "end":10
                  }
               },
               "item":{
                  "Primitive":{
                     "Boolean":True
                  }
               }
            }
         }
      },
      "name_tag":{
         "anchor":None,
         "span":{
            "start":0,
            "end":3
         }
      }
   }
}

filter_end_request = {"jsonrpc":"2.0", "method":"end_filter", "params":[]}

filter_string_request = {
   "jsonrpc":"2.0",
   "method":"filter",
   "params":{
      "tag":{
         "anchor": None,
         "span":{
            "start":0,
            "end":2
         }
      },
      "item":{
         "Primitive":{
            "String":"pancakes"
         }
      }
   }
}

filter_int_request = {
   "jsonrpc":"2.0",
   "method":"filter",
   "params":{
      "tag":{
         "anchor": None,
         "span":{
            "start":0,
            "end":2
         }
      },
      "item":{
         "Primitive":{
            "Int":"imanumber"
         }
      }
   }
}

# A custom primitive
filter_custom_request = {
   "jsonrpc":"2.0",
   "method":"filter",
   "params":{
      "tag":{
         "anchor": None,
         "span":{
            "start":0,
            "end":2
         }
      },
      "item":{
         "Primitive":{
            "Any":"imathing"
         }
      }
   }
}
