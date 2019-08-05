from collections import namedtuple
from gettext import gettext as _

import magic
from PyQt5.QtCore import Qt, QDirIterator, QAbstractListModel, pyqtSignal, pyqtSlot, QObject, QThread
from PyQt5.QtGui import QPixmap
from pathlib import Path

from models.errors import ReadOnlyError
from ui.common import IMAGE_TYPES

Resource = namedtuple('Resource', 'path, image, thumbnail')


class LoadingImagesWorker(QObject):
    resource_loaded = pyqtSignal(Resource)
    finished = pyqtSignal()

    def __init__(self, path: str, _filter: [str]):
        super(LoadingImagesWorker, self).__init__()

        self._path = path
        self._filter = _filter

    def run(self):

        file_iter = QDirIterator(self._path, QDirIterator.Subdirectories)

        while file_iter.hasNext():

            file_name = file_iter.next()

            if Path(file_name).is_dir():
                continue

            condition = [
                magic.from_file(file_name).lower().startswith(ext)
                for ext in self._filter
            ]

            if any(condition):
                new_resource = Resource(
                    path=file_name,
                    image=QPixmap(file_name),
                    thumbnail=QPixmap(file_name).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )

                self.resource_loaded.emit(new_resource)

        self.finished.emit()


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

        self._thread = QThread()
        self._load_images_worker = LoadingImagesWorker(path=path, _filter=self.__filter)
        self._load_images_worker.moveToThread(self._thread)
        self._thread.started.connect(self._load_images_worker.run)
        self._load_images_worker.resource_loaded.connect(self.resource_loaded)
        self._thread.start()
        self._load_images_worker.finished.connect(self._thread.quit)

    @pyqtSlot(Resource, name="resource_loaded")
    def resource_loaded(self, resource):
        end = len(self.__resources)
        self.beginInsertRows(self.index(end), end, end + 1)
        self.__resources.append(resource)
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
