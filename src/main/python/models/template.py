import logging
from collections import namedtuple
from enum import Enum, unique

import svgutils as svg
from PyQt5.QtWidgets import QGraphicsItem
from io import BytesIO
from itertools import count
from lxml import etree
from lxml.cssselect import CSSSelector
from pathlib import Path
from typing import Union

from ui.common import SVG_SCALE_FACTOR

logger = logging.getLogger(__file__)

Position = namedtuple('Position', 'x, y, z')
Size = namedtuple('Size', 'width, height')

from gettext import gettext as _


class NoBaseSvgError(Exception):
    pass


class OutputDirError(Exception):
    pass


@unique
class LayerType(Enum):
    PRIMARY = 0
    PRESENTATION = 1
    SECONDARY = 2
    ZOOM_SELECTION = 3
    CROP_SELECTION = 4


class Layer:
    _type_counter = {
        LayerType.PRIMARY: count(),
        LayerType.SECONDARY: count(),
        LayerType.PRESENTATION: count(),
        LayerType.ZOOM_SELECTION: count(),
        LayerType.CROP_SELECTION: count()
    }

    XML_REPR = (
        """
    <g
        id="{layer_id}"
    >   
                
        <image
            y="{image_pos_y}"
            x="{image_pos_x}"
            id="{image_id}"
            preserveAspectRatio="none"
            height="{image_height}"
            width="{image_width}" 
        />
        
    </g>
    """)

    def __init__(self, pos: Position, size: Size, _type: LayerType, lock_aspect_ratio: bool = True):
        """
        :param pos: The x and y coordinates wrapped in a Position object.
        :param size: The size of the layer wrapped in a Size object.
        :param lock_aspect_ratio:  If true any change to width will affect height, and the other way around.
        """

        self.type = _type
        self.pos = pos

        self._size = size
        self._lock_aspect_ratio = lock_aspect_ratio

        self.__inner_id = next(Layer._type_counter[self.type])

    @property
    def width(self) -> int:
        return self._size.width

    @property
    def height(self) -> int:
        return self._size.height

    @width.setter
    def width(self, value: int):

        if self._lock_aspect_ratio:
            factor = value / self._size.width
        else:
            factor = 1.0

        self._size.width = value
        self._size.height = self._size.height * factor

    @height.setter
    def height(self, value: int):

        if self._lock_aspect_ratio:
            factor = value / self._size.height
        else:
            factor = 1.0

        self._size.height = value
        self._size.width = self._size.width * factor

    @property
    def layer_id(self):
        return f'layer-{self.type.name}-{self.__inner_id}'

    @property
    def image_id(self):
        return f'image-{self.type.name}-{self.__inner_id}'

    @property
    def xml(self) -> str:
        return self.XML_REPR.format(
            layer_id=self.layer_id,
            image_pos_x=f'{self.pos.x}',
            image_pos_y=f'{self.pos.y}',
            image_id=self.image_id,
            image_height=f'{self._size.height}',
            image_width=f'{self._size.width}'
        )

    def update(self, pos: Position = None, size: Size = None) -> "Layer":
        if pos:
            self.pos = pos
        if size:
            self._size = size

        return self


class SelectionLayer(Layer):
    XML_REPR = (
        """
    <selection_layer
        id="{layer_id}"
    >   

        <image
            y="{image_pos_y}"
            x="{image_pos_x}"
            id="{image_id}"
            preserveAspectRatio="none"
            height="{image_height}"
            width="{image_width}" 
        />

    </selection_layer>
    """)

    def __init__(self, pos: Position, size: Size, _type: LayerType, lock_aspect_ratio: bool = True):
        super(SelectionLayer, self).__init__(pos, size, _type, lock_aspect_ratio=lock_aspect_ratio)


