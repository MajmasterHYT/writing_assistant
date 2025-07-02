import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QSplitter, QAction, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from editor import EditorTab
from filetree import FileTree
from search import SearchReplaceDialog
from theme import load_dark_theme
from review import ReviewTab

DEFAULT_FONT_SIZE = 20  # 默认字体大小

class VSEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VS Poem 编辑器")
        self.resize(1000, 600)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.tabs.addTab(EditorTab(), "欢迎页")

        self.tree = FileTree(self.open_file)

        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.tabs)
        splitter.setSizes([200, 800])
        self.setCentralWidget(splitter)

        self.font_size = DEFAULT_FONT_SIZE  # 默认字体大小

        # 定时器
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.auto_save_all)
        self.autosave_timer.start(60000)  # 每60秒自动保存

        self._create_menu()

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")
        search_menu = menubar.addMenu("编辑")

        edit_menu = search_menu.addMenu("编辑选项")

        font_menu = edit_menu.addMenu("字体大小")

        increase_action = QAction("放大 (+)", self)
        increase_action.triggered.connect(self.increase_font_size)
        font_menu.addAction(increase_action)

        decrease_action = QAction("缩小 (-)", self)
        decrease_action.triggered.connect(self.decrease_font_size)
        font_menu.addAction(decrease_action)

        reset_action = QAction("恢复默认", self)
        reset_action.triggered.connect(self.reset_font_size)
        font_menu.addAction(reset_action)

        new_action = QAction("新建", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        save_action = QAction("保存当前文件", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_current_file)
        file_menu.addAction(save_action)

        save_all_action = QAction("保存所有", self)
        save_all_action.setShortcut("Ctrl+Shift+S")
        save_all_action.triggered.connect(self.save_all_files)
        file_menu.addAction(save_all_action)


        search_action = QAction("查找 / 替换", self)
        search_action.triggered.connect(self.open_search_dialog)
        search_menu.addAction(search_action)

        review_action = QAction("检视当前文档", self)
        review_action.triggered.connect(self.review_current_document)
        search_menu.addAction(review_action)

        review_selected_action = QAction("检视选中内容", self)
        review_selected_action.triggered.connect(self.review_selected_text)
        search_menu.addAction(review_selected_action)

        file_menu.addAction("退出", self.close)

    def open_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                editor_tab = EditorTab()
                editor_tab.editor.setPlainText(content)
                self.tabs.addTab(editor_tab, path.split("/")[-1])
        except Exception as e:
            print("打开失败:", e)

    def open_search_dialog(self):
        current = self.tabs.currentWidget()
        if current:
            dlg = SearchReplaceDialog(current.editor)
            dlg.exec_()

    def review_current_document(self):
        current = self.tabs.currentWidget()
        if current:
            text = current.editor.toPlainText()
            review_tab = ReviewTab(text)
            self.tabs.addTab(review_tab, "🧐 检视结果")
            self.tabs.setCurrentWidget(review_tab)

    def review_selected_text(self):
        current = self.tabs.currentWidget()
        if current:
            selected_text = current.editor.textCursor().selectedText()
            if selected_text.strip():
                review_tab = ReviewTab(selected_text)
                self.tabs.addTab(review_tab, "🔍 检视选中内容")
                self.tabs.setCurrentWidget(review_tab)
            else:
                print("未选中文本，跳过")

    def new_file(self):
        new_tab = EditorTab()
        self.tabs.addTab(new_tab, "未命名")
        self.tabs.setCurrentWidget(new_tab)

    def save_current_file(self):
        current = self.tabs.currentWidget()
        if not current:
            return

        # 如果是未命名文件，弹出保存对话框
        if not getattr(current, 'file_path', None):
            path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt);;所有文件 (*)")
            if path:
                success = current.save(path)
                if success:
                    self.tabs.setTabText(self.tabs.currentIndex(), path.split("/")[-1])
                    QMessageBox.information(self, "保存成功", f"文件已保存到：\n{path}")
        else:
            if current.save():
                QMessageBox.information(self, "保存成功", f"已覆盖保存：\n{current.file_path}")

    def save_all_files(self):
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if hasattr(tab, "save"):
                if not getattr(tab, 'file_path', None):
                    path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt);;所有文件 (*)")
                    if path:
                        tab.save(path)
                        self.tabs.setTabText(i, path.split("/")[-1])
                else:
                    tab.save()

    def auto_save_all(self):
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if hasattr(tab, "save") and getattr(tab, 'file_path', None):
                tab.save()

    def get_current_editor(self):
        tab = self.tabs.currentWidget()
        return tab if hasattr(tab, "set_font_size") else None

    def increase_font_size(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.editor.font()
            self.font_size = font.pointSize() + 1
            editor.set_font_size(self.font_size)

    def decrease_font_size(self):
        editor = self.get_current_editor()
        if editor:
            font = editor.editor.font()
            self.font_size = max(font.pointSize() - 1, 6)  # 不小于6
            editor.set_font_size(self.font_size)

    def reset_font_size(self):
        editor = self.get_current_editor()
        if editor:
            self.font_size = DEFAULT_FONT_SIZE
            editor.set_font_size(DEFAULT_FONT_SIZE)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_dark_theme(app)
    win = VSEditor()
    win.show()
    sys.exit(app.exec_())
