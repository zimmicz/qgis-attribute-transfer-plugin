#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-18 18:40:50
# @Author  : Michal Zimmermann <zimmicz@gmail.com>

from qgis.core import QgsFeature, QgsPoint, QgsGeometry


def create_dummy_data(source_layer, target_layer):

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
