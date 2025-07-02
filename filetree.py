from PyQt5.QtWidgets import QFileSystemModel, QTreeView
from PyQt5.QtCore import QDir


class FileTree(QTreeView):
    def __init__(self, file_open_callback):
        super().__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.setModel(self.model)
        self.setRootIndex(self.model.index(QDir.currentPath()))
        self.setHeaderHidden(True)
        self.clicked.connect(lambda idx: file_open_callback(self.model.filePath(idx)))
