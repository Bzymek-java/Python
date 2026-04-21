# =========================
# mainwidget.py
# =========================

# Import klas Qt
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QPushButton, QLabel,
    QGridLayout, QMessageBox, QListWidget, QListWidgetItem
)

# Biblioteka do pobierania danych z internetu
import requests

# Import okna ustawień
from settingsdialog import SettingsDialog


# Główne okno programu
class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Odczyt zapisanych ustawień
        self.weatherVariables = self.restoreWeatherVariables()

        # Tytuł okna
        self.setWindowTitle("Pogoda")

        # Pole tekstowe do wpisania miasta
        self.edit = QLineEdit("Lublin")

        # Funkcja uruchamiająca wyszukiwanie
        searchWithParameter = lambda: self.search(self.edit.text())

        # Enter w polu tekstowym uruchamia wyszukiwanie
        self.edit.returnPressed.connect(searchWithParameter)

        # Przycisk wyszukiwania
        self.button = QPushButton("Okay")
        self.button.clicked.connect(searchWithParameter)

        # Lista znalezionych miast
        self.citylist = QListWidget()

        # Etykieta do wyświetlania pogody
        self.weatherLabel = QLabel()

        # Przycisk ustawień
        self.settingsButon = QPushButton("Settings")
        self.settingsButon.clicked.connect(self.execSettings)

        # Layout siatkowy
        self.layout = QGridLayout(self)

        # Dodawanie widgetów do layoutu
        self.layout.addWidget(QLabel("Miasto"), 0, 0)
        self.layout.addWidget(self.edit, 0, 1)
        self.layout.addWidget(self.button, 1, 0, 1, 2)
        self.layout.addWidget(self.citylist, 2, 0, 1, 2)
        self.layout.addWidget(self.weatherLabel, 3, 0, 1, 2)
        self.layout.addWidget(self.settingsButon, 4, 0, 1, 2)

        # Kliknięcie miasta pokazuje pogodę
        self.citylist.itemPressed.connect(self.showWeather)

    # Wyszukiwanie miasta
    def search(self, city):

        # Pobiera dane geograficzne miasta z API
        request = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        )

        # Zamiana odpowiedzi na JSON
        data = request.json()

        print(data)
        print(request.status_code)

        try:
            # Jeśli błąd strony
            if request.status_code != 200:
                raise Exception("błąd ładowania strony")

            # Jeśli brak wyników
            if "results" not in data:
                raise Exception("nie znaleziono miasta")

            # Pobranie listy wyników
            data = data["results"]

        except Exception as error:
            # Okno błędu
            QMessageBox.critical(self, "BŁĄD", str(error))

        # Lista miast: nazwa + współrzędne
        citiesData = [
            (result["name"], result["latitude"], result["longitude"])
            for result in data
        ]

        # Wyświetlenie listy
        self.pullList(citiesData)

    # Uzupełnia listę miast
    def pullList(self, citiesData):

        # Czyści listę
        self.citylist.clear()

        for name, latitude, longitude in citiesData:

            # Tworzy element listy
            item = QListWidgetItem(name)

            # Zapisuje ukryte dane (lat, lon)
            item.setData(Qt.UserRole, (latitude, longitude))

            # Dodaje do listy
            self.citylist.addItem(item)

    # Pokazuje pogodę po kliknięciu miasta
    def showWeather(self, item):

        # Pobiera współrzędne z elementu listy
        data = item.data(Qt.UserRole)

        latitude, longitude = data

        # Łączy wybrane parametry pogody
        variables = ",".join(self.weatherVariables)

        # Pobiera pogodę z API
        request = requests.get(
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&current={variables}"
        )

        # JSON
        data = request.json()

        print(data)

        # Buduje tekst wynikowy
        temp = "\n".join(
            [f"{key} = {data['current'][key]}" for key in self.weatherVariables]
        )

        # Wyświetla pogodę
        self.weatherLabel.setText(temp)

    # Otwiera okno ustawień
    def execSettings(self):

        settingsDialog = SettingsDialog(self.weatherVariables, self)

        # Pokazuje okno modalne
        settingsDialog.exec()

        # Jeśli kliknięto OK
        if settingsDialog.result() == True:

            # Pobiera nowe ustawienia
            self.weatherVariables = settingsDialog.weatherVariables()

            # Zapisuje ustawienia
            self.saveWeatherVariables()

        print(self.weatherVariables)

    # Zapis ustawień
    def saveWeatherVariables(self):

        settings = QSettings()

        settings.setValue(
            "filters/weather_code",
            "weather_code" in self.weatherVariables
        )

        settings.setValue(
            "filters/temperature_2m",
            "temperature_2m" in self.weatherVariables
        )

        settings.setValue(
            "filters/pressure_msl",
            "pressure_msl" in self.weatherVariables
        )

    # Odczyt ustawień
    def restoreWeatherVariables(self):

        settings = QSettings()

        weatherVariables = set()

        # Jeśli zaznaczone wcześniej
        if settings.value("filters/weather_code", False, type=bool):
            weatherVariables.add("weather_code")

        if settings.value("filters/temperature_2m", False, type=bool):
            weatherVariables.add("temperature_2m")

        if settings.value("filters/pressure_msl", False, type=bool):
            weatherVariables.add("pressure_msl")

        return weatherVariables