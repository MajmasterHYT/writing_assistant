from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QMenu, QListWidget, QCheckBox
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt, QRegExp, QTimer


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Bold)

        keywords = ["def", "class", "if", "else", "try", "except", "return", "import"]
        for word in keywords:
            pattern = QRegExp(f"\\b{word}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.highlighting_rules.append((QRegExp("#[^\n]*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)


class EditorTab(QWidget):
    def __init__(self, file_path=None):
        super().__init__()
        self.file_path = file_path
        self.modified_lines = set()
        self.analyze_all = False

        layout = QVBoxLayout()
        self.editor = QTextEdit()
        self.editor.setAcceptRichText(False)
        self.editor.setLineWrapMode(QTextEdit.WidgetWidth)
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.context_menu)

        self.default_font_size = 20
        self.set_font_size(self.default_font_size)

        PythonHighlighter(self.editor.document())

        self.review_timer = QTimer()
        self.review_timer.setSingleShot(True)
        self.review_timer.timeout.connect(self.review_text)
        self.editor.textChanged.connect(self.on_text_change)

        self.mode_toggle = QCheckBox("启用全文分析")
        self.mode_toggle.stateChanged.connect(self.toggle_analysis_mode)

        self.issue_list = QListWidget()
        self.issue_list.setMaximumHeight(120)
        self.issue_list.itemClicked.connect(self.goto_issue)

        layout.addWidget(self.editor)
        layout.addWidget(self.mode_toggle)
        layout.addWidget(self.issue_list)
        self.setLayout(layout)

    def context_menu(self, pos):
        menu = QMenu()
        menu.addAction("复制", self.editor.copy)
        menu.addAction("剪切", self.editor.cut)
        menu.addAction("粘贴", self.editor.paste)
        menu.exec_(self.editor.mapToGlobal(pos))

    def get_text(self):
        return self.editor.toPlainText()

    def set_text(self, content):
        self.editor.setPlainText(content)

    def save(self, path=None):
        path = path or self.file_path
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.get_text())
            self.file_path = path
            return True
        return False

    def on_text_change(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        self.modified_lines.add(line)
        self.review_timer.start(10000)

    def toggle_analysis_mode(self, state):
        self.analyze_all = state == Qt.Checked

    def review_text(self):
        self.issue_list.clear()
        text = self.get_text()
        lines = text.splitlines()
        target_lines = range(1, len(lines) + 1) if self.analyze_all else self.modified_lines

        for line_num in sorted(target_lines):
            if 1 <= line_num <= len(lines):
                line = lines[line_num - 1]
                if True:
                    self.issue_list.addItem(f"第 {line_num} 行：写得太烂")
                if len(line) > 100:
                    self.issue_list.addItem(f"第 {line_num} 行过长，建议换行")
                if "。。" in line:
                    self.issue_list.addItem(f"第 {line_num} 行标点异常：出现“。。”")

        self.modified_lines.clear()

    def goto_issue(self, item):
        msg = item.text()
        if "第 " in msg:
            try:
                line = int(msg.split("第 ")[1].split(" 行")[0])
                cursor = self.editor.textCursor()
                cursor.movePosition(cursor.Start)
                for _ in range(line - 1):
                    cursor.movePosition(cursor.Down)
                self.editor.setTextCursor(cursor)
            except:
                pass

    def set_font_size(self, size):
        font = self.editor.font()
        font.setPointSize(size)
        self.editor.setFont(font)
        # self.issue_list.setFont(font)