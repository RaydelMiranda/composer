import itertools
import logging
import re
from collections import defaultdict
from ctypes import c_void_p, c_wchar_p
from gettext import gettext as _
from pathlib import Path
from typing import Generator, Callable

from colorama import Fore, Style
from wand.api import library

from composer_core.composer.common import CompositionItem
from composer_core.composer.compose import compose
from composer_core.config import settings
from models.template import Template, LayerType
from ui.common import GenerationOptions

logger = logging.Logger(__name__)

# -----------------------------------------------------------------------------
# Some wand settings.
# -----------------------------------------------------------------------------
library.MagickSetOption.argtypes = [c_void_p,
                                    c_wchar_p,
                                    c_wchar_p]


class CompositionError(Exception):
    pass


class Composition:
    """
    A class that represents a whole composition. This means the template plus
    any other image that fills the template slots.
    """

    def __init__(self, template: Template, items: [CompositionItem]):
        self._items = items
        self._template = template

    def render(self, options: GenerationOptions, output_path: Path = None, ) -> Path:
        """
        Render this composition into a complete image.

        :param options: Some options passed to the function that actually generates images.
        :param output_path: The directory where to save the resulting image. If not set
                            the current working directory is used.

        :return: The path of the resulting image.
        """

        composition_file_name = compute_output_name(self)
        output_file_name = output_path.joinpath(composition_file_name)

        return compose(self._items, self._template, options, output=output_file_name)

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
    def presentation_item(self) -> CompositionItem:
        items = self.filter_items(lambda x: x.layer.type == LayerType.PRESENTATION)
        if len(items) > 1:
            raise CompositionError(_("Found more that one presentation item. It should be only one."))
        return items[0]

    @property
    def secondary_items(self) -> [CompositionItem]:
        return self.filter_items(lambda x: x.layer.type == LayerType.SECONDARY)

    def save(self, options: GenerationOptions) -> Path:
        """
        Method that creates a folder structure ready for sync to s3.

        Such folder structure is as follow:

        - <product_code>
            | - <composition - code>.webp
            | - <composition - code>.svg
            | - presentation.png
            | - background.png

        The root folder for such structure might exist, due a previously saved composition of
        the same product, the same might happen with the background, if that's the case,
        the results are merged.

        :param options: Some options passed to the function that actually generates images.
        """

        # Get the root folder name.
        main_product_name = despeluze_item_name(self.primary_item)
        main_product_name = main_product_name.split('_')[0]
        root_dir = Path(settings.output_path).joinpath(main_product_name)

        # Try to crete the root dir, if exists, it is ok.
        root_dir.mkdir(exist_ok=True)

        path_to_webp = self.render(options, root_dir)

        # Save presentation
        presentation_image_path = Path(self.presentation_item.image_path)
        presentation_image_path.rename(root_dir.joinpath(presentation_image_path.name))

        return path_to_webp


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
        secondary_items = self.build_secondary_items()
        presentation_items = self.build_presentation_items()

        primary_presentation_combos = itertools.product(primary_items, presentation_items)
        secondary_combos = itertools.combinations(secondary_items, len(self._template.get_secondary_layers()))

        for combo in itertools.product(primary_presentation_combos, secondary_combos):
            primary_and_presentation = combo[0]
            secondaries = combo[1]

            all_ = list(itertools.chain(primary_and_presentation, secondaries))

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
        secondary_product_code_pattern='.*'):
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
    presentation_name = despeluze_item_name(composition.presentation_item)
    presentation_name_match = re.match(presentation_code_pattern, presentation_name)

    if presentation_name_match:
        presentation_name = presentation_name_match.group()
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

    return f"{'_'.join(name_components)}.{extension}"
