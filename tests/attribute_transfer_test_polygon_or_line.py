#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-18 18:40:50
# @Author  : Michal Zimmermann <zimmicz@gmail.com>

import os
import sip
import sys
import unittest
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer, QgsFeature, QgsGeometry, QgsPoint
from utilities import get_qgis_app

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from attribute_transfer import AttributeTransfer
from create_dummy_data import create_dummy_data_polygon_or_line

sip.setapi('QtCore', 2)
sip.setapi('QString', 2)
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)

QGIS_APP = get_qgis_app()
IFACE = QGIS_APP[2]


class AttributeTransferTestPolygonOrLine(unittest.TestCase):

    def setUp(self):
        self.source_layer = QgsVectorLayer(
            "Polygon?crs=epsg:4326&field=id:integer&field=textAttr:string&field=intAttr:integer&field=decAttr:double&field=dateAttr:date&index=yes", "source layer", "memory")
        self.target_layer = QgsVectorLayer(
            "Linestring?crs=epsg:4326&field=id:integer&index=yes", "target layer", "memory")
        self.widget = AttributeTransfer(IFACE)

        registry = QgsMapLayerRegistry.instance()
        registry.removeAllMapLayers()
        registry.addMapLayers([self.source_layer, self.target_layer])
        create_dummy_data_polygon_or_line(self.source_layer, self.target_layer)
        self.widget.initGui()
        self.widget.vectors = [self.source_layer, self.target_layer]
        self.widget.editable_vectors = [self.source_layer, self.target_layer]
        self.widget.dlg.sourceLayer.addItems(["source layer", "target layer"])

    def test_text_attr(self):
        ATTRIBUTE_NAME = "textAttr"
        ATTRIBUTE_INDEX = 1

        self._test_attr(ATTRIBUTE_NAME, ATTRIBUTE_INDEX)

    def test_int_attr(self):
        ATTRIBUTE_NAME = "intAttr"
        ATTRIBUTE_INDEX = 2

        self._test_attr(ATTRIBUTE_NAME, ATTRIBUTE_INDEX)

    def test_dec_attr(self):
        ATTRIBUTE_NAME = "decAttr"
        ATTRIBUTE_INDEX = 3

        self._test_attr(ATTRIBUTE_NAME, ATTRIBUTE_INDEX)

    def test_date_attr(self):
        ATTRIBUTE_NAME = "dateAttr"
        ATTRIBUTE_INDEX = 4

        self._test_attr(ATTRIBUTE_NAME, ATTRIBUTE_INDEX)

    def test_existing_attr(self):
        ATTRIBUTE_NAME = "id"
        ATTRIBUTE_INDEX = 0

        self.widget.dlg.sourceAttribute.setCurrentIndex(ATTRIBUTE_INDEX)
        self.widget.dlg.targetAttribute.setText(ATTRIBUTE_NAME)

        self.assertEqual(
            self.widget.dlg.sourceAttribute.currentText(), ATTRIBUTE_NAME)
        self.assertFalse(self.widget.transfer())

    def _test_attr(self, attr_name, attr_index):
        self.widget.dlg.sourceAttribute.setCurrentIndex(attr_index)
        self.widget.dlg.targetAttribute.setText(attr_name)

        self.assertEqual(
            self.widget.dlg.sourceAttribute.currentText(), attr_name)

        self.widget.transfer()

        target_fields = [f.name()
                         for f in self.target_layer.dataProvider().fields()]
        self.assertIn(attr_name, target_fields)

        source_features = [f for f in self.source_layer.getFeatures()]
        target_features = [f for f in self.target_layer.getFeatures()]

        for idx, f in enumerate(source_features):
            self.assertEqual(f.attribute(attr_name), target_features[
                             idx].attribute(attr_name))


if __name__ == "__main__":
    unittest.main()
