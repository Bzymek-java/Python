# =========================
# settingsdialog.py
# =========================

# Import klas Qt
from PySide6.QtWidgets import (
    QDialog, QCheckBox, QGridLayout, QDialogButtonBox
)


# Okno ustawień
class SettingsDialog(QDialog):

    def __init__(self, weatherVariables, parent):
        super().__init__(parent)

        # Tytuł okna
        self.setWindowTitle("Settings")

        # Checkboxy
        codeBox = QCheckBox("Weather code")
        temperatureBox = QCheckBox("Temperature box")
        pressureBox = QCheckBox("Pressure box")

        # Powiązanie checkboxów z nazwami API
        self.boxes = {
            "weather_code": codeBox,
            "temperature_2m": temperatureBox,
            "pressure_msl": pressureBox
        }

        # Przyciski OK / Cancel
        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        # Kliknięcie OK
        buttonBox.accepted.connect(self.accept)

        # Kliknięcie Cancel
        buttonBox.rejected.connect(self.reject)

        # Layout
        self.layout = QGridLayout(self)

        self.layout.addWidget(codeBox)
        self.layout.addWidget(temperatureBox)
        self.layout.addWidget(pressureBox)
        self.layout.addWidget(buttonBox)

        # Przywraca wcześniejsze zaznaczenia
        self.restoreVariables(weatherVariables)

    # Zwraca zaznaczone opcje
    def weatherVariables(self):

        weatherVariables = set()

        for key, checkbox in self.boxes.items():

            if checkbox.isChecked():
                weatherVariables.add(key)

        return weatherVariables

    # Zaznacza checkboxy wg ustawień
    def restoreVariables(self, variables):

        for key, checkbox in self.boxes.items():
            checkbox.setChecked(key in variables)