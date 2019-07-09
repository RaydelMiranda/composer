from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QErrorMessage
from pathlib import Path

from models.template import Template, LayerType, Position, Size, NoBaseSvgError
from ui.common import BACKGROUND, PRESENTATION, PRIMARY, SECONDARY


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
        text = None
        origin = None

        if ev.mimeData().hasText():
            text = ev.mimeData().text()

            origin, _ = text.split(',')

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

            self.addItem(item)

            self.parent().fitInView(self.sceneRect(), Qt.KeepAspectRatio)

        self.process_dropped_data(item, text)

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

    def process_dropped_data(self, item, text):
        """
        Create the new layers according the given item, this layers are mapped then to the item
        in order to update if necessary when rendering the whole svg.

        :param item:  A QGraphicsItem.
        :param text: A string containing the <origin,path> of the dropped data.
        """

        layer_type_origin_map = {
            PRESENTATION: LayerType.PRESENTATION,
            PRIMARY: LayerType.PRIMARY,
            SECONDARY: LayerType.SECONDARY
        }

        origin, path = text.split(',')

        print(f'Origin: {origin}, Path: {path}')

        bounding_rect = item.boundingRect()
        pos = Position(item.x(), item.y(), item.zValue())
        size = Size(bounding_rect.width(), bounding_rect.height())

        if origin == BACKGROUND:
            self.__template.set_background(path, size=size)
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
