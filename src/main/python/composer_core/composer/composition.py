import logging
from collections import defaultdict
from ctypes import c_void_p, c_wchar_p
from gettext import gettext as _
from tempfile import TemporaryFile

from io import BytesIO

import itertools
import re
import shutil
from colorama import Fore, Style
from pathlib import Path
from typing import Generator, Callable, Union, Optional
from wand.api import library
from wand.image import Image

from composer_core.composer.common import CompositionItem
from composer_core.composer.compose import compose, CompositionRenderResult
from composer_core.config import settings
from models.template import Template, LayerType
from ui.common import GenerationOptions, PRESENTATION, BACKGROUND

logger = logging.Logger(__name__)

# -----------------------------------------------------------------------------
# Some wand settings.
# -----------------------------------------------------------------------------
library.MagickSetOption.argtypes = [c_void_p,
                                    c_wchar_p,
                                    c_wchar_p]


class CompositionError(Exception):
    pass


def revalue_zero_dimension(
        original_width: float, original_height: float, new_width: float, new_height: float
) -> float:
    """
    Given new_with or new_height being 0, this function computes what its value should be to keep
    aspect ratio.

    :return: The value new_height or new_width must have to keep aspect ratio.
    """

    assert (new_width or new_height) != 0

    if new_width == 0:
        return original_width * (new_height / original_height)
    if new_height == 0:
        return original_height * (new_width / original_width)


class ExtractingZoomError(Exception):
    pass


