import os
import re
import sys
import time
import requests
from MainWindow import Ui_MainWindow
from ConfigWidget import Ui_Config
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QFile, QTextCodec, QTextStream, QIODevice, QFile, pyqtSignal
from PyQt5.QtGui import QIcon, QMovie, QPixmap, QPainter
import source_rc
class MainWindow(QWidget, Ui_MainWindow):

    margin = 5
    width = 4000
    height = 3000        
    random_state = 60

    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.setWindowIcon(QIcon(':/source/wordcloud.ico'))
        self.pic_show.setStyleSheet("border-image: url(:/source/cloud.png)")

        self.config_widget = ConfigWidget()

        self.load_text.clicked.connect(self.load_file)
        self.make_cloud.clicked.connect(self.create_pic)
        self.save_pic.clicked.connect(self.save_picture)
        self.change_setting.clicked.connect(self.config_widget.show)

        if os.path.exists('./wordcloud'):
            pass
        else:
            os.mkdir('./wordcloud')
        if os.path.exists('./source'):
            pass
        else:
            os.mkdir('./source')

    def save_picture(self):
        self.is_save = True
        QMessageBox.information(self, '提示', '词云保存成功！')

    def load_file(self):
        self.path, ok = QFileDialog.getOpenFileName(self, 'Load file', ':/source/', 'Text Files (*.txt)')
        if ok:
            self.text_path.setText(str(self.path))

    def create_pic(self):
        if not os.path.exists(self.path):
            QMessageBox.warning(self, '警告', '请先载入数据！')
            return
        if os.path.exists(self.config_widget.mask_path_line.text()):
            image = Image.open(self.config_widget.mask_path_line.text())
            self.mask = np.array(image)

        self.pic_show.clear()
        movie = QMovie(':/source/loading.gif')
        movie.setScaledSize(self.pic_show.size())
        self.pic_show.setMovie(movie)
        movie.start()

        font_path = self.config_widget.font_path_line.text()
        max_words = self.config_widget.max_word.value()
        background_color = self.config_widget.background_color
        color_random = self.config_widget.color_random.value()
        min_font_size = int(self.config_widget.min_size.text())
        max_font_size = int(self.config_widget.max_size.text())

        self.thread = CreateThread(self.path, font_path, self.margin, self.width, self.height, 
                                   max_words, background_color, self.mask, color_random, 
                                   min_font_size, max_font_size)
        self.thread.finish_signal.connect(self.set_pixmap)
        self.thread.start()

        self.make_cloud.setEnabled(False)
        self.make_cloud.setText('正在生成')
        self.load_text.setEnabled(False)

    def set_pixmap(self, pic_name):
        self.load_text.setEnabled(True)
        self.make_cloud.setEnabled(True)
        self.make_cloud.setText('开始生成')
        self.pic_show.clear()
        print('设置图片')
        self.pic_show.setStyleSheet("border-image:url({0})".format(pic_name))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.TargetMoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            path = str(event.mimeData().urls()[0].toLocalFile())
            if path[-3:] == 'txt':
                self.text_path.setText(path)
                self.path = path
            else:
                QMessageBox.warning(self, "警告!", '你拖的不是txt格式的文本文件吧？', QMessageBox.Yes)
        else:
            event.ignore()

    def closeEvent(self, event):
        print('删除缓存')
        try:
            os.remove(self.text_path.text())
        except:
            print('not found!')

class ConfigWidget(QWidget, Ui_Config):

    background_color = 'white'
    i = 0

    def __init__(self, parent = None):
        super(ConfigWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/source/wordcloud.ico'))

        self.set_btn.clicked.connect(self.change_config)
        self.mask_btn.clicked.connect(self.set_mask_path)
        self.font_btn.clicked.connect(self.set_font_path)
        self.color_btn.clicked.connect(self.set_color)

    def set_color(self):
        self.i += 1
        if self.i == 0:
            self.color_btn.setStyleSheet("background-color: white")
            self.background_color = 'white'
        elif self.i == 1:
            self.color_btn.setStyleSheet("background-color: black")
            self.background_color = 'black'
        elif self.i == 2:
            self.color_btn.setStyleSheet("background-color: red")
            self.background_color = 'red'
        elif self.i == 3:
            self.color_btn.setStyleSheet("background-color: pink")
            self.background_color = 'pink'
        elif self.i == 4:
            self.color_btn.setStyleSheet("background-color: green")
            self.background_color = 'green'
        elif self.i == 5:
            self.color_btn.setStyleSheet("background-color: magenta")
            self.background_color = 'magenta'
        elif self.i == 6:
            self.color_btn.setStyleSheet("background-color: gray")
            self.background_color = 'gray'
            self.i = -1

    def set_font_path(self):
        path, ok = QFileDialog.getOpenFileName(self, '选择Font', './source', 'Files (*.ttf *.TTF *.ttc)')
        if ok:
            self.font_path_line.setText(str(path))

    def set_mask_path(self):
        path, ok = QFileDialog.getOpenFileName(self, '选择Mask', './source', 'Files (*.jpg *.png)')
        if ok:
            self.mask_path_line.setText(str(path))

    def change_config(self):
        QMessageBox.information(self, 'Success!', '更新配置成功。')
        self.hide()


class CreateThread(QThread):

    finish_signal = pyqtSignal(str)

    def __init__(self, path, font_path, margin, width, height, \
                 max_words, background_color, mask, random_state,\
                 min_font_size, max_font_size):
        super(CreateThread, self).__init__()
        self.path = path
        self.wordcloud = WordCloud(font_path=font_path,
                                   margin=margin, 
                                   width=width,
                                   height=height,
                                   max_words=max_words,
                                   background_color=background_color,
                                   mask=mask, 
                                   random_state=random_state, 
                                   min_font_size=min_font_size,
                                   max_font_size=max_font_size)

    def run(self):
        print('正在生成词云...')
        with open(self.path, 'rb') as file:
            data = file.read().decode('gbk', 'ignore')
            self.wordcloud.generate(data)
        pic_name = './wordcloud/' + str(time.time()) + '.png'
        self.wordcloud.to_file(pic_name)
        print('词云生成完毕...')
        self.finish_signal.emit(pic_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    # import qdarkstyle
    # win.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win.show()
    sys.exit(app.exec_())
