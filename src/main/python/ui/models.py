from collections import namedtuple
from gettext import gettext as _
from pathlib import Path

import magic
from PyQt5.QtCore import Qt, QDirIterator, QAbstractListModel
from PyQt5.QtGui import QPixmap

from models.errors import ReadOnlyError
from ui.common import IMAGE_TYPES

Resource = namedtuple('Resource', 'path, image, thumbnail')


class ResourceModel(QAbstractListModel):

    def __init__(self, parent, _filter=None, origin=None, *args, **kwargs):
        """
        :param _filter: Type of files we are interested in.
        :param origin: A unique text that identifies an instance of this class as the origen
                       of a Drag-Drop event.
        :param args:
        :param kwargs:
        """
        super(ResourceModel, self).__init__(parent, *args, **kwargs)

        if _filter is None:
            self.__filter = IMAGE_TYPES

        self.__root_path = None
        self.__resources = []
        self.__origin = origin

    @property
    def resources(self):
        return self.__resources

    @resources.setter
    def resources(self, value):
        raise ReadOnlyError(_("Resources can't be edited directly."))

    def setRootPath(self, path: str):

        end = len(self.__resources)

        self.beginRemoveRows(self.index(0), 0, end)
        self.__resources = []
        self.endRemoveRows()

        self.__root_path = path

        file_iter = QDirIterator(path, QDirIterator.Subdirectories)

        while file_iter.hasNext():

            file_name = file_iter.next()

            if Path(file_name).is_dir():
                continue

            condition = [
                magic.from_file(file_name).lower().startswith(ext)
                for ext in self.__filter
            ]

            if any(condition):
                self.beginInsertRows(self.index(end), end, end + 1)
                self.__resources.append(
                    Resource(
                        path=file_name,
                        image=QPixmap(file_name),
                        thumbnail=QPixmap(file_name).scaled(190, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                     )
                )
                self.endInsertRows()

    def data(self, index, role=None):
        if role == Qt.DecorationRole:
            return self.__resources[index.row()].thumbnail

    def flags(self, index):
        if index.isValid():
            return super(ResourceModel, self).flags(index) | Qt.ItemIsDragEnabled

        return Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__resources)

    def mimeData(self, indexes, model_index=None):

        mime_data = super(ResourceModel, self).mimeData(indexes)
        resource = self.__resources[indexes[0].row()]

        mime_data.setImageData(resource.image)
        mime_data.setText(f'{self.__origin},{resource.path}')

        return mime_data
