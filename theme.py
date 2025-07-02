import qdarkstyle

def load_dark_theme(app):
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
