#!/usr/bin/env python
import sys
import logging
import resources

# import app classes
from app.client import OpcClient
from gui.widgets import TreeViewModel

from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


ORGANIZATION_NAME = 'WIIM'
ORGANIZATION_DOMAIN = 'joseafga.com.br'
APPLICATION_NAME = 'Wiim'

logger = logging.getLogger(__name__)


class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        uic.loadUi('gui/main_window.ui', self)

        global icons

        # self.treeView = QTreeView()
        # create opcua tree view model
        self.model = TreeViewModel(icons)
        self.model.set_root_node(data)
        # self.addItems(self.model, data)
        self.treeView.setModel(self.model)

        self.model.setHorizontalHeaderLabels([self.tr("Object")])

    def addItems(self, parent, elements):
        for text, children in elements:
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                self.addItems(item, children)


if __name__ == '__main__':
    global icons
    icons = {
        "folder": QIcon(":/images/icons/svg/folder.svg"),
        "object": QIcon(":/images/icons/svg/tree_structure.svg"),
        "property": QIcon(":/images/icons/svg/info.svg"),
        "variable": QIcon(":/images/icons/svg/ratings.svg"),
        "method": QIcon(":/images/icons/svg/info.svg"),
        "object_type": QIcon(":/images/icons/svg/tree_structure.svg"),
        "variable_type": QIcon(":/images/icons/svg/ratings.svg"),
        "data_type": QIcon(":/images/icons/svg/ratings.svg"),
        "reference_type": QIcon(":/images/icons/svg/info.svg")
    }

    client = OpcClient()
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    # client.connect()
    # exit()

    try:
        client.connect('opc.tcp://opcuademo.sterfive.com:26543')
        data = client.client.get_root_node()

        # endp = client.get_endpoints('opc.tcp://opcua.demo-this.com:51210/UA/SampleServer')
        # print(endp)

        # Client has a few methods to get proxy to UA nodes that
        # should always be in address space such as Root or Objects
        # root = client.get_root_node()
        # print("Objects node is: ", root)

        # Node objects have methods to read and write
        # node attributes as well as browse or populate address space
        # print("Children of root are: ", root.get_children())

        # get a specific node knowing its node id
        # var = client.get_node(ua.NodeId(1002, 2))
        # var = client.get_node("ns=3;i=2002")
        # print(var)
        # var.get_data_value() # get value of node as a DataValue object
        # var.get_value() # get value of node as a python builtin
        # var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        # var.set_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        # myvar = root.get_child(["0:Objects", "1:MyObject", "1:MyVariable"])
        # obj = root.get_child(["0:Objects", "1:MyObject"])
        # print("myvar is: ", myvar)
        # print("myobj is: ", obj)

        # Stacked myvar access
        # print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())

    finally:
        pass

    app = QApplication(sys.argv)
    window = Window()

    handler = QtHandler(client.ui.logTextEdit)
    logging.getLogger().addHandler(handler)
    logging.getLogger("uaclient").setLevel(logging.NOTSET)

    window.show()
    client.disconnect()
    sys.exit(app.exec_())
