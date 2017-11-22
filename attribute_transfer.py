# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AttributeTransfer
                                 A QGIS plugin
 Transfers attribute values from source to target layer.
                              -------------------
        begin                : 2017-11-14
        git sha              : 22bb77ff067da4fa1e88c1542a67f4ddca14f470
        copyright            : (C) 2017 by Michal Zimmermann
        email                : zimmicz@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QgsMapLayerRegistry, QgsVectorDataProvider, QgsField, QgsSpatialIndex
from qgis.gui import QgsMessageBar
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt4.QtGui import QAction, QIcon, QDialogButtonBox
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from attribute_transfer_dialog import AttributeTransferDialog
import os.path


class AttributeTransfer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.vectors = []
        self.editable_vectors = []
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value(
            'locale/userLocale') and QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AttributeTransfer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&AttributeTransfer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AttributeTransfer')
        # self.toolbar.setObjectName(u'AttributeTransfer')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AttributeTransfer', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = AttributeTransferDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar and self.toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/AttributeTransfer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'AttributeTransfer'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg.sourceLayer.currentIndexChanged.connect(
            self._update_editable_vectors)
        self.dlg.sourceLayer.currentIndexChanged.connect(
            self._load_source_attributes)
        self.dlg.targetAttribute.textChanged.connect(self._toggle_ok_button)
        self.dlg.targetLayer.currentIndexChanged.connect(
            self._toggle_ok_button)
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&AttributeTransfer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        self.dlg.sourceLayer.clear()
        self.dlg.targetLayer.clear()
        self.dlg.sourceAttribute.clear()
        self.dlg.targetAttribute.clear()

        registry = QgsMapLayerRegistry.instance()
        self.vectors = [registry.mapLayer(
            id) for id in registry.mapLayers() if registry.mapLayer(id).type() == 0]
        self.editable_vectors = [v for v in self.vectors if v.dataProvider(
        ).capabilities() & QgsVectorDataProvider.AddAttributes]

        sorted(self.vectors, key=lambda v: v.name())
        sorted(self.editable_vectors, key=lambda v: v.name())

        self.dlg.sourceLayer.addItems([v.name() for v in self.vectors])

        result = self.dlg.exec_()

        if result:
            self.transfer()

    def transfer(self):
        source_layer = self.vectors[self.dlg.sourceLayer.currentIndex()]
        target_layer = QgsMapLayerRegistry.instance().mapLayersByName(
            self.dlg.targetLayer.currentText())[0]
        source_attribute_name = self.dlg.sourceAttribute.currentText()
        target_attribute_name = self.dlg.targetAttribute.text()

        def create_target_attribute():
            source_attribute_type = source_layer.dataProvider().fields().at(
                source_layer.fieldNameIndex(source_attribute_name)).type()
            target_attr = QgsField(target_attribute_name)
            target_attr.setType(source_attribute_type)
            return target_layer.addAttribute(target_attr)

        def load_data():
            # 0 = point, 1 = line, 2 = polygon
            valid_types = [0, 1, 2]
            source_geom_type = source_layer.geometryType()
            target_geom_type = target_layer.geometryType()

            def _load_point_data():
                if target_geom_type == 0:
                    """Point target layer. It is safe to create index on source layer."""
                    spatial_index = QgsSpatialIndex(source_layer.getFeatures())
                    source_features = {feature.id(): feature for (
                    feature) in source_layer.getFeatures()}
                    target_features = target_layer.getFeatures()
                else:
                    """Point source layer and non-point target layer. It is safe
                    to switch layers and do the same as in previous situation."""
                    spatial_index = QgsSpatialIndex(target_layer.getFeatures())
                    source_features = {feature.id(): feature for (
                    feature) in target_layer.getFeatures()}
                    target_features = source_layer.getFeatures()

                for f in target_features:
                    nearest = spatial_index.nearestNeighbor(
                        f.geometry().asPoint(), 1)[0]
                    if target_geom_type == 0:
                        value = source_features[
                        nearest].attribute(source_attribute_name)
                    else:
                        value = target_features[
                        nearest].attribute(source_attribute_name)
                    # look for the last attribute in the attribute list
                    if not target_layer.changeAttributeValue(f.id(), max(target_layer.attributeList()), value):
                        return False
                return True

            def _load_polygon_or_line_data():
                spatial_index = QgsSpatialIndex(source_layer.getFeatures())
                source_features = {feature.id(): feature for (
                feature) in source_layer.getFeatures()}
                target_features = target_layer.getFeatures()
                distance = None
                value = None

                for tf in target_features:
                    ids = spatial_index.intersects(tf.geometry().boundingBox())
                    for id in ids:
                        f = source_features[id]
                        d = f.geometry().distance(tf.geometry())

                        if distance is None or d < distance:
                            distance = d
                            value = f.attribute(source_attribute_name)

                    result = target_layer.changeAttributeValue(tf.id(), max(target_layer.attributeList()), value)
                    distance = None
                    value = None
                return result

            if source_geom_type not in valid_types or target_geom_type not in valid_types:
                self.iface.messageBar().pushMessage("Error",
                                                    u"Unknown geometry type found.", level=QgsMessageBar.CRITICAL)
                return False

            if source_geom_type == 0 or target_geom_type == 0:
               return  _load_point_data()
            else:
                return _load_polygon_or_line_data()

        target_layer.startEditing()
        if create_target_attribute():
            if not load_data():
                self.iface.messageBar().pushMessage("Error",
                                                    u"Attribute values transfer failed for an unknown reason.", level=QgsMessageBar.CRITICAL)
                target_layer.rollBack()
                return False
            self.iface.messageBar().pushMessage(
                "Success", u"Attribute transfer succeeded.", level=QgsMessageBar.SUCCESS)
            target_layer.commitChanges()
            return True
        else:
            self.iface.messageBar().pushMessage("Error",
                                                u"Target layer attribute creation failed. It might already exist and won't be overwritten.", level=QgsMessageBar.CRITICAL)
            target_layer.rollBack()
            return False

    def _update_editable_vectors(self):
        current_vector = self.dlg.sourceLayer.currentText()
        filtered = [v.name()
                    for v in self.editable_vectors if v.name() != current_vector]
        self.dlg.targetLayer.clear()
        self.dlg.targetLayer.addItems(filtered)

    def _load_source_attributes(self):
        fields = [f.name() for f in self.vectors[
            self.dlg.sourceLayer.currentIndex()].dataProvider().fields()]
        self.dlg.sourceAttribute.clear()
        self.dlg.sourceAttribute.addItems(fields)

    def _toggle_ok_button(self):
        if self.dlg.targetLayer.currentText() and self.dlg.targetAttribute.text():
            self.dlg.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.dlg.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
