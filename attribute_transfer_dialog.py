# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AttributeTransferDialog
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

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'attribute_transfer_dialog_base.ui'))


class AttributeTransferDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(AttributeTransferDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
