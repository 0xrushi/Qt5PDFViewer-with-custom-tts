#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMenu
from time import sleep
import requests

root = os.path.dirname(sys.argv[0])
PDFJS = f"file://{os.path.abspath('./web/viewer.html')}"
print(PDFJS)
PDF = f'file://{"%20".join(sys.argv[1:])}'
print("loading PDF:", PDF)

class Window(QWebEngineView):
    def __init__(self):
        super(Window, self).__init__()
        if len(sys.argv) > 1:
            self.load(QUrl.fromUserInput(f'{PDFJS}?file={PDF}'))
            self.selectionChanged.connect(self.selection_changed)
        else:
            self.load(QUrl.fromUserInput(f"{PDFJS}?file=file://{root}/test.pdf"))
    def selection_changed(self):
        # print("Selection changed:", self.selectedText())
        pass

    # https://forum.qt.io/topic/128824/custom-context-menu-in-qtwebengineview-in-python
    def contextMenuEvent(self, event):
        self.menus = QMenu()
        
        speak_action = self.menus.addAction('Speak')
        speak_action.triggered.connect(self.inference)
        
        self.menus.popup(event.globalPos())

    def inference(self):
        text = self.self.selectedText()
        r = requests.post('http://127.0.0.1:5000', data={'text': text})
        print(r.json())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())
    
