import logging
from collections import namedtuple
from enum import Enum, unique
from itertools import count
from pathlib import Path

import lxml
import svgutils as svg
from svgutils.transform import SVGFigure

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


class Layer:
    _type_counter = {
        LayerType.PRIMARY: count(),
        LayerType.SECONDARY: count(),
        LayerType.PRESENTATION: count()
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
        return Layer.XML_REPR.format(
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


class Template:
    """
    A class representing an SVG templates. Holds info about layers positions and sizes,
    as well as the background.
    """

    def __init__(self, output_dir=None):

        self.__layers = []
        self.__background = None

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

        if self.__base_svg is None:
            raise NoBaseSvgError(_("You must set a background before being able to add any layer."))

        layer = Layer(pos, size, _type)
        self.__layers.append(layer)
        return layer

    def map_layer_with_item(self, layer: Layer, graphic_item):
        self.__layer_map_to_item[graphic_item] = layer

    def remove_layer_for_item(self, item):
        self.__layers.remove(self.__layer_map_to_item[item])
        del self.__layer_map_to_item[item]

    def update_layer(self, item):
        layer = self.__layer_map_to_item[item]
        scale_factor = item.scale()

        pos = Position(item.x(), item.y(), item.zValue())

        size = Size(
            item.boundingRect().width() * scale_factor,
            item.boundingRect().height() * scale_factor
        )

        layer.update(pos, size)

    def set_background(self, background_file_path: str, size: Size = None):

        path = Path(background_file_path)

        if size is None:
            size = Size(1290, 1080)

        if path.exists() and path.is_file():
            self.__background = background_file_path

        self.__base_svg = svg.compose.Figure(
            size.width, size.height,
            svg.compose.Image(size.width, size.height, background_file_path)
        )

    def __build_svg_final_figure(self):
        if self.__base_svg is None:
            raise NoBaseSvgError(_("You must , at least, set a background before being able to render the svg."))

        svg_xml = self.__base_svg.tostr()

        for layer in self.__layers:
            svg_xml = self.__inject_layer(svg_xml, layer)

        try:
            svg_figure = svg.transform.fromstring(svg_xml.decode())
        except lxml.etree.XMLSysntaxError as err:
            logger.exception(err)
            return None
        else:
            return svg_figure

    def render(self):
        """ Write an svg file to the output dir."""

        svg_figure = self.__build_svg_final_figure()
        if svg_figure is not None:
            svg_figure.save(self.__output_dir.joinpath("template.svg"))

    def render_to_str(self):
        """ Write an svg as string. """
        svg_figure = self.__build_svg_final_figure()
        if svg_figure is not None:
            return svg_figure.to_str()

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
        return next(layer for layer in self.__layers if layer.type == LayerType.PRIMARY)

    def get_presentation_layer(self):
        return next(layer for layer in self.__layers if layer.type == LayerType.PRESENTATION)

    def get_secondary_layers(self) -> [Layer]:
        return [layer for layer in self.__layers if layer.type == LayerType.SECONDARY]