class Composition:
    """
    A class that represents a whole composition. This means the template plus
    any other image that fills the template slots.
    """

    def __init__(self, template: Template, items: [CompositionItem]):
        self._items = items
        self._template = template

    def render(self, options: GenerationOptions, output_path: Path = None, svg_output_path: Path = None) -> CompositionRenderResult:
        """
        Render this composition into a complete image.

        :param svg_output_path: The path to the directory where to save svg for this composition, if None, svg is saved
                                in the same directory as composition.
        :param options: Some options passed to the function that actually generates images.
        :param output_path: The directory where to save the resulting image. If not set
                            the current working directory is used.

        :return: The path of the resulting image.
        """

        composition_file_name = compute_output_name(
            self,
            presentation_code_pattern=settings.presentation_code_pattern,
            append_bg_name_as_suffix=settings.secondary_generation
        )
        output_file_name = output_path.joinpath(composition_file_name)

        result = compose(self._items, self._template, options, output=output_file_name, svg_output_path=svg_output_path)

        return result

    def _extract_zoom(self, output_dir: Path, output_file_name: str, source_image: Path) -> Path:
        """
        Extract the part of the image selected for use as zoom, this part is specified by
        the ZOOM layer in the template.

        :return: The path for the generated image.
        """
        zoom_layer = self._template.get_zoom_selection_layer()

    def extract_zoom(self, source_image: Path, options: GenerationOptions, output_path: Path) -> Union[Path, None]:
        """
        Extract the part of the image selected for use as a square image, this part is specified by
        the crop layer in the template.

        :return: The path for the generated image.
        """
        crop_layer = self._template.get_zoom_selection_layer()

        if not crop_layer:
            return

        try:
            foreground = self.extract_zoom_foreground()
            backdrop = self.extract_zoom_backdrop()
        except Exception as err:
            logger.exception(err)
            raise ExtractingZoomError

        with Image(file=backdrop) as bg:

            with Image(file=foreground) as fg:
                # Compute scale factor for.
                primary_layer = self._template.get_primary_layer()
                primary_item = self._template.get_item_for_layer(primary_layer)
                primary_item_scale_factor = primary_item.scale()

                bg.resize(
                    int(bg.width / primary_item_scale_factor),
                    int(bg.height / primary_item_scale_factor)
                )

                bg.composite(fg)

                with TemporaryFile('w+b') as temporary_svg:

                    bg.save(file=temporary_svg)
                    temporary_svg.seek(0)

                    with Image(file=temporary_svg) as image:

                        library.MagickSetOption(image.wand, 'webp:lossless', 'true')
                        library.MagickSetOption(image.wand, 'webp:alpha-quality', '100')
                        library.MagickSetOption(image.wand, 'webp:emulate-jpeg-size', 'true')
                        library.MagickSetOption(image.wand, 'webp:method', '6')

                        image.compression_quality = 99

                        new_width = settings.adaptive_resize_width
                        new_height = settings.adaptive_resize_height

                        # If just one of the size is 0, scale to keep aspect ratio.
                        if (new_height + new_width) != (new_height or new_width):
                            # Both are different from 0
                            image.adaptive_resize(columns=new_width, rows=new_height)
                        else:
                            # One of them is 0.
                            if new_height == 0:
                                factor = new_width / image.width
                            else:
                                factor = new_height / image.height

                            image.adaptive_resize(columns=int(image.width * factor), rows=int(image.height * factor))

                        if options.unsharp:
                            image.unsharp_mask(radius=0, sigma=1, amount=1, threshold=0)
                            image.adaptive_sharpen(0.5, 2.5)

                        name = source_image.name.replace(source_image.suffix, '.zoom.webp')
                        output_file_path = output_path.joinpath(name)

                        if options.override_images and output_file_path.exists():
                            output_file_path.unlink()

                        image.save(filename=str(output_file_path))

    def extract_zoom_foreground(self) -> BytesIO:

        # Get foreground image.
        with Image(filename=str(self.primary_item.image_path)) as original_image:
            # Items and layers.
            zoom_layer = self._template.get_zoom_selection_layer()

            primary_layer = self._template.get_primary_layer()
            primary_item = self._template.get_item_for_layer(primary_layer)

            # Compute coords from the original image.
            primary_item_scale_factor = primary_item.scale()

            dx = zoom_layer.pos.x - primary_layer.pos.x
            dy = zoom_layer.pos.y - primary_layer.pos.y

            dx = (0 if dx < 0 else dx) / primary_item_scale_factor
            dy = (0 if dy < 0 else dy) / primary_item_scale_factor

            bottom = dy + (zoom_layer.height / primary_item_scale_factor)
            right = dx + (zoom_layer.width / primary_item_scale_factor)

            if bottom > original_image.height:
                bottom = original_image.height

            if right > original_image.width:
                right = original_image.width

            with original_image.clone() as image:

                result = BytesIO()

                image.crop(
                    int(dx), int(dy),
                    int(right), int(bottom)
                )
                image.save(file=result)
                result.seek(0)
                return result

    def extract_zoom_backdrop(self) -> BytesIO:

        zoom_layer = self._template.get_zoom_selection_layer()

        # Get background original image.
        with Image(filename=str(self._template.background)) as original_background:
            # Scaled rect.
            pos = zoom_layer.pos
            left, top, = pos.x, pos.y
            right, bottom = pos.x + zoom_layer.width, pos.y + zoom_layer.height

            # Crop image.
            with original_background.clone() as background_clone:
                result = BytesIO()

                background_clone.crop(
                    int(left), int(top),
                    int(right), int(bottom)
                )
                background_clone.save(file=result)
                result.seek(0)
                return result

    def __str__(self):
        end_line = "\n"

        return (
            f'============ \n'
            f'Composition: \n'
            f'============ \n'
            f'{end_line.join([str(i) for i in self._items])}'
        )

    def is_valid(self):
        """
        A place where to put some conditions that states whether a composition is valid or not.
        :return: True if composition is valid, False otherwise.
        """

        # All items must be in different layers.
        layer_id_count = defaultdict(int)
        for item in self._items:
            layer_id_count[item.layer.layer_id] += 1
            # There are two different items assigned to the same svg layer.
            if layer_id_count[item.layer.layer_id] > 1:
                return False

        return True

    def filter_items(self, predicate: Callable) -> [CompositionItem]:
        items = [item for item in self._items if predicate(item)]
        return items

    @property
    def primary_item(self) -> CompositionItem:
        items = self.filter_items(lambda x: x.layer.type == LayerType.PRIMARY)
        if len(items) > 1:
            raise CompositionError(_("Found more that one primary item. It should be only one."))
        return items[0]

    @property
    def presentation_item(self) -> Optional[CompositionItem]:
        items = self.filter_items(lambda x: x.layer.type == LayerType.PRESENTATION)
        if len(items) > 1:
            raise CompositionError(_("Found more that one presentation item. It should be only one."))
        if len(items) == 0:
            return None
        return items[0]

    @property
    def secondary_items(self) -> [CompositionItem]:
        return self.filter_items(lambda x: x.layer.type == LayerType.SECONDARY)

    def save(self, options: GenerationOptions, svg_output_path: Path = None) -> Path:
        """
        Method that creates a folder structure ready for sync to s3.

        Such folder structure is as follow:

        - <product_code>
            | - <composition - code>.webp
            | - presentation.png
            | - background.png

        The root folder for such structure might exist, due a previously saved composition of
        the same product, the same might happen with the background, if that's the case,
        the results are merged.

        :param svg_output_path: The path to the directory where to save svg for this composition, if None, svg is saved
                            in the same directory as composition.
        :param options: Some options passed to the function that actually generates images.
        """

        line_products_folder_name = "LINE-PRODUCTS"
        clipping_dir = "CLIPPING"

        # Get the root folder name.
        root_dir = Path(settings.output_path)

        main_product_name = despeluze_item_name(self.primary_item)
        main_product_name = main_product_name.split('_')[0]
        main_product_dir = root_dir.joinpath(line_products_folder_name).joinpath(main_product_name)

        # Try to crete the root dir, if exists, it is ok.
        root_dir.joinpath(line_products_folder_name).mkdir(exist_ok=True)
        main_product_dir.mkdir(exist_ok=True)

        # Render composition to the desired folder. render method will also save the
        # svg file corresponding to this composition.
        result = self.render(options, main_product_dir, svg_output_path=svg_output_path)
        self.extract_zoom(result.svg_path, options, main_product_dir)

        # Save presentation
        self.save_presentation(root_dir)

        # Save background
        self.save_background(root_dir)

        # Save clipping of the product and secondary items.
        clipping_dir = self.save_clipping(clipping_dir, root_dir)
        self.save_secondary_items(clipping_dir)

        return result.filename

    def save_presentation(self, root_dir: Path):

        if not self.presentation_item:
            return

        presentation_image_path = Path(self.presentation_item.image_path)
        presentations_dir = root_dir.joinpath(PRESENTATION)
        presentations_dir.mkdir(exist_ok=True)

        presentation_parent_folder = presentation_image_path.name.replace(presentation_image_path.suffix, "")
        presentation_parent_folder = presentations_dir.joinpath(presentation_parent_folder)
        presentation_parent_folder.mkdir(exist_ok=True)

        full_path = presentation_parent_folder.joinpath(presentation_image_path.name)

        if not full_path.exists():
            shutil.copy(presentation_image_path, full_path)

    def save_secondary_items(self, clipping_dir: Path):
        for item in self.secondary_items:
            secondary_product_clipping = item.image_path
            full_path = clipping_dir.joinpath(secondary_product_clipping.name)
            if not full_path.exists():
                shutil.copy(secondary_product_clipping, full_path)

    def save_clipping(self, clipping_dir: Path, root_dir: Path):
        main_product_clipping = self.primary_item.image_path
        clipping_dir = root_dir.joinpath(clipping_dir)
        clipping_dir.mkdir(exist_ok=True)

        clipping_parent_folder = main_product_clipping.name.replace(main_product_clipping.suffix, "")
        clipping_parent_folder = clipping_dir.joinpath(clipping_parent_folder)
        clipping_parent_folder.mkdir(exist_ok=True)

        full_path = clipping_parent_folder.joinpath(main_product_clipping.name)
        if not full_path.exists():
            shutil.copy(main_product_clipping, full_path)
        return clipping_dir

    def save_background(self, root_dir: Path):
        background_path = Path(self._template.background)
        backgrounds_dir = root_dir.joinpath(BACKGROUND)
        backgrounds_dir.mkdir(exist_ok=True)
        full_path = backgrounds_dir.joinpath(background_path.name)
        if not full_path.exists():
            shutil.copy(background_path, full_path)

    @property
    def template(self):
        return self._template


