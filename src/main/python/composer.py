from configparser import NoOptionError
from contextlib import contextmanager
from gettext import gettext as _
from pathlib import Path

from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLineEdit, QErrorMessage, QMessageBox

from _s3.sync import S3Sync
from composer_core.composer.composition import CompositionBuilder, Composition
from composer_core.config import settings
from models.template import OutputDirError, Template, Position, Size, LayerType, Layer
from ui.common import PRIMARY, SECONDARY, BACKGROUND, PRESENTATION, GenerationOptions
from ui.composer_graphic_scene import ComposerGraphicScene
from ui.imagecomposer import Ui_Imagecomposer
from ui.models import ResourceModel
from ui.selectors import Selector


@contextmanager
def disconnected_signal(control, signal_name):
    pass


class ComposeWorker(QObject):
    # Composition ready signal, receives a str as argument being the path
    # of the resulting composition.
    composition_ready = pyqtSignal(str)
    composition_finished = pyqtSignal()
    composition_uploading_to_s3 = pyqtSignal()
    composition_uploaded_to_s3 = pyqtSignal()

    def __init__(self,
                 compositions: [Composition],
                 options: GenerationOptions, output_path: Path):
        super(ComposeWorker, self).__init__()

        self._compositions = compositions
        self._options = options
        self._output_path = output_path

    def run(self):
        for composition in self._compositions:
            if composition.is_valid():
                path = composition.save(self._options)
                self.composition_ready.emit(str(path))

        if self._options.upload_to_s3:
            self.composition_uploading_to_s3.emit()

            sync = S3Sync()
            sync.sync(str(self._output_path), settings.bucket_name)

            self.composition_uploaded_to_s3.emit()

        self.composition_finished.emit()


