from gettext import gettext as _
from pathlib import Path

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLineEdit, QErrorMessage

from composer_core.composer.composition import CompositionBuilder
from models.template import OutputDirError, Template
from ui.common import PRIMARY, SECONDARY, BACKGROUND, PRESENTATION, GenerationOptions
from ui.composer_graphic_scene import ComposerGraphicScene
from ui.imagecomposer import Ui_Imagecomposer
from ui.models import ResourceModel


class Composer(QMainWindow):

    def __init__(self, parent=None):
        super(Composer, self).__init__(parent=parent)
        # initializing ui components.
        self.ui = Ui_Imagecomposer()
        self.ui.setupUi(self)

        self.ui.output_path.editingFinished.connect(self.on_output_path_changed)

        self.__prepare_list_views()
        self.__prepare_graphic_view()
        self.__prepare_property_controls()

    def __prepare_graphic_view(self):
        self.ui.preview_scene = ComposerGraphicScene(self.ui.preview)
        self.ui.preview_scene.selectionChanged.connect(self.on_graphic_item_selection_change)

        self.ui.preview.setScene(self.ui.preview_scene)
        self.ui.preview.acceptDrops()

        self.ui.item_properties.setEnabled(False)

        self.ui.preview_scene.item_moved.connect(self.on_graphic_item_moved)

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
        self.ui.preview_scene.render_template()

    def __collect_resource_path(self, edit: QLineEdit, message: str) -> str:
        path = QFileDialog.getExistingDirectory(self, message)
        edit.setText(path)
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

        composition_builder = CompositionBuilder(template,
                                                 primaries_paths, secondaries_paths, presentations_paths)

        compositions = composition_builder.compose()

        output_dir = Path(self.ui.output_path.text())

        options = GenerationOptions(
            unsharp=self.ui.apply_unsharp.isChecked()
        )

        for composition in compositions:
            if composition.is_valid():
                composition.render(options, output_path=output_dir)

    @pyqtSlot()
    def on_using_template_button_clicked(self, *args, **kwargs):
        template_path, filter = QFileDialog.getOpenFileName(self, _("Select template file."), ".",
                                                            "Template files (*.svg)")

        with open(template_path, 'rb') as template_file:
            template = Template()
            template.load_from_file(template_file=template_file)
            self.ui.preview_scene.template = template
            self.on_generate_button_clicked()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    composer = Composer()
    composer.show()

    app.exec()
