"""
Copyright (2017) Raydel Miranda 

This file is part of "VillaFlores Product Creator".

    "VillaFlores Product Creator" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "VillaFlores Product Creator" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "VillaFlores Product Creator".  If not, see <http://www.gnu.org/licenses/>.
"""

import base64
import logging
import os
import tempfile
from io import BytesIO
from pathlib import Path

from colorama import init, Fore, Style
from lxml import etree

# -----------------------------------------------------------------------------
# Initialize colorama.
# -----------------------------------------------------------------------------
from composer_core.composer.common import CompositionItem
from models.template import Template

init()

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
NS = {
    'svg': 'http://www.w3.org/2000/svg',
    'xlink': 'http://www.w3.org/1999/xlink',
}

logger = logging.getLogger('vf_productcreate')

xml_tree_memoization = {}
image_memoization = {}


def compose(items: [CompositionItem], template: Template, output: Path=None, verbose=False):
    """
    Compose images from combinations of a set of images and a template.

    :param items: A list compositions items.
    :param template: The template.
    :param output:  The result image file name.
    :param verbose:  Print the process.
    :return:
    """

    svg_temp_name = None

    template_stream = BytesIO(template.render_to_str())
    svg = etree.parse(template_stream)

    for item in items:
        if not image_memoization.get(item.image_path, False):
            image_file = open(item.image_path, 'rb')
            encoded_string = base64.b64encode(image_file.read())
            image_memoization.update({item.image_path: encoded_string})

        encoded_string = image_memoization[item.image_path]

        svg_image = (svg.xpath('.//svg:image[@id="{}"]'.format(item.image_id), namespaces=NS))

        if len(svg_image) == 0:
            if verbose:
                print("Error parsing layer, check that the image and layer ids are as "
                      "expected.")
            return

        svg_image[0].attrib['{http://www.w3.org/1999/xlink}href'] = \
            "data:image/{};base64,{}".format(os.path.splitext(item.image_path)[1][1:], str(encoded_string)[1:])

        svg_image[0].attrib['style'] = "overflow:visible;opacity:100;"

    svg_temp_dir = tempfile.mktemp(dir=tempfile.gettempdir())

    if svg_temp_name is None:
        svg_temp_name = '{}.svg'.format(svg_temp_dir)
    try:
        svg.write(svg_temp_name)
    except etree.SerialisationError as err:
        if verbose:
            logger.exception(Fore.RED + err)
            logger.exception(Style.RESET_ALL)
        else:
            logger.error(Fore.RED + "Error generating: " +
                         Fore.CYAN + "{}".format(svg_temp_name))
    #     template = svg_temp_name
    #
    #     proc = subprocess.Popen(["convert", svg_temp_name,
    #                              '-adaptive-resize', settings.adaptive_resize,
    #                              '-unsharp', settings.unsharp, output],
    #                             stderr=subprocess.PIPE,
    #                             stdout=subprocess.PIPE)
    #     out, err = proc.communicate()
    #     if err != b'':
    #         logger.error(err)
    #     else:
    #         if verbose:
    #             logger.info(out)
    #
    # shutil.os.remove(svg_temp_name)
