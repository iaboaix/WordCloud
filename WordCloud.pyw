import os
import re
import sys
import time
import jieba
import requests
from random import randint
from MainWindow import Ui_MainWindow
from ConfigWidget import Ui_Config
from wordcloud import WordCloud
from collections import Counter
from PIL import Image
import numpy as np
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QTableWidgetItem, \
                            QHBoxLayout, QGraphicsProxyWidget, QVBoxLayout, QLabel, QGraphicsLineItem
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QFile, QTextCodec, QTextStream, QIODevice, \
                         QFile, pyqtSignal, QPointF, QPoint, QRectF
from PyQt5.QtGui import QIcon, QMovie, QPixmap, QPainter, QPen
from PyQt5.QtChart import QChartView, QChart, QBarSeries, QBarSet, QBarCategoryAxis
import source_rc
class MainWindow(QWidget, Ui_MainWindow):

    margin = 5
    width = 4000
    height = 3000        
    random_state = 60
    draw_chart = pyqtSignal(list)
    set_item = pyqtSignal(int, tuple)

    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.resize(1800, 1300)
        self.setAcceptDrops(True)
        self.setWindowIcon(QIcon(':/source/wordcloud.ico'))
        self.pic_show.setStyleSheet("border-image: url(:/source/cloud.png)")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.chart_view = ChartView()
        layout.addWidget(self.chart_view)
        self.chart_widget.setLayout(layout)
        self.config_widget = ConfigWidget()

        self.load_text.clicked.connect(self.load_file)
        self.make_cloud.clicked.connect(self.create_pic)
        self.make_cloud.clicked.connect(self.analyse_thread)
        self.save_pic.clicked.connect(self.save_picture)
        self.change_setting.clicked.connect(self.config_widget.show)
        self.draw_chart.connect(self.chart_view.initChart)
        self.set_item.connect(self.set_table_item)

        if os.path.exists('./wordcloud'):
            pass
        else:
            os.mkdir('./wordcloud')
        if os.path.exists('./source'):
            pass
        else:
            os.mkdir('./source')


    def analyse_thread(self):
        self.text_thread = Thread(target=self.analyse_text)
        self.text_thread.start()

    def analyse_text(self):
        result = []
        remove_words = [u'的', u'，',u'和', u'是', u'随着', u'对于',u'对',u'等',u'能',u'都',u'。',
        u' ',u'、',u'中',u'在',u'了',u'通常',u'如果',u'我们',u'需要', u'\n', u'我', u'你', u'她', 
        u'他', u'也', u'？', u'又', u'人', u'\u3000', u'“', u'”', u'去', u'与', u'不', u'：', 
        u'将', u'！', u'还', u'说', u'着', u'有', u'再', u'来', u'想', u'就', u'上', u'得', u'走',
        u'并', u'要', u'会', u'什么', u'知道', u'为', u'自己', u'到', u'给', u'做', u'这', 
        u'让', u'那']
        with open(self.path, 'r') as file:
            pattern = re.compile('[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~+:…]')
            text = re.sub(pattern, '', file.read())
            words = jieba.cut(text)
            for word in words:
                if word not in remove_words:
                    result.append(word)

        common = Counter(result).most_common(20)
        for i in range(20):
            self.set_item.emit(i, common[i])
        self.tableWidget.update()
        self.draw_chart.emit(common)

    def set_table_item(self, index, item):
        self.tableWidget.setItem(index, 0, QTableWidgetItem(item[0]))
        self.tableWidget.setItem(index, 1, QTableWidgetItem(str(item[1])))

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

        self.pic_thread = CreateThread(self.path, font_path, self.margin, self.width, self.height, 
                                   max_words, background_color, self.mask, color_random, 
                                   min_font_size, max_font_size)
        self.pic_thread.finish_signal.connect(self.set_pixmap)
        self.pic_thread.start()

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


