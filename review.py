from PyQt5.QtWidgets import QWidget, QSplitter, QTextEdit, QListWidget, QVBoxLayout
from PyQt5.QtCore import Qt


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

        if len(text.strip()) == 0:
            issues.append("内容为空")
        if "很" in text and text.count("很") > 3:
            issues.append("“很”字重复较多，可适当减少以增强表达力")
        if "的的" in text:
            issues.append("发现可能的错别字：重复的“的”")
        if text.endswith("了了"):
            issues.append("句尾出现重复词“了了”")

        lines = text.splitlines()
        for i, line in enumerate(lines):
            if len(line) > 120:
                issues.append(f"第 {i+1} 行过长（{len(line)} 字），建议换行")
            if line.strip().startswith("但是但是"):
                issues.append(f"第 {i+1} 行出现重复连接词“但是”")

        if not issues:
            issues.append("未发现明显问题，已通过初步审阅 ✅")

        self.issue_list.addItems(issues)
