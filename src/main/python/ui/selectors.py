import sys

from PyQt5.QtCore import Qt, QRectF, QPointF, QSize, pyqtSignal, QObject
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem


class Selector(QGraphicsRectItem):
    handle_top_left = 1
    handle_top_middle = 2
    handle_top_right = 3
    handle_middle_left = 4
    handle_middle_right = 5
    handle_bottom_left = 6
    handle_bottom_middle = 7
    handle_bottom_right = 8

    handle_cursors = {
        handle_top_left: Qt.SizeFDiagCursor,
        handle_top_middle: Qt.SizeVerCursor,
        handle_top_right: Qt.SizeBDiagCursor,
        handle_middle_left: Qt.SizeHorCursor,
        handle_middle_right: Qt.SizeHorCursor,
        handle_bottom_left: Qt.SizeBDiagCursor,
        handle_bottom_middle: Qt.SizeVerCursor,
        handle_bottom_right: Qt.SizeFDiagCursor,
    }

    def __init__(self, *args, rgb=(255, 0, 0), handle_size=+8.0, handle_space=-4.0, aspect_ratio=None):
        """
        Initialize the shape.
        """
        super().__init__(*args)

        self.handle_size = handle_size
        self.handle_space = handle_space

        self.handles = {}
        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None
        self.aspect_ratio = aspect_ratio
        self.rgb = rgb
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

        self.text_size = self.rect().height() / 15

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, move_event):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(move_event.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handle_cursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(move_event)

    def hoverLeaveEvent(self, move_event):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(move_event)

    def mousePressEvent(self, mouse_event):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handle_selected = self.handleAt(mouse_event.pos())
        if self.handle_selected:
            self.mouse_press_pos = mouse_event.pos()
            self.mouse_press_rect = self.boundingRect()
        super().mousePressEvent(mouse_event)

    def mouseMoveEvent(self, mouse_event):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handle_selected is not None:
            self.interactiveResize(mouse_event.pos())
        else:
            super().mouseMoveEvent(mouse_event)

    def mouseReleaseEvent(self, mouse_event):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouse_event)
        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handle_size + self.handle_space
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handle_size
        b = self.boundingRect()
        self.handles[self.handle_top_left] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handle_top_middle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handle_top_right] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handle_middle_left] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handle_middle_right] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handle_bottom_left] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handle_bottom_middle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handle_bottom_right] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mouse_pos):
        """
        Perform shape interactive resize.
        """
        offset = self.handle_size + self.handle_space
        bounding_rect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handle_selected == self.handle_top_left:

            from_x = self.mouse_press_rect.left()
            from_y = self.mouse_press_rect.top()
            to_x = from_x + mouse_pos.x() - self.mouse_press_pos.x()
            to_y = from_y + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setX(to_x - from_x)
            diff.setY(to_y - from_y)
            bounding_rect.setLeft(to_x)
            bounding_rect.setTop(to_y)
            rect.setLeft(bounding_rect.left() + offset)
            rect.setTop(bounding_rect.top() + offset)

        elif self.handle_selected == self.handle_top_middle:

            from_y = self.mouse_press_rect.top()
            to_y = from_y + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setY(to_y - from_y)
            bounding_rect.setTop(to_y)
            rect.setTop(bounding_rect.top() + offset)

        elif self.handle_selected == self.handle_top_right:

            from_x = self.mouse_press_rect.right()
            from_y = self.mouse_press_rect.top()
            to_x = from_x + mouse_pos.x() - self.mouse_press_pos.x()
            to_y = from_y + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setX(to_x - from_x)
            diff.setY(to_y - from_y)
            bounding_rect.setRight(to_x)
            bounding_rect.setTop(to_y)
            rect.setRight(bounding_rect.right() - offset)
            rect.setTop(bounding_rect.top() + offset)

        elif self.handle_selected == self.handle_middle_left:

            from_x = self.mouse_press_rect.left()
            to_x = from_x + mouse_pos.x() - self.mouse_press_pos.x()
            diff.setX(to_x - from_x)
            bounding_rect.setLeft(to_x)
            rect.setLeft(bounding_rect.left() + offset)

        elif self.handle_selected == self.handle_middle_right:
            from_x = self.mouse_press_rect.right()
            to_x = from_x + mouse_pos.x() - self.mouse_press_pos.x()
            diff.setX(to_x - from_x)
            bounding_rect.setRight(to_x)
            rect.setRight(bounding_rect.right() - offset)

        elif self.handle_selected == self.handle_bottom_left:

            from_x = self.mouse_press_rect.left()
            from_y = self.mouse_press_rect.bottom()
            to_x = from_x + mouse_pos.x() - self.mouse_press_pos.x()
            to_y = from_y + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setX(to_x - from_x)
            diff.setY(to_y - from_y)
            bounding_rect.setLeft(to_x)
            bounding_rect.setBottom(to_y)
            rect.setLeft(bounding_rect.left() + offset)
            rect.setBottom(bounding_rect.bottom() - offset)

        elif self.handle_selected == self.handle_bottom_middle:

            from_y = self.mouse_press_rect.bottom()
            to_y = from_y + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setY(to_y - from_y)
            bounding_rect.setBottom(to_y)
            rect.setBottom(bounding_rect.bottom() - offset)

        elif self.handle_selected == self.handle_bottom_right:

            from_x = self.mouse_press_rect.right()
            from_y = self.mouse_press_rect.bottom()
            to_x = from_x + mouse_pos.x() - self.mouse_press_pos.x()
            to_y = from_y + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setX(to_x - from_x)
            diff.setY(to_y - from_y)
            bounding_rect.setRight(to_x)
            bounding_rect.setBottom(to_y)
            rect.setRight(bounding_rect.right() - offset)
            rect.setBottom(bounding_rect.bottom() - offset)

        if self.aspect_ratio:
            rect.setHeight(rect.width() / self.aspect_ratio)

        self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """

        painter.setBrush(QBrush(QColor(*self.rgb, 100)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(*self.rgb, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handle_selected is None or handle == self.handle_selected:
                painter.drawEllipse(rect)

        font = painter.font()
        font.setPointSize(self.text_size)
        painter.setFont(font)

        text_padding = self.text_size / 2

        painter.drawText(
            self.rect().x() + self.text_size + text_padding,
            self.rect().y() + self.text_size + text_padding,
            f'( {self.rect().width():.2f} x {self.rect().height():.2f} )'
        )

    def itemChange(self, change, value):
        scene = self.scene()
        if scene and QGraphicsItem.ItemPositionHasChanged == change:
            scene.on_item_position_change(self, change, value)
        if scene and QGraphicsItem.ItemScaleHasChanged == change:
            scene.on_item_scale_changed(self, change, value)
        return super(Selector, self).itemChange(change, value)


def main():
    app = QApplication(sys.argv)

    grview = QGraphicsView()
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 680, 459)

    scene.addPixmap(QPixmap('01.png'))
    grview.setScene(scene)

    item = Selector(0, 0, 300, 150)
    scene.addItem(item)

    grview.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
    grview.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
