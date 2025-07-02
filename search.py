from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton


class SearchReplaceDialog(QDialog):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setWindowTitle("查找 / 替换")
        layout = QVBoxLayout()

        self.search_box = QLineEdit()
        self.replace_box = QLineEdit()

        search_btn = QPushButton("查找")
        replace_btn = QPushButton("替换")
        replace_all_btn = QPushButton("全部替换")

        search_btn.clicked.connect(self.find_next)
        replace_btn.clicked.connect(self.replace_one)
        replace_all_btn.clicked.connect(self.replace_all)

        layout.addWidget(self.search_box)
        layout.addWidget(self.replace_box)

        btns = QHBoxLayout()
        btns.addWidget(search_btn)
        btns.addWidget(replace_btn)
        btns.addWidget(replace_all_btn)

        layout.addLayout(btns)
        self.setLayout(layout)

    def find_next(self):
        text = self.search_box.text()
        if text:
            cursor = self.editor.textCursor()
            if not self.editor.find(text):
                cursor.movePosition(cursor.Start)
                self.editor.setTextCursor(cursor)
                self.editor.find(text)

    def replace_one(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_box.text())
        self.find_next()

    def replace_all(self):
        self.editor.moveCursor(0)
        while self.editor.find(self.search_box.text()):
            cursor = self.editor.textCursor()
            cursor.insertText(self.replace_box.text())
