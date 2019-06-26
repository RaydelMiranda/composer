from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QErrorMessage

from models.template import Template, LayerType, Position, Size, NoBaseSvgError
from ui.common import BACKGROUND, VASE, PRIMARY, SECONDARY


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

    def dragEnterEvent(self, ev):
        if ev.mimeData().hasImage():
            ev.accept()

    def dropEvent(self, ev):

        item = None
        text = None

        if ev.mimeData().hasImage():
            pixmap = ev.mimeData().imageData()

            item = CustomPixmapItem(pixmap)
            item.setFlags(QGraphicsPixmapItem.ItemIsMovable |
                          QGraphicsPixmapItem.ItemIsSelectable |
                          QGraphicsPixmapItem.ItemSendsGeometryChanges)
            item.setPos(ev.pos())

            self.addItem(item)
            self.parent().fitInView(self.sceneRect(), Qt.KeepAspectRatio)

        if ev.mimeData().hasText():
            text = ev.mimeData().text()

        self.process_dropped_data(item, text)

    def dragMoveEvent(self, ev):
        ev.accept()

    def on_item_position_change(self, item, change, value):
        self.__template.update_layer(item)
        self.item_moved.emit(value.x(), value.y())

    def on_item_scale_changed(self, item, change, value):
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
            VASE: LayerType.VASE,
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

    def render_template(self):
        self.__template.render()

    def set_output_dir(self, path: str):
        self.__template.output_dir = path
