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
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AttributeTransfer class from file AttributeTransfer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .attribute_transfer import AttributeTransfer
    return AttributeTransfer(iface)
