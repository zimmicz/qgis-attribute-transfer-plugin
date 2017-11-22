#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-18 18:40:50
# @Author  : Michal Zimmermann <zimmicz@gmail.com>

from qgis.core import QgsFeature, QgsPoint, QgsGeometry


def create_dummy_data_point(source_layer, target_layer):
    source_layer.startEditing()
    target_layer.startEditing()

    feature = QgsFeature(source_layer.pendingFields())

    for i in range(10):
        feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(i, i)))
        feature.setAttribute("id", i)
        feature.setAttribute("textAttr", "text {}".format(i))
        feature.setAttribute("intAttr", i)
        feature.setAttribute("decAttr", "{:04.2f}".format(i))
        feature.setAttribute("dateAttr", "2017-11-18")
        source_layer.addFeature(feature)

    feature = QgsFeature(target_layer.pendingFields())

    for i in range(10):
        feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(i, i)))
        feature.setAttribute("id", i)
        target_layer.addFeature(feature)

    source_layer.commitChanges()
    target_layer.commitChanges()

def create_dummy_data_polygon_or_line(source_layer, target_layer):
    coordinates = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
    source_layer.startEditing()
    target_layer.startEditing()

    source_feature = QgsFeature(source_layer.pendingFields())
    for i in range(10):
        wkt = ", ".join([" ".join([str(x[0] + i), str(x[1] + i)]) for x in coordinates])
        source_feature.setGeometry(QgsGeometry.fromWkt("POLYGON(({}))".format(wkt)))
        source_feature.setAttribute("id", i)
        source_feature.setAttribute("textAttr", "text {}".format(i))
        source_feature.setAttribute("intAttr", i)
        source_feature.setAttribute("decAttr", "{:04.2f}".format(i))
        source_feature.setAttribute("dateAttr", "2017-11-18")
        source_layer.addFeature(source_feature)

    target_feature = QgsFeature(target_layer.pendingFields())

    for i in range(10):
        wkt = ", ".join([" ".join([str(x[0] + 0.5 + i), str(x[1] + i)]) for x in coordinates[0:2]])
        target_feature.setGeometry(QgsGeometry.fromWkt("LINESTRING({})".format(wkt)))
        target_feature.setAttribute("id", i)
        target_layer.addFeature(target_feature)

    source_layer.commitChanges()
    target_layer.commitChanges()