class ToolTipItem(QWidget):

    def __init__(self, color, text, parent=None):
        super(ToolTipItem, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        clabel = QLabel(self)
        clabel.setMinimumSize(12, 12)
        clabel.setMaximumSize(12, 12)
        clabel.setStyleSheet("border-radius:6px;background: rgba(%s,%s,%s,%s);" % (
            color.red(), color.green(), color.blue(), color.alpha()))
        layout.addWidget(clabel)
        self.textLabel = QLabel(text, self, styleSheet="color:white;")
        layout.addWidget(self.textLabel)

    def setText(self, text):
        self.textLabel.setText(text)


class ToolTipWidget(QWidget):

    Cache = {}

    def __init__(self, *args, **kwargs):
        super(ToolTipWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ToolTipWidget{background: rgba(50, 50, 50, 100);}")
        layout = QVBoxLayout(self)
        self.titleLabel = QLabel(self, styleSheet="color:white;")
        layout.addWidget(self.titleLabel)

    def updateUi(self, title, bars):
        self.titleLabel.setText(title)
        for bar, value in bars:
            if bar not in self.Cache:
                item = ToolTipItem(
                    bar.color(),
                    (bar.label() or "-") + ":" + str(value), self)
                self.layout().addWidget(item)
                self.Cache[bar] = item
            else:
                self.Cache[bar].setText(
                    (bar.label() or "-") + ":" + str(value))
            brush = bar.brush()
            color = brush.color()
            self.Cache[bar].setVisible(color.alphaF() == 1.0)  # 隐藏那些不可用的项
        self.adjustSize()  # 调整大小


class GraphicsProxyWidget(QGraphicsProxyWidget):

    def __init__(self, *args, **kwargs):
        super(GraphicsProxyWidget, self).__init__(*args, **kwargs)
        self.setZValue(999)
        self.tipWidget = ToolTipWidget()
        self.setWidget(self.tipWidget)
        self.hide()

    def width(self):
        return self.size().width()

    def height(self):
        return self.size().height()

    def show(self, title, bars, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, bars)
        super(GraphicsProxyWidget, self).show()


class ChartView(QChartView):

    def __init__(self, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self._chart = QChart(title="词频图")
        # 提示widget
        self.toolTipWidget = GraphicsProxyWidget(self._chart)
        # line 宽度需要调整
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

        self._chart.setAcceptHoverEvents(True)
        # Series动画
        self._chart.setAnimationOptions(QChart.SeriesAnimations)

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        pos = event.pos()
        # 把鼠标位置所在点转换为对应的xy值
        x = self._chart.mapToValue(pos).x()
        y = self._chart.mapToValue(pos).y()
        index = round(x)
        # 得到在坐标系中的所有bar的类型和点
        try:
            serie = self._chart.series()[0]
        except:
            return
        bars = [(bar, bar.at(index))
                for bar in serie.barSets() if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y]
        if bars:
            right_top = self._chart.mapToPosition(
                QPointF(self.max_x, self.max_y))
            # 等分距离比例
            step_x = round(
                (right_top.x() - self.point_top.x()) / self.category_len)
            posx = self._chart.mapToPosition(QPointF(x, self.min_y))
            self.lineItem.setLine(posx.x(), self.point_top.y(),
                                  posx.x(), posx.y())
            self.lineItem.show()
            try:
                title = self.categories[index]
            except:
                title = ""
            t_width = self.toolTipWidget.width()
            t_height = self.toolTipWidget.height()
            # 如果鼠标位置离右侧的距离小于tip宽度
            x = pos.x() - t_width if self.width() - \
                pos.x() - 20 < t_width else pos.x()
            # 如果鼠标位置离底部的高度小于tip高度
            y = pos.y() - t_height if self.height() - \
                pos.y() - 20 < t_height else pos.y()
            self.toolTipWidget.show(
                title, bars, QPoint(x, y))
        else:
            self.toolTipWidget.hide()
            self.lineItem.hide()

    def handleMarkerClicked(self):
        marker = self.sender()  # 信号发送者
        if not marker:
            return
        bar = marker.barset()
        if not bar:
            return
        # bar透明度
        brush = bar.brush()
        color = brush.color()
        alpha = 0.0 if color.alphaF() == 1.0 else 1.0
        color.setAlphaF(alpha)
        brush.setColor(color)
        bar.setBrush(brush)
        # marker
        brush = marker.labelBrush()
        color = brush.color()
        alpha = 0.4 if color.alphaF() == 1.0 else 1.0
        # 设置label的透明度
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setLabelBrush(brush)
        # 设置marker的透明度
        brush = marker.brush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)

    def handleMarkerHovered(self, status):
        # 设置bar的画笔宽度
        marker = self.sender()  # 信号发送者
        if not marker:
            return
        bar = marker.barset()
        if not bar:
            return
        pen = bar.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        bar.setPen(pen)

    def handleBarHoverd(self, status, index):
        # 设置bar的画笔宽度
        bar = self.sender()  # 信号发送者
        pen = bar.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        bar.setPen(pen)

    def initChart(self, common):
        self.categories = [item[0] for item in common]
        series = QBarSeries(self._chart)
        bar = QBarSet("")
        # 随机数据
        for item in common:
            bar.append(item[1])
        series.append(bar)
        bar.hovered.connect(self.handleBarHoverd)  # 鼠标悬停
        self._chart.addSeries(series)
        self._chart.createDefaultAxes()  # 创建默认的轴
        # x轴
        axis_x = QBarCategoryAxis(self._chart)
        axis_x.append(self.categories)
        self._chart.setAxisX(axis_x, series)
        # chart的图例
        legend = self._chart.legend()
        legend.setVisible(True)
        # 遍历图例上的标记并绑定信号
        for marker in legend.markers():
            # 点击事件
            marker.clicked.connect(self.handleMarkerClicked)
            # 鼠标悬停事件
            marker.hovered.connect(self.handleMarkerHovered)
        # 一些固定计算，减少mouseMoveEvent中的计算量
        # 获取x和y轴的最小最大值
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        self.category_len = len(axisX.categories())
        self.min_x, self.max_x = -0.5, self.category_len - 0.5
        self.min_y, self.max_y = axisY.min(), axisY.max()
        # 坐标系中左上角顶点
        self.point_top = self._chart.mapToPosition(
            QPointF(self.min_x, self.max_y))
        self.setChart(self._chart)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    # import qdarkstyle
    # win.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win.show()
    sys.exit(app.exec_())
