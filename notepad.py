# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, 
                             QMessageBox, QStatusBar, QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QFileInfo
import subprocess

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.initUI()

    def initUI(self):
        # --- 위젯 생성 ---
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_status_bar) # Tab change updates status bar
        self.setCentralWidget(self.tab_widget)
        
        # --- 상태 표시줄 ---
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # --- 액션 생성 ---
        # 파일 메뉴
        self.new_tab_action = QAction('새 탭', self)
        self.new_tab_action.setShortcut('Ctrl+T')
        self.new_tab_action.triggered.connect(self.new_tab)

        self.new_window_action = QAction('새 창', self)
        self.new_window_action.setShortcut('Ctrl+N')
        self.new_window_action.triggered.connect(self.new_window)

        self.open_action = QAction('열기...', self)
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction('저장', self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction('다른 이름으로 저장...', self)
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self.save_as_file)
        
        self.exit_action = QAction('끝내기', self)
        self.exit_action.setShortcut(QKeySequence.Quit)
        self.exit_action.triggered.connect(self.close)

        # 편집 메뉴
        self.undo_action = QAction('실행 취소', self)
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.undo_action.triggered.connect(self.undo)

        # 보기 메뉴
        self.zoom_in_action = QAction('확대', self)
        self.zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        self.zoom_in_action.triggered.connect(self.zoom_in)

        self.zoom_out_action = QAction('축소', self)
        self.zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        self.zoom_out_action.triggered.connect(self.zoom_out)

        self.default_zoom_action = QAction('기본값으로', self)
        self.default_zoom_action.setShortcut('Ctrl+0')
        self.default_zoom_action.triggered.connect(self.default_zoom)


        # --- 메뉴바 생성 ---
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('파일(&F)')
        file_menu.addAction(self.new_tab_action)
        file_menu.addAction(self.new_window_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = menu_bar.addMenu('편집(&E)')
        edit_menu.addAction(self.undo_action)
        
        view_menu = menu_bar.addMenu('보기(&V)')
        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.default_zoom_action)

        # --- 초기 창 설정 ---
        self.new_tab() # Start with a new tab
        self.setGeometry(300, 300, 800, 600)
        
    def get_current_editor(self):
        return self.tab_widget.currentWidget()

    def update_title(self):
        editor = self.get_current_editor()
        if editor:
            title = QFileInfo(editor.property("file_path")).fileName() if editor.property("file_path") else "제목 없음"
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), title)
            self.setWindowTitle(f'{title}[*] - 메모장')

    def new_tab(self):
        editor = QTextEdit()
        editor.setProperty("file_path", None)
        self.tab_widget.addTab(editor, "제목 없음")
        self.tab_widget.setCurrentWidget(editor)
        editor.document().modificationChanged.connect(self.update_tab_title)
        editor.textChanged.connect(self.update_status_bar)
        editor.cursorPositionChanged.connect(self.update_status_bar)
        self.update_status_bar() # Initial update

    def new_window(self):
        subprocess.Popen([sys.executable, __file__])

    def open_file(self):
        editor = self.get_current_editor()
        if not self.maybe_save(editor):
            return
        file_name, _ = QFileDialog.getOpenFileName(self, '파일 열기', '', '텍스트 파일 (*.txt);;모든 파일 (*.*)')
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    editor.setText(f.read())
                editor.setProperty("file_path", file_name)
                self.update_title()
                editor.document().setModified(False)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 여는 중 오류가 발생했습니다: {e}")

    def save_file(self):
        editor = self.get_current_editor()
        if editor.property("file_path") is None:
            return self.save_as_file()
        
        try:
            with open(editor.property("file_path"), 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            editor.document().setModified(False)
            self.update_title()
            return True
        except Exception as e:
            QMessageBox.critical(self, "오류", f"파일을 저장하는 중 오류가 발생했습니다: {e}")
            return False

    def save_as_file(self):
        editor = self.get_current_editor()
        file_name, _ = QFileDialog.getSaveFileName(self, '다른 이름으로 저장', '', '텍스트 파일 (*.txt);;모든 파일 (*.*)')
        if file_name:
            editor.setProperty("file_path", file_name)
            return self.save_file()
        return False

    def undo(self):
        editor = self.get_current_editor()
        if editor:
            editor.undo()

    def zoom_in(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(font.pointSize() + 1)
            editor.setFont(font)

    def zoom_out(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(max(1, font.pointSize() - 1))
            editor.setFont(font)

    def default_zoom(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(10) # Or your preferred default size
            editor.setFont(font)

    def maybe_save(self, editor):
        if not editor.document().isModified():
            return True

        file_name = QFileInfo(editor.property("file_path")).fileName() if editor.property("file_path") else '제목 없음'
        message = f"'{file_name}'의 내용이 변경되었습니다.\n\n변경된 내용을 저장하시겠습니까?"

        ret = QMessageBox.warning(self, "메모장",
                                  message,
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.save_file()
        elif ret == QMessageBox.Cancel:
            return False
        return True

    def close_tab(self, index):
        editor = self.tab_widget.widget(index)
        if self.maybe_save(editor):
            self.tab_widget.removeTab(index)

    def update_tab_title(self, modified):
        editor = self.get_current_editor()
        if editor:
            index = self.tab_widget.indexOf(editor)
            if index != -1:
                title = QFileInfo(editor.property("file_path")).fileName() if editor.property("file_path") else "제목 없음"
                self.tab_widget.setTabText(index, f"{title}{'*' if modified else ''}")


    def update_status_bar(self):
        editor = self.get_current_editor()
        if editor:
            text_length = len(editor.toPlainText())
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.statusBar.showMessage(f"글자 수: {text_length} | 줄: {line}, 열: {col}")
        else:
            self.statusBar.showMessage("글자 수: 0 | 줄: 1, 열: 1")

    def closeEvent(self, event):
        for i in range(self.tab_widget.count()):
            if not self.maybe_save(self.tab_widget.widget(i)):
                event.ignore()
                return
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec_())