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
from ctypes import c_void_p, c_wchar_p
from gettext import gettext as _

from colorama import init, Fore, Style
from io import BytesIO
from lxml import etree
from pathlib import Path
from wand import image as wand_img
from wand.api import library

# -----------------------------------------------------------------------------
# Initialize colorama.
# -----------------------------------------------------------------------------
from composer_core.composer.common import CompositionItem
from models.template import Template
from ui.common import GenerationOptions

init()

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
NS = {
    'svg': 'http://www.w3.org/2000/svg',
    'xlink': 'http://www.w3.org/1999/xlink',
}

# -----------------------------------------------------------------------------
# Some wand settings.
# -----------------------------------------------------------------------------
library.MagickSetOption.argtypes = [c_void_p,  # MagickWand * wand
                                    c_wchar_p,  # const char * option
                                    c_wchar_p]  # const char * value

logger = logging.getLogger('vf_productcreate')

xml_tree_memoization = {}
image_memoization = {}


def compose(
        items: [CompositionItem], template: Template, options: GenerationOptions,
        output: Path, verbose=False) -> Path:
    """
    Compose images from combinations of a set of images and a template.

    :param options: A named tuple containing several configurable options for rendering.
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

        svg_image = (svg.xpath('.//svg:image[@id="{}"]'.format(item.layer.image_id), namespaces=NS))

        if len(svg_image) == 0:
            message = _(
                "Error parsing layer, check that the image and layer "
                "ids are as expected."
            )
            logger.error(message)

        svg_image[0].attrib['{http://www.w3.org/1999/xlink}href'] = \
            "data:image/{};base64,{}".format(os.path.splitext(item.image_path)[1][1:], str(encoded_string)[1:])

        svg_image[0].attrib['style'] = "overflow:visible;opacity:100;"

    output_file_path = output
    svg_file_name = str(output_file_path).replace(output_file_path.suffix, '.svg')

    with open(svg_file_name, 'wb') as svg_file:

        try:
            svg.write(svg_file)
        except etree.SerialisationError as err:
            if verbose:
                logger.exception(Fore.RED + err)
                logger.exception(Style.RESET_ALL)
            else:
                logger.error(Fore.RED + "Error generating: " +
                             Fore.CYAN + "{}".format(svg_temp_name))

        # Convert svg to wepb

        image_resolution = 512
        with wand_img.Image(filename=svg_file.name, resolution=image_resolution) as image:

            library.MagickSetOption(image.wand, 'webp:lossless', 'true')
            library.MagickSetOption(image.wand, 'webp:alpha-quality', '100')
            library.MagickSetOption(image.wand, 'webp:emulate-jpeg-size', 'true')
            library.MagickSetOption(image.wand, 'webp:method', '6')

            image.compression_quality = 99
            image.adaptive_resize(1500, 1500)

            if options.unsharp:
                image.unsharp_mask(radius=0, sigma=1, amount=1, threshold=0)
                image.adaptive_sharpen(0.5, 2.5)

            if options.override_images and output_file_path.exists():
                output_file_path.unlink()

            image.save(filename=str(output_file_path))

            return Path(output_file_path)
