# =========================
# main.py
# =========================

# Import klasy do ustawień aplikacji
from PySide6.QtCore import QCoreApplication, QSettings

# Import podstawowych klas GUI
from PySide6.QtWidgets import QWidget, QApplication

# Import głównego okna programu
from mainwidget import MainWidget


def main():
    # Tworzy aplikację Qt
    app = QApplication()

    # Ustawia nazwę organizacji (potrzebne do QSettings)
    QCoreApplication.setOrganizationName("UMCS")

    # Ustawia nazwę aplikacji
    QCoreApplication.setApplicationName("Pogoda")

    # Tworzy główne okno programu
    widget = MainWidget()

    # Pokazuje okno
    widget.show()

    # Uruchamia pętlę programu
    return app.exec()


# Uruchamia program tylko jeśli plik został odpalony bezpośrednio
if __name__ == '__main__':
    main()