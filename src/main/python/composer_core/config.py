"""
Copyright (2017) Raydel Miranda 

This file is part of "Villa Flores product creator".

    "Villa Flores product creator" is free software: you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    "Villa Flores product creator" is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
    Public License for more details.

    You should have received a copy of the GNU General Public License along
    with "Villa Flores product creator".  If not,
    see <http://www.gnu.org/licenses/>. """

import configparser
import os
from functools import partial
from itertools import groupby

USER_FOLDER = os.environ.get('VF_CONFIG_DIR', False) or os.path.expanduser('~')
CONF_DIR = os.path.join(USER_FOLDER, '.vf_suite/')
CONFIG_FILE = os.path.join(USER_FOLDER, '.vf_suite/vfconf.cfg')

config = configparser.ConfigParser()

if not os.path.exists(CONFIG_FILE):
    config.add_section('product_creator')
    config.set('product_creator', 'flower_code_pattern', '.*')
    config.set('product_creator', 'background_code_pattern', '.*')
    config.set('product_creator', 'bundles_code_pattern', '.*')
    config.set('product_creator', 'num_threads', '5')
    config.set('product_creator', 'bundles_number', '3')
    config.set('product_creator', 'flower_layer_id', 'clipping-flower-image')
    config.set('product_creator', 'output_geometry', '568x568')
    config.set('product_creator', 'adaptive_resize', '1500x')
    config.set('product_creator', 'unsharp', '0x1')

    if not os.path.exists(CONF_DIR):
        os.mkdir(CONF_DIR)

    with open(CONFIG_FILE, 'w') as file_cfg:
        config.write(file_cfg)

config.read(CONFIG_FILE)


class ConfigHelper(object):

    def __init__(self, config_object):
        self.__config = config_object

        self.get_config = partial(self.__config.get, 'product_creator')
        self.get_config_boolean = partial(self.__config.getboolean,
                                          'product_creator')
        self.get_config_int = partial(self.__config.getint, 'product_creator')

    @property
    def flower_layer_id(self):
        return self.get_config('flower_layer_id')

    @property
    def bundle_layers(self):
        return self.get_config('bundles_layers_id').rsplit()

    @property
    def flowers_folder(self):
        return self.get_config('flowers_folder')

    @property
    def flower_code_pattern(self):
        return self.get_config('flower_code_pattern')

    @property
    def backgrounds_folder(self):
        return self.get_config('backgrounds_folder')

    @property
    def background_code_pattern(self):
        return self.get_config('background_code_pattern')

    @property
    def bundles_folder(self):
        return self.get_config('bundles_folder')

    @property
    def bundles_code_pattern(self):
        return self.get_config('bundles_code_pattern')

    @property
    def bundles_number(self):
        return self.get_config_int('bundles_number')

    @property
    def output_geometry(self):
        return self.get_config('output_geometry')

    @property
    def adaptive_resize(self):
        return self.get_config('adaptive_resize')

    @property
    def unsharp(self):
        return self.get_config('unsharp')

    @property
    def bundle_layer_selection(self):
        params = self.get_config('layer_bundle_selection').rsplit()
        result = {}
        last_key = None
        for k, g in groupby(params):
            if k not in self.bundle_layers:
                result.update({k: []})
                last_key = k
            else:
                result[last_key].extend(list(g))
        return result

    @property
    def num_threads(self):
        return self.get_config_int('num_threads')


settings = ConfigHelper(config)
