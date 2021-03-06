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
    config.set('composer', 'presentation_code_pattern', '(\w+-)([\w-]+)')
    config.set('composer', 'secondary_product_code_pattern', '.*')
    config.set('composer', 'num_threads', '5')

    config.set('composer', 'output_geometry', '568x568')
    config.set('composer', 'image_resolution', '72')
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

    config.set('composer', 'upload_to_s3', 'True')
    config.set('composer', 'secondary_generation', 'False')

    config.set('composer', 'zoom_ar_x', '18')
    config.set('composer', 'zoom_ar_y', '9')
    config.set('composer', 'force_zoom_ar', 'False')

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
    def include_secondary_items(self):
        try:
            result = self.get_config_boolean('include_secondary_items')
        except configparser.NoOptionError:
            config.set('composer', 'include_secondary_items', 'True')
            self.save()
            return True
        else:
            return result

    @property
    def include_presentation_items(self):
        try:
            result = self.get_config_boolean('include_presentation_items')
        except configparser.NoOptionError:
            config.set('composer', 'include_presentation_items', 'True')
            self.save()
            return True
        else:
            return result

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
    def secondary_generation(self):
        try:
            result = self.get_config_boolean('secondary_generation')
        except configparser.NoOptionError:
            config.set('composer', 'secondary_generation', 'False')
            self.save()
            return False
        else:
            return result

    @property
    def force_zoom_ar(self):
        try:
            return self.get_config_boolean('force_zoom_ar')
        except configparser.NoOptionError:
            config.set('composer', 'force_zoom_ar', 'False')
            self.save()
            return False

    @property
    def zoom_ar_x(self):
        try:
            return self.get_config_int('zoom_ar_x')
        except configparser.NoOptionError:
            config.set('composer', 'zoom_ar_x', '18')
            self.save()
            return 18

    @property
    def zoom_ar_y(self):
        try:
            return self.get_config_int('zoom_ar_y')
        except configparser.NoOptionError:
            config.set('composer', 'zoom_ar_y', '9')
            self.save()
            return 9

    @property
    def num_threads(self):
        return self.get_config_int('num_threads')

    @property
    def override_target_files(self):
        return self.get_config_boolean('override_target_files')

    @property
    def upload_to_s3(self):
        return self.get_config_boolean('upload_to_s3')

    @property
    def output_path(self):
        return self.get_config('output_path')

    @property
    def presentations_path(self):
        return self.get_config('presentations_path')

    @property
    def presentation_code_pattern(self):
        return self.get_config('presentation_code_pattern')

    @property
    def backgrounds_path(self):
        return self.get_config('backgrounds_path')

    @property
    def inner_config_obj(self):
        return self.__config

    @property
    def bucket_name(self):
        try:
            return self.get_config('bucket_name')
        except configparser.NoOptionError as err:
            return None


settings = ConfigHelper(config)
