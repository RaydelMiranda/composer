from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QPoint
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QErrorMessage
from pathlib import Path
from wand.image import Image

from composer_core.composer.common import Rectangle, min_resize
from composer_core.config import settings
from models.template import Template, LayerType, Position, Size, NoBaseSvgError
from ui.common import BACKGROUND, PRESENTATION, PRIMARY, SECONDARY, SVG_SCALE_FACTOR


class CustomPixmapItem(QGraphicsPixmapItem):

    def __init__(self, *args, **kwargs):
        super(CustomPixmapItem, self).__init__(*args, **kwargs)

    def itemChange(self, change, value):
        scene = self.scene()
        if scene and QGraphicsPixmapItem.ItemPositionHasChanged == change:
            scene.on_item_position_change(self, change, value)
        if scene and QGraphicsPixmapItem.ItemScaleHasChanged == change:
            scene.on_item_scale_changed(self, change, value)

        return super(CustomPixmapItem, self).itemChange(change, value)


class ComposerGraphicScene(QGraphicsScene):
    item_moved = pyqtSignal(float, float)

    def __init__(self, parent, *args, **kwargs):
        super(ComposerGraphicScene, self).__init__(parent, *args, **kwargs)

        self.__template = Template()
        self.__background_item = None

        self._rubber_band = None
        self._rubber_band_origin = QPoint(0, 0)

    @property
    def template(self):
        return self.__template

    @template.setter
    def template(self, value):
        self.__template = value

    def dragEnterEvent(self, ev):
        if ev.mimeData().hasImage():
            ev.accept()

    def dropEvent(self, ev):

        item = None
        origin = None
        path = None

        if ev.mimeData().hasText():
            text = ev.mimeData().text()

            origin, path = text.split(',')
            path = Path(path)

        if ev.mimeData().hasImage():
            pixmap = ev.mimeData().imageData()

            # If origin != BACKGROUND, we scale item to fit.
            parent = self.__background_item if origin != BACKGROUND else None
            item = CustomPixmapItem(pixmap, parent=parent)

            item.setFlags(QGraphicsPixmapItem.ItemIsMovable |
                          QGraphicsPixmapItem.ItemIsSelectable |
                          QGraphicsPixmapItem.ItemSendsGeometryChanges)

            if origin == BACKGROUND:
                item.setZValue(-1)

            if origin != BACKGROUND:
                # Scale to fit the scene.
                scene_rect = self.sceneRect()
                item_rect = item.boundingRect()

                scene_width = scene_rect.width()
                scene_height = scene_rect.height()

                item_width = item_rect.width()
                item_height = item_rect.height()

                if scene_width >= scene_height:
                    factor = scene_height / (2 * item_height)
                else:
                    factor = scene_width / (2 * item_width)

                item.setScale(factor)

                dx = item.boundingRect().width() * factor / 2
                dy = item.boundingRect().height() * factor / 2

                scene_pos = ev.scenePos()

                item.setPos(QPointF(abs(scene_pos.x() - dx), abs(scene_pos.y() - dy)))
            else:
                # Modify the background aspect ratio in order to match the aspect ratio for
                # the desired size.
                desired_size_width = settings.adaptive_resize_width
                desired_size_height = settings.adaptive_resize_height

                if not (desired_size_height == 0 or desired_size_width == 0):
                    ratio = desired_size_width / desired_size_height

                    with Image(filename=str(path)) as original_background:
                        r = Rectangle(original_background.width, original_background.height)
                        r_resize = min_resize(r, ratio)
                        original_background.liquid_rescale(int(r_resize.width), int(r_resize.height))

                        root_dir = Path(settings.output_path)
                        backgrounds_dir = root_dir.joinpath(BACKGROUND)
                        backgrounds_dir.mkdir(exist_ok=True)

                        name = path.name.replace(path.suffix, f".fixed{ path.suffix}")

                        path = backgrounds_dir.joinpath(name)

                        original_background.save(filename=str(path))

            self.addItem(item)

            if origin == BACKGROUND:
                self.show_grid()

            self.parent().fitInView(self.sceneRect(), Qt.KeepAspectRatio)

        self.process_dropped_data(item, origin=origin, path=path)

    def dragMoveEvent(self, ev):
        ev.accept()

    def on_item_position_change(self, item, change, value):
        self.__template.update_layer(item)
        self.item_moved.emit(value.x(), value.y())

    def on_item_scale_changed(self, item: CustomPixmapItem, change, value):
        self.__template.update_layer(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            items = self.selectedItems()
            for item in items:
                self.removeItem(item)
        return super(ComposerGraphicScene, self).keyPressEvent(event)

    def process_dropped_data(self, item, origin: str, path: Path):
        """
        Create the new layers according the given item, this layers are mapped then to the item
        in order to update if necessary when rendering the whole svg.

        :param path: path to the real image being processed.
        :param origin: String containing the origin of the item, one of
                        "BACKGROUND", "PRESENTATION", "PRIMARY", "SECONDARY"
        :param item:  A QGraphicsItem.
        """

        layer_type_origin_map = {
            PRESENTATION: LayerType.PRESENTATION,
            PRIMARY: LayerType.PRIMARY,
            SECONDARY: LayerType.SECONDARY
        }

        bounding_rect = item.boundingRect()

        pos = Position(item.x() * SVG_SCALE_FACTOR, item.y() * SVG_SCALE_FACTOR, item.zValue())

        size = Size(bounding_rect.width() * SVG_SCALE_FACTOR, bounding_rect.height() * SVG_SCALE_FACTOR)

        if origin == BACKGROUND:
            self.__template.set_background(str(path), size=size)
        else:
            try:
                layer = self.__template.add_layer(pos=pos, size=size, _type=layer_type_origin_map[origin])
            except NoBaseSvgError as err:
                self.removeItem(item)
                error_dialog = QErrorMessage(self.parent())
                error_dialog.showMessage(str(err))
            else:
                self.__template.map_layer_with_item(layer, graphic_item=item)

    def render_template(self) -> Path:
        return self.__template.render()

    def set_output_dir(self, path: str):
        self.__template.output_dir = path

    def show_grid(self):

        w = int(self.width())
        h = int(self.height())

        w_step = int(w / 3)
        h_step = int(h / 3)

        # Add vertical lines
        for x in range(0, w, w_step):
            self.addLine(x, 0, x, h)

        # Add horizontal lines.
        for y in range(0, h, h_step):
            self.addLine(0, y, w, y)
