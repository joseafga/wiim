import os
import sys
from PyQt5 import uic, QtGui, QtCore, QtSvg
from PyQt5.QtWidgets import *
import resources


class QCard(QWidget):
    """Cards Widget Class"""

    def __init__(self):
        super(QCard, self).__init__()
        uic.loadUi('gui/widget_card.ui', self)


class QCardsGallery(QWidget):
    def __init__(self, parent=None):
        super(QCardsGallery, self).__init__(parent)

        self.cards = []

        for title, desc in [
            # ('Moenda', 'Area de moenda bla bla bla'),
            # ('Caldeiraria', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin fermentum.'),
            # ('Destilaria', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque scelerisque.'),

            ('Condensadores', 'Lorem ipsum dolor sit posuere.'),
            ('Fornalhas', 'Lorem ipsum dolor sit amet, consectetur cras amet.')
        ]:
            self.cards.append(QCard())
            self.cards[-1].title.setText(title)
            self.cards[-1].description.setText(desc)
            self.cards[-1].picture.setPixmap(QtGui.QPixmap('images/test.jpg'))

        self.layout = QGridLayout()
        col = 0
        for i, card in enumerate(self.cards):
            self.layout.addWidget(card, i / 2, col, 1, 1)

            if col == 1:
                col = 0
            else:
                col += 1

        self.setLayout(self.layout)


class QListItem(QWidget):
    def __init__(self, parent=None):
        super(QListItem, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        font = QtGui.QFont('Roboto', 14)
        font.setBold(True)
        self.textUpQLabel.setFont(font)
        self.textDownQLabel = QLabel()
        self.textDownQLabel.setWordWrap(True)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.iconQLabel.setMargin(10)
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def setIcon(self, imagePath, size=None):
        svg = QtSvg.QSvgRenderer(imagePath)
        qim = QtGui.QImage(48, 48, QtGui.QImage.Format_ARGB32)
        qim.fill(0)
        painter = QtGui.QPainter()

        painter.begin(qim)
        svg.render(painter)
        painter.end()

        pixmap = QtGui.QPixmap(qim)
        self.iconQLabel.setPixmap(pixmap)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form_cards = QCardsGallery()
        self.setCentralWidget(self.form_cards)

        self.form_list = QListWidget(self)
        for index, name in [
            # ('Paraguacu Pta.', 'Unidade da empresa para produção de alguma coisa'),
            # ('Assis', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur purus nunc, vestibulum a odio non, finibus laoreet augue. Duis ultrices ligula ac ipsum suscipit, sit amet placerat neque tincidunt. Phasellus iaculis finibus arcu, sed vestibulum mauris vehicula ac. Integer sed elementum diam, eu volutpat velit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce non dignissim lectus, nec dictum lorem. Cras dignissim libero tortor, et eleifend ligula vehicula ac.'),
            # ('Candido Mota', 'Unidade da empresa para assuntos financeiros')

            ('Moenda', 'Area de moenda bla bla bla'),
            ('Caldeiraria', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin fermentum.'),
            ('Destilaria', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque scelerisque.'),
        ]:
            # Create QCustomQWidget
            self.myQCustomQWidget = QListItem()
            self.myQCustomQWidget.setTextUp(index)
            self.myQCustomQWidget.setTextDown(name)
            # self.myQCustomQWidget.setIcon(':/images/icons/factory_48.png')
            self.myQCustomQWidget.setIcon(':/images/icons/svg/mind_map.svg')
            # Create QListWidgetItem
            self.myQListWidgetItem = QListWidgetItem(self.form_list)
            # Set size hint
            self.myQListWidgetItem.setSizeHint(self.myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.form_list.addItem(self.myQListWidgetItem)
            self.form_list.setItemWidget(self.myQListWidgetItem, self.myQCustomQWidget)

        split = QWidget()
        self.box_layout = QHBoxLayout()
        self.box_layout.addWidget(self.form_list)
        self.box_layout.addWidget(self.form_cards)
        split.setLayout(self.box_layout)

        self.setCentralWidget(split)

        app_icon = QtGui.QIcon()
        app_icon.addFile(':/images/icons/icon_16.png', QtCore.QSize(16, 16))
        app_icon.addFile(':/images/icons/icon_32.png', QtCore.QSize(24, 24))
        app_icon.addFile(':/images/icons/icon_64.png', QtCore.QSize(32, 32))
        self.setWindowIcon(app_icon)

        self.init_ui()

    def init_ui(self):
        bar = self.menuBar()
        file = bar.addMenu('File')

        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')

        open_action = QAction('&Open', self)

        quit_action = QAction('&Quit', self)

        file.addAction(new_action)
        file.addAction(save_action)
        file.addAction(open_action)
        file.addAction(quit_action)

        quit_action.triggered.connect(self.quit_trigger)
        file.triggered.connect(self.respond)

        self.show()

    def quit_trigger(self):
        qApp.quit()

    def respond(self, q):
        signal = q.text()

        if signal == 'New':
            self.form_widget.clear_text()
        elif signal == '&Open':
            self.form_widget.open_text()
        elif signal == '&Save':
            self.form_widget.save_text()


app = QApplication(sys.argv)
main = Main()
sys.exit(app.exec_())
