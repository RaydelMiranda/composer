import itertools
from collections import defaultdict
from pathlib import Path
from typing import Generator

from composer_core.composer.common import CompositionItem
from composer_core.composer.compose import compose
from models.template import Template


class Composition:
    """
    A class that represents a whole composition. This means the template plus
    any other image that fills the template slots.
    """

    def __init__(self, template: Template, items: [CompositionItem]):
        self._items = items
        self._template = template

    def render(self, output_path: Path = None) -> Path:
        """
        Render this composition into a complete image.

        :param output_path: The directory where to save the resulting image. If not set
                            the current working directory is used.

        :return: The path of the resulting image.
        """

        if output_path is None:
            output_path = Path('.')

        compose(self._items, self._template)

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
            layer_id_count[item.layer_id] += 1
            # There are two different items assigned to the same svg layer.
            if layer_id_count[item.layer_id] > 1:
                return False

        return True


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
            yield CompositionItem(image_path=image_path, layer_id=layer.layer_id, image_id=layer.image_id)

        raise StopIteration

    def build_presentation_items(self) -> [CompositionItem]:

        presentation_layer = self._template.get_presentation_layer()
        combos = itertools.product(self._presentations, [presentation_layer])

        for image_path, layer in combos:
            yield CompositionItem(image_path=image_path, layer_id=layer.layer_id, image_id=layer.image_id)

        raise StopIteration

    def build_secondary_items(self) -> [CompositionItem]:

        secondary_layers = self._template.get_secondary_layers()
        number_of_layers = len(secondary_layers)

        permutations = itertools.permutations(self._secondaries, number_of_layers)

        for combo in permutations:
            for image_path, layer in zip(combo, secondary_layers):
                yield CompositionItem(image_path=image_path, layer_id=layer.layer_id, image_id=layer.image_id)

        raise StopIteration