class CompositionBuilder:
    """
    Class that takes a template and several images of the different types
    (PRIMARY, SECONDARY, PRESENTATION, ...) and yield all possible compositions
    resulting from combining all those elements.
    """

    def __init__(self, template: Template, primaries: [Path], secondaries: [Path], presentations: [Path]):
        """
        :param template:  The template we'll be using for composing.
        :param primaries:   A list of paths to primary product images.
        :param secondaries: A list of paths to secondary product images.
        :param presentations: A list of paths to presentation product images.
        """

        self._template = template
        self._primaries = primaries
        self._secondaries = secondaries
        self._presentations = presentations

    def compose(self) -> Generator[Composition, None, None]:
        """
        Generator function that yields a composition at the time.

        :return:
        """

        primary_items = self.build_primary_items()

        if settings.include_presentation_items:
            presentation_items = self.build_presentation_items()
        else:
            presentation_items = None

        if settings.include_secondary_items:
            secondary_items = self.build_secondary_items()
        else:
            secondary_items = None

        if presentation_items:
            primary_presentation_combos = itertools.product(primary_items, presentation_items)
        else:
            primary_presentation_combos = primary_items

        if secondary_items:
            secondary_combos = itertools.combinations(secondary_items, len(self._template.get_secondary_layers()))
        else:
            secondary_combos = [None]

        for combo in itertools.product(primary_presentation_combos, secondary_combos):
            primary_and_presentation = combo[0]

            if not presentation_items:
                primary_and_presentation = list([primary_and_presentation])

            secondaries = combo[1]

            # Add selection items (zoom, crop, ...)  to all compositions.
            if secondaries is not None and len(secondaries) > 0:
                all_ = list(itertools.chain(primary_and_presentation, secondaries))
            else:
                all_ = primary_and_presentation

            yield Composition(self._template, all_)

    def build_primary_items(self) -> [CompositionItem]:

        primary_layer = self._template.get_primary_layer()
        combos = itertools.product(self._primaries, [primary_layer])

        for image_path, layer in combos:
            yield CompositionItem(image_path=image_path, layer=layer)

    def build_presentation_items(self) -> [CompositionItem]:

        presentation_layer = self._template.get_presentation_layer()
        combos = itertools.product(self._presentations, [presentation_layer])

        for image_path, layer in combos:
            yield CompositionItem(image_path=image_path, layer=layer)

    def build_secondary_items(self) -> [CompositionItem]:

        secondary_layers = self._template.get_secondary_layers()
        number_of_layers = len(secondary_layers)

        permutations = itertools.permutations(self._secondaries, number_of_layers)

        for combo in permutations:
            for image_path, layer in zip(combo, secondary_layers):
                yield CompositionItem(image_path=image_path, layer=layer)


