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

USER_FOLDER = os.environ.get('VF_CONFIG_DIR', False) or os.path.expanduser('~')
CONF_DIR = os.path.join(USER_FOLDER, '.composer/')
CONFIG_FILE = os.path.join(USER_FOLDER, '.composer/composer.cfg')

config = configparser.ConfigParser()

if not os.path.exists(CONFIG_FILE):
    config.add_section('composer')
    config.set('composer', 'main_product_code_pattern', '.*')
    config.set('composer', 'presentation_code_pattern', '.*')
    config.set('composer', 'secondary_product_code_pattern', '.*')
    config.set('composer', 'num_threads', '5')
    config.set('composer', 'output_geometry', '568x568')
    config.set('composer', 'adaptive_resize_width', '1500')
    config.set('composer', 'adaptive_resize_height', '1500')
    config.set('composer', 'unsharp', "True")
    config.set('composer', 'override_target_files', "True")
    config.set('composer', 'output_path', ".")
    config.set('composer', 'output_path', 'output')

    config.set('composer', 'main_products_path', 'main_products')
    config.set('composer', 'secondary_products_path', 'secondary_products')
    config.set('composer', 'presentations_path', 'presentations')
    config.set('composer', 'backgrounds_path', 'backgrounds')

    if not os.path.exists(CONF_DIR):
        os.mkdir(CONF_DIR)

    with open(CONFIG_FILE, 'w') as file_cfg:
        config.write(file_cfg)

config.read(CONFIG_FILE)


class ConfigHelper(object):

    def __init__(self, config_object):
        self.__config = config_object

        self.get_config = partial(self.__config.get, 'composer')
        self.get_config_boolean = partial(self.__config.getboolean,
                                          'composer')
        self.get_config_int = partial(self.__config.getint, 'composer')
        self.set_config_value = partial(self.__config.set, 'composer')

    def save(self):
        with open(CONFIG_FILE, 'w') as config_file:
            self.__config.write(config_file)

    @property
    def s3_access_key(self):
        return self.get_config('s3_access_key')

    @property
    def s3_secret_key(self):
        return self.get_config('s3_secret_key')

    @property
    def main_products_path(self):
        return self.get_config('main_products_path')

    @property
    def main_product_code_pattern(self):
        return self.get_config('main_product_code_pattern')

    @property
    def backgrounds_path(self):
        return self.get_config('backgrounds_path')

    @property
    def background_code_pattern(self):
        return self.get_config('background_code_pattern')

    @property
    def secondary_products_path(self):
        return self.get_config('secondary_products_path')

    @property
    def secondary_product_code_pattern(self):
        return self.get_config('secondary_product_code_pattern')

    @property
    def adaptive_resize_width(self):
        return self.get_config_int('adaptive_resize_width')

    @property
    def adaptive_resize_height(self):
        return self.get_config_int('adaptive_resize_height')

    @property
    def unsharp(self):
        return self.get_config_boolean('unsharp')

    @property
    def num_threads(self):
        return self.get_config_int('num_threads')

    @property
    def override_target_files(self):
        return self.get_config_boolean('override_target_files')

    @property
    def output_path(self):
        return self.get_config('output_path')

    @property
    def presentations_path(self):
        return self.get_config('presentations_path')

    @property
    def backgrounds_path(self):
        return self.get_config('backgrounds_path')

    @property
    def inner_config_obj(self):
        return self.__config


settings = ConfigHelper(config)