class Template:
    """
    A class representing an SVG templates. Holds info about layers positions and sizes,
    as well as the background.
    """

    def __init__(self, output_dir=None):

        self.__layers = []
        self.__background = None
        self.__loaded_from_file = False
        self.__str_representation = None
        self.__output_dir = Path.cwd()

        if output_dir is not None:
            output_path = Path(output_dir)
            if output_path.exists() and output_path.is_dir():
                self.__output_dir = output_path

        # Base svg on top of which we'll adding layers to create the
        # final template. This svg start with the `set_background`
        # method.
        self.__base_svg = None

        self.__layer_map_to_item = {}

    def add_layer(self, pos: Position, size: Size, _type: LayerType) -> Layer:

        if _type in [LayerType.CROP_SELECTION, LayerType.ZOOM_SELECTION]:
            return self._add_selection_layer(pos, size, _type)

        if self.__base_svg is None and not self.__loaded_from_file:
            raise NoBaseSvgError(_("You must set a background before being able to add any layer."))

        layer = Layer(pos, size, _type)
        self.__layers.append(layer)
        return layer

    def _add_selection_layer(self, pos: Position, size: Size, _type: LayerType):
        if self.__base_svg is None and not self.__loaded_from_file:
            raise NoBaseSvgError(_("You must set a background before being able to perform any selection."))

        layer = SelectionLayer(pos, size, _type)
        self.__layers.append(layer)
        return layer

    def load_from_file(self, template_file):

        layer_selector = CSSSelector("[id^=layer-]")
        image_selector = CSSSelector("[id^=image-]")

        parser = etree.XMLParser(huge_tree=True)
        tree = etree.parse(template_file, parser)

        self.__str_representation = etree.tostring(tree)

        layer_type_map = {
            LayerType.PRIMARY.name: LayerType.PRIMARY,
            LayerType.SECONDARY.name: LayerType.SECONDARY,
            LayerType.PRESENTATION.name: LayerType.PRESENTATION,
        }

        self.__loaded_from_file = True

        for layer in layer_selector(tree):
            layer_type_name = layer.get("id").split('-')[1]

            image = image_selector(layer)[0]

            pos = Position(x=image.get("x"), y=image.get("y"), z=0)
            size = Size(width=image.get("width"), height=image.get("height"))

            self.add_layer(pos=pos, size=size, _type=layer_type_map[layer_type_name])

    def map_layer_with_item(self, layer: Layer, graphic_item):
        self.__layer_map_to_item[graphic_item] = layer

    def remove_layer_for_item(self, item):
        self.__layers.remove(self.__layer_map_to_item[item])
        del self.__layer_map_to_item[item]

    def __build_svg_final_figure(self) -> BytesIO:
        if self.__base_svg is None:
            raise NoBaseSvgError(_("You must , at least, set a background before being able to render the svg."))

        svg_xml = self.__base_svg.tostr()

        for layer in self.__layers:
            svg_xml = self.__inject_layer(svg_xml, layer)

        svg_xml_stream = BytesIO(svg_xml)

        return svg_xml_stream

    @property
    def output_dir(self):
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, path):
        p = Path(path)
        if p.is_dir() and p.exists():
            self.__output_dir = p
        else:
            raise OutputDirError(_("Output dir must be an existing directory."))

    @property
    def background(self) -> Path:
        return Path(self.__background)

    @staticmethod
    def __inject_layer(svg_xml: bytes, layer: Layer) -> bytes:
        """
        :param svg_xml: The xml representation for the svg file.
        :return:  The new svg_xml string after layer injection.
        """

        layer_injection = (
            f'{layer.xml}'
            f'</svg>'
        )

        return svg_xml.replace(b'</svg>', layer_injection.encode())

    def get_primary_layer(self) -> Layer:
        return self._get_layer_by_type(LayerType.PRIMARY)

    def get_presentation_layer(self) -> Layer:
        return self._get_layer_by_type(LayerType.PRESENTATION)

    def get_secondary_layers(self) -> [Layer]:
        return [layer for layer in self.__layers if layer.type == LayerType.SECONDARY]

    def get_zoom_selection_layer(self) -> Layer:
        return self._get_layer_by_type(LayerType.ZOOM_SELECTION)

    def get_crop_selection_layer(self) -> Layer:
        return self._get_layer_by_type(LayerType.CROP_SELECTION)

    def _get_layer_by_type(self, _type: LayerType) -> Union[Layer, None]:
        try:
            return next(layer for layer in self.__layers if layer.type == _type)
        except StopIteration:
            return None

    def render(self) -> Path:
        """
        Write an svg file to the output dir.

        Returns the a Path object with the complete file name
        of the generated template.
        """

        svg_figure_stream = self.__build_svg_final_figure()

        template_filename = self.__output_dir.joinpath("template.svg")
        with open(template_filename, 'wb') as template_file:
            template_file.write(svg_figure_stream.read())
            return template_filename

    def render_to_bytes(self):
        """ Write an svg as string. """
        if self.__str_representation is not None:
            return self.__str_representation

        svg_stream = self.__build_svg_final_figure()

        # Proactive reset of the stream in case it has been read at some point.
        svg_stream.seek(0)

        result = svg_stream.read()

        if result:
            self.__str_representation = result

        return self.__str_representation

    def set_background(self, background_file_path: str, size: Size = None):

        path = Path(background_file_path)

        if size is None:
            size = Size(1500, 1500)

        if path.exists() and path.is_file():
            self.__background = background_file_path

        try:
            self.__base_svg = svg.compose.Figure(
                size.width, size.height,
                svg.compose.Image(size.width, size.height, background_file_path)
            )
        except Exception as err:
            logger.exception(err)

    def remove_background(self):
        self.__background = None
        self.__base_svg = None

    def update_layer(self, item):
        layer = self.__layer_map_to_item.get(item)

        if layer is None:
            return

        scale_factor = item.scale()

        pos = Position(item.x() * SVG_SCALE_FACTOR, item.y() * SVG_SCALE_FACTOR, item.zValue())

        size = Size(
            item.boundingRect().width() * scale_factor * SVG_SCALE_FACTOR,
            item.boundingRect().height() * scale_factor * SVG_SCALE_FACTOR
        )

        layer.update(pos, size)

    def get_item_for_layer(self, layer: Layer) -> QGraphicsItem:
        for item, _layer in self.__layer_map_to_item.items():
            if _layer == layer:
                return item
