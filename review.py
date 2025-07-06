from PyQt5.QtWidgets import QWidget, QSplitter, QTextEdit, QListWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from model import suggestions

class ReviewTab(QWidget):
    def __init__(self, text_to_review):
        super().__init__()
        layout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        # 左侧：只读文本显示
        self.text_view = QTextEdit()
        self.text_view.setPlainText(text_to_review)
        self.text_view.setReadOnly(True)

        # 右侧：问题列表
        self.issue_list = QListWidget()
        self.run_review(text_to_review)

        splitter.addWidget(self.text_view)
        splitter.addWidget(self.issue_list)
        splitter.setSizes([600, 400])

        layout.addWidget(splitter)
        self.setLayout(layout)

    def run_review(self, text):
        issues = []
        json_data = suggestions(text)
        for entry in json_data:
            original_text = entry["原文"]
            modified_text = entry["修改后"]
            issues.append(f"原文: {original_text}\n修改后: {modified_text}\n\n")

        if not issues:
            issues.append("未发现明显问题，已通过初步审阅 ✅")
        # print("审阅结果:", issues)  # 调试输出审阅结果
        self.issue_list.addItems(issues)