class Composer(QMainWindow):

    def __init__(self, parent=None):
        super(Composer, self).__init__(parent=parent)
        # initializing ui components.
        self.ui = Ui_Imagecomposer()
        self.ui.setupUi(self)
        self.__settings = settings
        self.__loading_settings = False

        self.ui.output_path.editingFinished.connect(self.on_output_path_changed)
        self.ui.bucket_name.textChanged.connect(self.__settings_changed)
        self.ui.upload_to_s3.clicked.connect(self.__settings_changed)

        self.ui.secret_access_key.textChanged.connect(self.__settings_changed)
        self.ui.access_key.textChanged.connect(self.__settings_changed)

        self.ui.image_result_width.valueChanged.connect(self.__settings_changed)
        self.ui.image_result_height.valueChanged.connect(self.__settings_changed)

        self.__prepare_list_views()
        self.__prepare_graphic_view()
        self.__prepare_property_controls()

        self._composition_thread = QThread()
        self._composition_worker = None

        self.__load_settings()

        # Connect conf widgets.
        self.ui.apply_unsharp.clicked.connect(self.__settings_changed)
        self.ui.secondary_generation.clicked.connect(self.__settings_changed)
        self.ui.override_images.clicked.connect(self.__settings_changed)

    def __load_settings(self):

        self.__loading_settings = True

        # Resource settings.
        self.ui.main_products_path.setText(str(Path(settings.main_products_path).absolute()))
        self.ui.secondary_products_path.setText(str(Path(settings.secondary_products_path).absolute()))
        self.ui.presentations_path.setText(str(Path(settings.presentations_path).absolute()))
        self.ui.backgrounds_path.setText(str(Path(settings.backgrounds_path).absolute()))
        self.ui.output_path.setText(str(Path(settings.output_path).absolute()))
        # Generation settings.
        self.ui.apply_unsharp.setChecked(self.__settings.unsharp)
        self.ui.override_images.setChecked(self.__settings.override_target_files)

        # Loading image resource lists according conf.
        self.ui.pproducts_view_model.setRootPath(self.ui.main_products_path.text())
        self.ui.sproducts_view_model.setRootPath(self.ui.secondary_products_path.text())
        self.ui.presentations_view_model.setRootPath(self.ui.presentations_path.text())
        self.ui.backgrounds_view_model.setRootPath(self.ui.backgrounds_path.text())

        # Image result settings.
        self.ui.image_result_width.setValue(self.__settings.adaptive_resize_width)
        self.ui.image_result_height.setValue(self.__settings.adaptive_resize_height)

        self.ui.secondary_generation.setChecked(self.__settings.secondary_generation)



        # Setting output dir.
        try:
            self.ui.preview_scene.set_output_dir(self.ui.output_path.text())
        except OutputDirError as err:
            self.ui.output_path.setText("")

        # S3 settings.
        try:
            self.ui.upload_to_s3.setChecked(self.__settings.upload_to_s3)
        except NoOptionError as err:
            self.__settings.set_config_value('upload_to_s3', "True")
            self.ui.upload_to_s3.setChecked(True)

        try:
            self.ui.access_key.setText(self.__settings.s3_access_key)
        except NoOptionError as err:
            self.__settings.set_config_value('s3_access_key', "")

        try:
            self.ui.secret_access_key.setText(self.__settings.s3_secret_key)
        except NoOptionError as err:
            self.__settings.set_config_value('s3_secret_key', "")

        try:
            self.ui.bucket_name.setText(self.__settings.bucket_name)
        except NoOptionError as err:
            self.__settings.set_config_value('bucket_name', "")

        self.__loading_settings = False

    def __settings_changed(self, *args, **kwargs):

        if self.__loading_settings:
            return

        pwd = Path.cwd()

        self.__settings.set_config_value("output_path", self.ui.output_path.text() or f'{pwd}')
        self.__settings.set_config_value("main_products_path", self.ui.main_products_path.text() or f'{pwd}')
        self.__settings.set_config_value("secondary_products_path", self.ui.secondary_products_path.text() or f'{pwd}')
        self.__settings.set_config_value("presentations_path", self.ui.presentations_path.text() or f'{pwd}')
        self.__settings.set_config_value("backgrounds_path", self.ui.backgrounds_path.text() or f'{pwd}')

        self.__settings.set_config_value("unsharp", str(self.ui.apply_unsharp.isChecked()))
        self.__settings.set_config_value("secondary_generation", str(self.ui.secondary_generation.isChecked()))

        self.__settings.set_config_value("override_target_files", str(self.ui.override_images.isChecked()))

        self.__settings.set_config_value("bucket_name", self.ui.bucket_name.text())
        self.__settings.set_config_value("upload_to_s3", str(self.ui.upload_to_s3.isChecked()))

        self.__settings.set_config_value("s3_access_key", self.ui.access_key.text())
        self.__settings.set_config_value("s3_secret_key", self.ui.secret_access_key.text())

        self.__settings.set_config_value("adaptive_resize_width", str(self.ui.image_result_width.value()))
        self.__settings.set_config_value("adaptive_resize_height", str(self.ui.image_result_height.value()))

        self.__settings.save()

    def __prepare_graphic_view(self):
        self.ui.preview_scene = ComposerGraphicScene(self.ui.preview)
        self.ui.preview_scene.selectionChanged.connect(self.on_graphic_item_selection_change)

        self.ui.preview.setScene(self.ui.preview_scene)
        self.ui.preview.acceptDrops()

        self.ui.item_properties.setEnabled(False)

        self.ui.preview_scene.item_moved.connect(self.on_graphic_item_moved)

        self.ui.preview_scene.zoom_selector = None
        self.ui.preview_scene.crop_selector = None

    def __prepare_list_views(self):
        # Models.
        self.ui.pproducts_view_model = ResourceModel(self, origin=PRIMARY)
        self.ui.sproducts_view_model = ResourceModel(self, origin=SECONDARY)
        self.ui.backgrounds_view_model = ResourceModel(self, origin=BACKGROUND)
        self.ui.presentations_view_model = ResourceModel(self, origin=PRESENTATION)

        # Bind models to views.
        self.ui.primary_products_view.setModel(self.ui.pproducts_view_model)
        self.ui.secondary_products_view.setModel(self.ui.sproducts_view_model)
        self.ui.backgrounds_view.setModel(self.ui.backgrounds_view_model)
        self.ui.presentations_view.setModel(self.ui.presentations_view_model)

        # Enable drag on views.
        self.ui.primary_products_view.setDragEnabled(True)
        self.ui.secondary_products_view.setDragEnabled(True)
        self.ui.backgrounds_view.setDragEnabled(True)
        self.ui.presentations_view.setDragEnabled(True)

    def __prepare_property_controls(self):
        self.ui.item_pos_x.valueChanged.connect(self.on_x_changed)
        self.ui.item_pos_y.valueChanged.connect(self.on_y_changed)
        self.ui.item_pos_z.valueChanged.connect(self.on_z_changed)

        self.ui.item_width.valueChanged.connect(self.on_width_changed)
        self.ui.item_height.valueChanged.connect(self.on_height_changed)

    def __selected_item(self):
        items = self.ui.preview_scene.selectedItems()
        if len(items) == 0:
            return None

        assert len(items) == 1
        return items[0]

    @pyqtSlot()
    def busy_mode(self):
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.setMinimum(0)

    @pyqtSlot()
    def normal_mode(self):
        self.ui.progressBar.setMaximum(100)

    @pyqtSlot()
    def on_mproducts_path_select_button_clicked(self, *args, **kwargs):
        path = self.__collect_resource_path(
            self.ui.main_products_path, _("Select main product's images directory.")
        )
        index = self.ui.pproducts_view_model.setRootPath(path)

    @pyqtSlot()
    def on_backgrounds_path_select_button_clicked(self, *args, **kwargs):
        path = self.__collect_resource_path(self.ui.backgrounds_path, _("Select background's images directory."))
        index = self.ui.backgrounds_view_model.setRootPath(path)

    @pyqtSlot()
    def on_sproducts_path_select_button_clicked(self, *args, **kwargs):
        path = self.__collect_resource_path(self.ui.secondary_products_path,
                                            _("Select secondary product's images directory."))
        index = self.ui.sproducts_view_model.setRootPath(path)

    @pyqtSlot()
    def on_presentations_path_select_button_clicked(self, *args, **kwargs):
        path = self.__collect_resource_path(self.ui.presentations_path, _("Select presentations's images directory."))
        index = self.ui.presentations_view_model.setRootPath(path)

    @pyqtSlot()
    def on_output_select_button_clicked(self, *args, **kwargs):
        path = self.__collect_resource_path(self.ui.output_path, _("Select secondary product's images directory."))
        self.ui.preview_scene.set_output_dir(path)

    @pyqtSlot()
    def on_output_path_changed(self):
        try:
            self.ui.preview_scene.set_output_dir(self.ui.output_path.text())
        except OutputDirError as err:
            message = QErrorMessage(self)
            message.showMessage(str(err))
            self.ui.output_path.clear()

    @pyqtSlot()
    def on_generate_template_button_clicked(self):
        path = self.ui.preview_scene.render_template()

        message = QMessageBox(self)
        message.setText(_("Template generated"))
        message.setInformativeText(str(path))

        message.exec()

    def __collect_resource_path(self, edit: QLineEdit, message: str) -> str:
        path = QFileDialog.getExistingDirectory(self, message, directory=edit.text())
        edit.setText(path)
        self.__settings_changed()
        self.__settings.save()
        return path

    def resizeEvent(self, event):
        self.ui.preview.fitInView(self.ui.preview_scene.sceneRect(), Qt.KeepAspectRatio)
        return super(Composer, self).resizeEvent(event)

    def on_graphic_item_selection_change(self):
        selection = self.ui.preview_scene.selectedItems()
        if selection:
            # TODO: Use flag for enable selection for just one item at the time.
            item = selection[0]

            # The item can be scaled to a new size in the process, use that
            # to keep things as the user wants it.
            scale_factor = item.scale()

            # Enable property controls.
            self.ui.item_properties.setEnabled(True)
            self.ui.item_pos_x.setEnabled(True)
            self.ui.item_pos_y.setEnabled(True)
            self.ui.item_height.setEnabled(True)
            self.ui.item_width.setEnabled(True)
            # Get item properties.
            rect = item.boundingRect()
            pos = item.scenePos()
            # Populate property controls.
            self.ui.item_pos_x.setValue(pos.x())
            self.ui.item_pos_y.setValue(pos.y())
            self.ui.item_height.setValue(rect.height() * scale_factor)
            self.ui.item_width.setValue(rect.width() * scale_factor)
        else:
            self.ui.item_properties.setEnabled(False)
            self.ui.item_pos_x.setValue(0)
            self.ui.item_pos_y.setValue(0)
            self.ui.item_height.setValue(0)
            self.ui.item_width.setValue(0)

    def on_graphic_item_moved(self, x, y):
        self.ui.item_pos_x.setValue(x)
        self.ui.item_pos_y.setValue(y)

    def on_x_changed(self, value):
        item = self.__selected_item()
        if item is None:
            # No item selected
            return
        item.setX(value)

    def on_y_changed(self, value):
        item = self.__selected_item()
        if item is None:
            # No item selected
            return
        item.setY(value)

    def on_z_changed(self, value):
        item = self.__selected_item()
        if item is None:
            # No item selected
            return
        item.setZValue(value)

    def on_height_changed(self, height):
        item = self.__selected_item()

        if item is None:
            # No item selected.
            return

        rect = item.boundingRect()

        original_height = rect.height()
        original_width = rect.width()

        factor = float(height / original_height)

        item.prepareGeometryChange()
        item.setScale(factor)
        item.update()

        # Update width control.
        old_state = self.ui.item_width.blockSignals(True)
        self.ui.item_width.setValue(original_width * factor)
        self.ui.item_width.blockSignals(old_state)

    def on_width_changed(self, width):
        item = self.__selected_item()

        if item is None:
            # No item selected.
            return

        rect = item.boundingRect()

        original_width = rect.width()
        original_height = rect.height()

        factor = float(width / original_width)

        item.prepareGeometryChange()
        item.setScale(factor)
        item.update()

        # Update height control.
        old_state = self.ui.item_height.blockSignals(True)
        self.ui.item_height.setValue(original_height * factor)
        self.ui.item_height.blockSignals(old_state)

    @pyqtSlot()
    def on_generate_button_clicked(self, *args, **kwargs):
        template = self.ui.preview_scene.template

        primaries_paths = [Path(resource.path) for resource in self.ui.pproducts_view_model.resources]
        secondaries_paths = [Path(resource.path) for resource in self.ui.sproducts_view_model.resources]
        presentations_paths = [Path(resource.path) for resource in self.ui.presentations_view_model.resources]

        composition_builder = CompositionBuilder(
            template, primaries_paths, secondaries_paths, presentations_paths
        )

        compositions = list(composition_builder.compose())

        output_dir = Path(self.ui.output_path.text())

        options = GenerationOptions(
            unsharp=self.ui.apply_unsharp.isChecked(),
            override_images=self.ui.override_images.isChecked(),
            upload_to_s3=self.ui.upload_to_s3.isChecked(),
            bucket_name=self.ui.bucket_name.text()
        )

        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(len(compositions))

        self._composition_thread = QThread()
        self._composition_worker = ComposeWorker(compositions, options, output_dir)
        self._composition_worker.moveToThread(self._composition_thread)

        self._composition_worker.composition_ready.connect(self.on_composition_ready)
        self._composition_worker.composition_finished.connect(self._composition_thread.quit)
        self._composition_worker.composition_finished.connect(self.on_generation_complete)

        self._composition_worker.composition_uploading_to_s3.connect(self.busy_mode)
        self._composition_worker.composition_uploaded_to_s3.connect(self.normal_mode)

        self._composition_thread.started.connect(self._composition_worker.run)

        self._composition_thread.start()

    @pyqtSlot(str, name="on_composition_ready")
    def on_composition_ready(self, composition_path):
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

    @pyqtSlot(name="on_generation_complete")
    def on_generation_complete(self, *args, **kwargs):

        dialog = QMessageBox(self)
        dialog.setText(_("Generation complete"))
        dialog.setIcon(QMessageBox.Information)
        dialog.exec()

        self.ui.progressBar.setValue(0)

    @pyqtSlot(name="on_using_template_button_clicked")
    def on_using_template_button_clicked(self, *args, **kwargs):
        template_path, filter = QFileDialog.getOpenFileName(self, _("Select template file."), ".",
                                                            "Template files (*.svg)")

        with open(template_path, 'rb') as template_file:
            template = Template()
            template.load_from_file(template_file=template_file)
            self.ui.preview_scene.template = template
            self.on_generate_button_clicked()

    @pyqtSlot(bool)
    def on_area_zoom_action_toggled(self, value):

        if value:

            scene_rect = self.ui.preview_scene.sceneRect()

            handle_size = max([scene_rect.width(), scene_rect.height()]) * 0.01
            handle_space = handle_size / -2

            self.ui.preview_scene.zoom_selector = Selector(
                handle_size, handle_size, scene_rect.width() * 0.25, scene_rect.height() * 0.25,
                handle_size=handle_size, handle_space=handle_space
            )
            self.ui.preview_scene.addItem(self.ui.preview_scene.zoom_selector)

            layer = self._add_selector_layer(self.ui.preview_scene.zoom_selector, LayerType.ZOOM_SELECTION)
            self.ui.preview_scene.template.map_layer_with_item(layer, self.ui.preview_scene.zoom_selector)
        else:
            self.ui.preview_scene.removeItem(self.ui.preview_scene.zoom_selector)
            self.ui.preview_scene.template.remove_layer_for_item(self.ui.preview_scene.zoom_selector)
            self.ui.preview_scene.zoom_selector = None

    @pyqtSlot(bool)
    def on_area_crop_action_toggled(self, value):

        if value:

            scene_rect = self.ui.preview_scene.sceneRect()

            handle_size = max([scene_rect.width(), scene_rect.height()]) * 0.01
            handle_space = handle_size / -2

            self.ui.preview_scene.crop_selector = Selector(
                handle_size, handle_size, scene_rect.width() * 0.25, scene_rect.height() * 0.25, rgb=(0, 0, 255),
                handle_size=handle_size, handle_space=handle_space
            )
            self.ui.preview_scene.addItem(self.ui.preview_scene.crop_selector)

            layer = self._add_selector_layer(self.ui.preview_scene.crop_selector, LayerType.CROP_SELECTION)
            self.ui.preview_scene.template.map_layer_with_item(layer, self.ui.preview_scene.crop_selector)

        else:
            self.ui.preview_scene.removeItem(self.ui.preview_scene.crop_selector)
            self.ui.preview_scene.template.remove_layer_for_item(self.ui.preview_scene.crop_selector)
            self.ui.preview_scene.crop_selector = None

    def _add_selector_layer(self, selector, layer_type) -> Layer:

        pos = Position(selector.x(), selector.y(), selector.zValue())

        size = Size(
            selector.boundingRect().width(),
            selector.boundingRect().height()
        )

        layer = self.ui.preview_scene.template.add_layer(pos=pos, size=size, _type=layer_type)

        return layer

    @pyqtSlot()
    def on_cancel_button_clicked(self):
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    composer = Composer()
    composer.show()

    app.exec()