def despeluze_item_name(item: CompositionItem) -> str:
    item_path = Path(item.image_path)

    item_name = item_path.name
    item_name_ext = item_path.suffix
    item_name = item_name.replace(item_name_ext, '')

    return item_name


def compute_output_name(
        composition: Composition, extension='webp',
        primary_product_code_pattern=r'.*',
        presentation_code_pattern='.*',
        secondary_product_code_pattern='.*',
        append_bg_name_as_suffix=False):
    # Process main product.
    main_product_name = despeluze_item_name(composition.primary_item)
    main_product_name = main_product_name.split('_')[0]
    main_product_match = re.match(primary_product_code_pattern, main_product_name)

    if main_product_match:
        main_product_name = main_product_match.group()
    else:
        main_product_name = ''
        logger.warning(Fore.CYAN + "Warning: pattern " +
                       Fore.YELLOW + primary_product_code_pattern +
                       Fore.CYAN + "do not match " + Fore.GREEN + main_product_name)
        logger.warning(Style.RESET_ALL)

    # Do the same for background
    if composition.presentation_item:
        presentation_name = despeluze_item_name(composition.presentation_item)
    else:
        presentation_name = ""

    presentation_name_match = re.match(presentation_code_pattern, presentation_name)

    if presentation_name_match:
        presentation_name = presentation_name_match.groups()[-1]
    else:
        presentation_name = ''
        logger.warning(Fore.CYAN + "Warning: pattern " +
                       Fore.YELLOW + presentation_code_pattern +
                       Fore.CYAN + "do not match " + Fore.GREEN + presentation_name)
        logger.warning(Style.RESET_ALL)

    # And for secondary_items_names.
    secondary_items_names = [despeluze_item_name(item) for item in composition.secondary_items]
    secondary_items_names = [item_name.split('_')[0] for item_name in secondary_items_names]

    _secondary_products = []

    for secondary_item in secondary_items_names:
        match = re.match(secondary_product_code_pattern, secondary_item)
        if match:
            _secondary_products.append(match.group())
        else:
            logger.warning(Fore.CYAN + "Warning: pattern " +
                           Fore.YELLOW + secondary_product_code_pattern +
                           Fore.CYAN + "do not match " + Fore.GREEN + secondary_item)
            logger.warning(Style.RESET_ALL)

    name_components = filter(
        lambda x: x != '',
        [main_product_name, presentation_name, "_".join(_secondary_products)]
    )

    result = f"{'_'.join(name_components)}.{extension}"

    if append_bg_name_as_suffix:
        background_path = composition.template.background
        bg_name = background_path.name.replace(background_path.suffix, '')

        result_path = Path(result)
        result = result.replace(result_path.suffix, f'.{bg_name}{result_path.suffix}')

    return result
