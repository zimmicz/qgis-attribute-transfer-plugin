#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-18 18:40:50
# @Author  : Michal Zimmermann <zimmicz@gmail.com>

from qgis.core import QgsGeometry, QgsPoint, QgsRectangle

def get_points_from_bbox(bbox):
    return [
        QgsGeometry.fromPoint(QgsPoint(bbox.xMinimum(), bbox.yMaximum())),
        QgsGeometry.fromPoint(QgsPoint(bbox.xMaximum(), bbox.yMaximum())),
        QgsGeometry.fromPoint(QgsPoint(bbox.xMaximum(), bbox.yMinimum())),
        QgsGeometry.fromPoint(QgsPoint(bbox.xMinimum(), bbox.yMinimum()))
    ]

def bbox_from_centroid(centroid, distance):
    x = centroid.asPoint().x()
    y = centroid.asPoint().y()
    ul = QgsPoint(x - distance, y + distance)
    lr = QgsPoint(x + distance, y - distance)
    return QgsRectangle(ul, lr)

def longest_distance_to_vertex(geom, vertices):
    distance = None

    for v in vertices:
        d = geom.distance(v)
        if distance is None or d > distance:
            distance = d

    return distance
