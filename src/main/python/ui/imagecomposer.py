# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imagecomposer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Imagecomposer(object):
    def setupUi(self, Imagecomposer):
        Imagecomposer.setObjectName("Imagecomposer")
        Imagecomposer.resize(1498, 908)
        self.centralWidget = QtWidgets.QWidget(Imagecomposer)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mproducts_path_select_button = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mproducts_path_select_button.sizePolicy().hasHeightForWidth())
        self.mproducts_path_select_button.setSizePolicy(sizePolicy)
        self.mproducts_path_select_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.mproducts_path_select_button.setObjectName("mproducts_path_select_button")
        self.gridLayout.addWidget(self.mproducts_path_select_button, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.sproducts_path_select_button = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sproducts_path_select_button.sizePolicy().hasHeightForWidth())
        self.sproducts_path_select_button.setSizePolicy(sizePolicy)
        self.sproducts_path_select_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.sproducts_path_select_button.setObjectName("sproducts_path_select_button")
        self.gridLayout.addWidget(self.sproducts_path_select_button, 1, 3, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.backgrounds_path = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backgrounds_path.sizePolicy().hasHeightForWidth())
        self.backgrounds_path.setSizePolicy(sizePolicy)
        self.backgrounds_path.setObjectName("backgrounds_path")
        self.gridLayout.addWidget(self.backgrounds_path, 3, 1, 1, 2)
        self.backgrounds_path_select_button = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backgrounds_path_select_button.sizePolicy().hasHeightForWidth())
        self.backgrounds_path_select_button.setSizePolicy(sizePolicy)
        self.backgrounds_path_select_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.backgrounds_path_select_button.setObjectName("backgrounds_path_select_button")
        self.gridLayout.addWidget(self.backgrounds_path_select_button, 3, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.output_path = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_path.sizePolicy().hasHeightForWidth())
        self.output_path.setSizePolicy(sizePolicy)
        self.output_path.setObjectName("output_path")
        self.gridLayout.addWidget(self.output_path, 4, 1, 1, 2)
        self.output_select_button = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_select_button.sizePolicy().hasHeightForWidth())
        self.output_select_button.setSizePolicy(sizePolicy)
        self.output_select_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.output_select_button.setObjectName("output_select_button")
        self.gridLayout.addWidget(self.output_select_button, 4, 3, 1, 1)
        self.presentations_path_select_button = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.presentations_path_select_button.sizePolicy().hasHeightForWidth())
        self.presentations_path_select_button.setSizePolicy(sizePolicy)
        self.presentations_path_select_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.presentations_path_select_button.setObjectName("presentations_path_select_button")
        self.gridLayout.addWidget(self.presentations_path_select_button, 2, 3, 1, 1)
        self.presentations_path = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.presentations_path.sizePolicy().hasHeightForWidth())
        self.presentations_path.setSizePolicy(sizePolicy)
        self.presentations_path.setObjectName("presentations_path")
        self.gridLayout.addWidget(self.presentations_path, 2, 1, 1, 2)
        self.secondary_products_path = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.secondary_products_path.sizePolicy().hasHeightForWidth())
        self.secondary_products_path.setSizePolicy(sizePolicy)
        self.secondary_products_path.setObjectName("secondary_products_path")
        self.gridLayout.addWidget(self.secondary_products_path, 1, 1, 1, 2)
        self.main_products_path = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_products_path.sizePolicy().hasHeightForWidth())
        self.main_products_path.setSizePolicy(sizePolicy)
        self.main_products_path.setObjectName("main_products_path")
        self.gridLayout.addWidget(self.main_products_path, 0, 1, 1, 2)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.item_properties = QtWidgets.QGroupBox(self.centralWidget)
        self.item_properties.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_properties.sizePolicy().hasHeightForWidth())
        self.item_properties.setSizePolicy(sizePolicy)
        self.item_properties.setMinimumSize(QtCore.QSize(0, 0))
        self.item_properties.setMaximumSize(QtCore.QSize(350, 16777215))
        self.item_properties.setObjectName("item_properties")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.item_properties)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_9 = QtWidgets.QLabel(self.item_properties)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.item_width = QtWidgets.QSpinBox(self.item_properties)
        self.item_width.setEnabled(True)
        self.item_width.setMinimumSize(QtCore.QSize(100, 0))
        self.item_width.setMaximum(1000000)
        self.item_width.setObjectName("item_width")
        self.horizontalLayout_4.addWidget(self.item_width)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 3)
        self.label_14 = QtWidgets.QLabel(self.item_properties)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 3, 1, 1)
        self.item_pos_x = QtWidgets.QSpinBox(self.item_properties)
        self.item_pos_x.setEnabled(True)
        self.item_pos_x.setMinimumSize(QtCore.QSize(100, 0))
        self.item_pos_x.setMaximum(1000000)
        self.item_pos_x.setObjectName("item_pos_x")
        self.gridLayout_2.addWidget(self.item_pos_x, 0, 4, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.item_properties)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 1, 0, 1, 2)
        self.item_height = QtWidgets.QSpinBox(self.item_properties)
        self.item_height.setEnabled(True)
        self.item_height.setMinimumSize(QtCore.QSize(100, 0))
        self.item_height.setMaximum(1000000)
        self.item_height.setObjectName("item_height")
        self.gridLayout_2.addWidget(self.item_height, 1, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.item_properties)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 1, 3, 1, 1)
        self.item_pos_y = QtWidgets.QSpinBox(self.item_properties)
        self.item_pos_y.setEnabled(True)
        self.item_pos_y.setMinimumSize(QtCore.QSize(100, 0))
        self.item_pos_y.setMaximum(1000000)
        self.item_pos_y.setObjectName("item_pos_y")
        self.gridLayout_2.addWidget(self.item_pos_y, 1, 4, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.item_properties)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        self.item_angle = QtWidgets.QSpinBox(self.item_properties)
        self.item_angle.setEnabled(True)
        self.item_angle.setMinimumSize(QtCore.QSize(100, 0))
        self.item_angle.setMaximum(1000000)
        self.item_angle.setObjectName("item_angle")
        self.gridLayout_2.addWidget(self.item_angle, 2, 1, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.item_properties)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 2, 3, 1, 1)
        self.item_pos_z = QtWidgets.QSpinBox(self.item_properties)
        self.item_pos_z.setEnabled(True)
        self.item_pos_z.setMinimumSize(QtCore.QSize(100, 0))
        self.item_pos_z.setMaximum(1000000)
        self.item_pos_z.setObjectName("item_pos_z")
        self.gridLayout_2.addWidget(self.item_pos_z, 2, 4, 1, 1)
        self.horizontalLayout_2.addWidget(self.item_properties)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.primary_products_view = QtWidgets.QListView(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(220)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.primary_products_view.sizePolicy().hasHeightForWidth())
        self.primary_products_view.setSizePolicy(sizePolicy)
        self.primary_products_view.setMinimumSize(QtCore.QSize(220, 0))
        self.primary_products_view.setMaximumSize(QtCore.QSize(220, 16777215))
        self.primary_products_view.setDragEnabled(True)
        self.primary_products_view.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.primary_products_view.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.primary_products_view.setFlow(QtWidgets.QListView.TopToBottom)
        self.primary_products_view.setProperty("isWrapping", False)
        self.primary_products_view.setViewMode(QtWidgets.QListView.IconMode)
        self.primary_products_view.setObjectName("primary_products_view")
        self.verticalLayout.addWidget(self.primary_products_view)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.secondary_products_view = QtWidgets.QListView(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(220)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.secondary_products_view.sizePolicy().hasHeightForWidth())
        self.secondary_products_view.setSizePolicy(sizePolicy)
        self.secondary_products_view.setMinimumSize(QtCore.QSize(220, 0))
        self.secondary_products_view.setMaximumSize(QtCore.QSize(220, 16777215))
        self.secondary_products_view.setDragEnabled(True)
        self.secondary_products_view.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.secondary_products_view.setFlow(QtWidgets.QListView.TopToBottom)
        self.secondary_products_view.setProperty("isWrapping", False)
        self.secondary_products_view.setViewMode(QtWidgets.QListView.IconMode)
        self.secondary_products_view.setObjectName("secondary_products_view")
        self.verticalLayout_2.addWidget(self.secondary_products_view)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_3.addWidget(self.label_16)
        self.presentations_view = QtWidgets.QListView(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(220)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.presentations_view.sizePolicy().hasHeightForWidth())
        self.presentations_view.setSizePolicy(sizePolicy)
        self.presentations_view.setMinimumSize(QtCore.QSize(220, 0))
        self.presentations_view.setMaximumSize(QtCore.QSize(220, 16777215))
        self.presentations_view.setDragEnabled(True)
        self.presentations_view.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.presentations_view.setFlow(QtWidgets.QListView.TopToBottom)
        self.presentations_view.setProperty("isWrapping", False)
        self.presentations_view.setViewMode(QtWidgets.QListView.IconMode)
        self.presentations_view.setObjectName("presentations_view")
        self.verticalLayout_3.addWidget(self.presentations_view)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.backgrounds_view = QtWidgets.QListView(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(220)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backgrounds_view.sizePolicy().hasHeightForWidth())
        self.backgrounds_view.setSizePolicy(sizePolicy)
        self.backgrounds_view.setMinimumSize(QtCore.QSize(220, 0))
        self.backgrounds_view.setMaximumSize(QtCore.QSize(220, 16777215))
        self.backgrounds_view.setDragEnabled(True)
        self.backgrounds_view.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.backgrounds_view.setFlow(QtWidgets.QListView.TopToBottom)
        self.backgrounds_view.setProperty("isWrapping", False)
        self.backgrounds_view.setViewMode(QtWidgets.QListView.IconMode)
        self.backgrounds_view.setObjectName("backgrounds_view")
        self.verticalLayout_4.addWidget(self.backgrounds_view)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.preview = QtWidgets.QGraphicsView(self.tab)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.preview.setBackgroundBrush(brush)
        self.preview.setObjectName("preview")
        self.verticalLayout_5.addWidget(self.preview)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_8.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.apply_unsharp = QtWidgets.QCheckBox(self.groupBox_2)
        self.apply_unsharp.setChecked(True)
        self.apply_unsharp.setObjectName("apply_unsharp")
        self.verticalLayout_8.addWidget(self.apply_unsharp)
        self.override_images = QtWidgets.QCheckBox(self.groupBox_2)
        self.override_images.setChecked(True)
        self.override_images.setObjectName("override_images")
        self.verticalLayout_8.addWidget(self.override_images)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label_20 = QtWidgets.QLabel(self.groupBox_2)
        self.label_20.setObjectName("label_20")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.image_result_width = QtWidgets.QSpinBox(self.groupBox_2)
        self.image_result_width.setMaximum(10000)
        self.image_result_width.setProperty("value", 1500)
        self.image_result_width.setObjectName("image_result_width")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.image_result_width)
        self.label_21 = QtWidgets.QLabel(self.groupBox_2)
        self.label_21.setObjectName("label_21")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.image_result_height = QtWidgets.QSpinBox(self.groupBox_2)
        self.image_result_height.setMaximum(10000)
        self.image_result_height.setProperty("value", 1500)
        self.image_result_height.setObjectName("image_result_height")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.image_result_height)
        self.verticalLayout_8.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem)
        self.gridLayout_5.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_17 = QtWidgets.QLabel(self.groupBox_3)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 0, 0, 1, 1)
        self.access_key = QtWidgets.QLineEdit(self.groupBox_3)
        self.access_key.setObjectName("access_key")
        self.gridLayout_4.addWidget(self.access_key, 0, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_3)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 1, 0, 1, 1)
        self.secret_access_key = QtWidgets.QLineEdit(self.groupBox_3)
        self.secret_access_key.setObjectName("secret_access_key")
        self.gridLayout_4.addWidget(self.secret_access_key, 1, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox_3)
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 2, 0, 1, 1)
        self.bucket_name = QtWidgets.QLineEdit(self.groupBox_3)
        self.bucket_name.setObjectName("bucket_name")
        self.gridLayout_4.addWidget(self.bucket_name, 2, 1, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout_4)
        self.upload_to_s3 = QtWidgets.QCheckBox(self.groupBox_3)
        self.upload_to_s3.setChecked(True)
        self.upload_to_s3.setObjectName("upload_to_s3")
        self.verticalLayout_7.addWidget(self.upload_to_s3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.gridLayout_5.addWidget(self.groupBox_3, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem3, 1, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_6.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBar.setMinimumSize(QtCore.QSize(850, 0))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.cancel_button = QtWidgets.QPushButton(self.centralWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.generate_button = QtWidgets.QPushButton(self.centralWidget)
        self.generate_button.setObjectName("generate_button")
        self.horizontalLayout.addWidget(self.generate_button)
        self.using_template_button = QtWidgets.QPushButton(self.centralWidget)
        self.using_template_button.setObjectName("using_template_button")
        self.horizontalLayout.addWidget(self.using_template_button)
        self.generate_template_button = QtWidgets.QPushButton(self.centralWidget)
        self.generate_template_button.setObjectName("generate_template_button")
        self.horizontalLayout.addWidget(self.generate_template_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        Imagecomposer.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(Imagecomposer)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1498, 24))
        self.menuBar.setObjectName("menuBar")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        Imagecomposer.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(Imagecomposer)
        self.mainToolBar.setObjectName("mainToolBar")
        Imagecomposer.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(Imagecomposer)
        self.statusBar.setObjectName("statusBar")
        Imagecomposer.setStatusBar(self.statusBar)
        self.area_zoom_action = QtWidgets.QAction(Imagecomposer)
        self.area_zoom_action.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-zoom-para-extensión-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.area_zoom_action.setIcon(icon)
        self.area_zoom_action.setObjectName("area_zoom_action")
        self.area_crop_action = QtWidgets.QAction(Imagecomposer)
        self.area_crop_action.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/icons8-cupón-para-recortar-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.area_crop_action.setIcon(icon1)
        self.area_crop_action.setObjectName("area_crop_action")
        self.menuTools.addAction(self.area_zoom_action)
        self.menuTools.addAction(self.area_crop_action)
        self.menuBar.addAction(self.menuTools.menuAction())
        self.mainToolBar.addAction(self.area_zoom_action)
        self.mainToolBar.addAction(self.area_crop_action)

        self.retranslateUi(Imagecomposer)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Imagecomposer)

    def retranslateUi(self, Imagecomposer):
        _translate = QtCore.QCoreApplication.translate
        Imagecomposer.setWindowTitle(_translate("Imagecomposer", "Imagecomposer"))
        self.groupBox.setTitle(_translate("Imagecomposer", "Resources"))
        self.label.setText(_translate("Imagecomposer", "Main products:"))
        self.mproducts_path_select_button.setText(_translate("Imagecomposer", "..."))
        self.label_2.setText(_translate("Imagecomposer", "Secondary products:"))
        self.sproducts_path_select_button.setText(_translate("Imagecomposer", "..."))
        self.label_15.setText(_translate("Imagecomposer", "Presentations options:"))
        self.label_3.setText(_translate("Imagecomposer", "Backgrounds:"))
        self.backgrounds_path_select_button.setText(_translate("Imagecomposer", "..."))
        self.label_4.setText(_translate("Imagecomposer", "Output:"))
        self.output_select_button.setText(_translate("Imagecomposer", "..."))
        self.presentations_path_select_button.setText(_translate("Imagecomposer", "..."))
        self.item_properties.setTitle(_translate("Imagecomposer", "Item properties"))
        self.label_9.setText(_translate("Imagecomposer", "Width:"))
        self.label_14.setText(_translate("Imagecomposer", "Pos X:"))
        self.label_13.setText(_translate("Imagecomposer", "Height:"))
        self.label_12.setText(_translate("Imagecomposer", "Pos Y:"))
        self.label_10.setText(_translate("Imagecomposer", "Angle:"))
        self.label_11.setText(_translate("Imagecomposer", "Pos Z:"))
        self.label_5.setText(_translate("Imagecomposer", "Main products"))
        self.label_6.setText(_translate("Imagecomposer", "Secondary products"))
        self.label_16.setText(_translate("Imagecomposer", "Presentation options"))
        self.label_7.setText(_translate("Imagecomposer", "Backgrounds"))
        self.label_8.setText(_translate("Imagecomposer", "Preview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Imagecomposer", "Image composition"))
        self.groupBox_2.setTitle(_translate("Imagecomposer", "Image generation"))
        self.apply_unsharp.setText(_translate("Imagecomposer", "Apply unsharp"))
        self.override_images.setText(_translate("Imagecomposer", "Overwrite target files"))
        self.label_20.setText(_translate("Imagecomposer", "Width"))
        self.label_21.setText(_translate("Imagecomposer", "Height"))
        self.groupBox_3.setTitle(_translate("Imagecomposer", "S3"))
        self.label_17.setText(_translate("Imagecomposer", "s3_access_key"))
        self.label_18.setText(_translate("Imagecomposer", "s3_secret_access_key"))
        self.label_19.setText(_translate("Imagecomposer", "Bucket name"))
        self.upload_to_s3.setText(_translate("Imagecomposer", "Upload to s3"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Imagecomposer", "Advanced options"))
        self.cancel_button.setText(_translate("Imagecomposer", "Cancel"))
        self.generate_button.setText(_translate("Imagecomposer", "Generate"))
        self.using_template_button.setText(_translate("Imagecomposer", "Generate using existing template"))
        self.generate_template_button.setText(_translate("Imagecomposer", "Generate template"))
        self.menuTools.setTitle(_translate("Imagecomposer", "Tools"))
        self.area_zoom_action.setText(_translate("Imagecomposer", "Zoom area selection"))
        self.area_zoom_action.setToolTip(_translate("Imagecomposer", "Select area from zoom"))
        self.area_zoom_action.setShortcut(_translate("Imagecomposer", "Ctrl+Shift+Z"))
        self.area_crop_action.setText(_translate("Imagecomposer", "Crop are selection"))
        self.area_crop_action.setToolTip(_translate("Imagecomposer", "Crop area selection"))
        self.area_crop_action.setShortcut(_translate("Imagecomposer", "Ctrl+Shift+X"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Imagecomposer = QtWidgets.QMainWindow()
    ui = Ui_Imagecomposer()
    ui.setupUi(Imagecomposer)
    Imagecomposer.show()
    sys.exit(app.exec_())

