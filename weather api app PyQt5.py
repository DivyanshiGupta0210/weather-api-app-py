# ed86485bf3a3f4e4c232561a45e4e306
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self) #alt + 0176 to get ° symbol 
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        # self.temp_label = QLabel("35°C", self) 
        # self.emoji_label = QLabel("☀️", self)
        # self.description_label = QLabel("Sunny", self)
        self.initUI()  #fn call
        self.setWindowIcon(QIcon("Visual Studio Code/py/py practice/PyQt5/weather icon.png"))
        self.setGeometry(450,150,300,200)

    #to avoid overlapping of the labels
    def initUI(self): #fn definition
        self.setWindowTitle("Weather App") 

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        #applying styles
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")


        self.setStyleSheet("""
        QLabel, QPushButton {
            font-family: Calibri;
        }
        QLineEdit#city_input {
            font-size: 40px;
            font-style: italic;
        }
        QPushButton#get_weather_button {
            font-size: 35px;
            font-weight: bold;
        }
        QLabel#temp_label {
            font-size: 40px;
        }
        QLabel#emoji_label {
            font-size: 40px;
            font-family: Segoe UI Emoji;
        }
        QLabel#description_label {
            font-size: 40px;
        }
        QLabel#city_label {
            font-size: 50px;
            font-style: italic;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather) #also runs if Enter key is pressed

    def get_weather(self):
        api_key = "ed86485bf3a3f4e4c232561a45e4e306"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}" #use ur code's var names

        try:
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()
            # print(data)
            if data ["cod"] == 200: #code for NO ERROR
                self.display_weather(data)

        # except HTTPError #inside requests module
        except requests.exceptions.HTTPError as http_error: #if code btw 400 and 500,like ERROR 404: city not found
            # print(response.status_code) 
            match response.status_code:
                case 400:
                    self.display_error("Bad request!\nPlease check your input.")
                case 401:
                    self.display_error("Unauthorized!\nInvalid API key.")
                case 403:
                    self.display_error("Forbidden!\nAccess is denied.")
                case 404:
                    self.display_error("City not found!")
                case 500:
                    self.display_error("Internal server error!\nPlease try again later.")
                case 502:
                    self.display_error("Bad gateway!\nInvalid response from the server.")
                case 503:
                    self.display_error("Service unvailable!\nServer is down.")
                case 504:
                    self.display_error("Gateway timeout!\nNo response from the server.")
                case _:
                    self.display_error(f"HTTP Error occured:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error!\nCheck your Internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error!\nThe request is timed out.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects!\nCheck the URL.")
        except requests.exceptions.RequestException as req_error: #for invalid url, etc
            self.display_error(f"Request Error:\n{req_error}") 

    def display_error(self,message):
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear() 

    def display_weather(self,data):
        temp_k = data["main"]["temp"]
    #    print(temp_k)
        temp_c = temp_k - 273.15
    #    print(temp_c)
        weather_id = data["weather"][0]["id"] #to get the weather condition ID
        weather_description = data["weather"][0]["description"] #to get weather description, like sunny/cloudy etc

        self.temp_label.setText(f"{temp_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.title())
    
    @staticmethod
    def get_weather_emoji(weather_id):

        '''Weather Condition IDs: ["weather"][0]["id"] 
        2xx: thunderstorm
        3xx: drizzle
        5xx: rain
        6xx: snow
        7xx: atmosphere
        800: clear
        80x: clouds'''

        #method 1: using else-if statements
        #method 2: using match-case statements
        match weather_id:
            case _ if 200 <= weather_id <= 232:
                return "⛈️"
            case _ if 300 <= weather_id <= 321:
                return "🌦️"
            case _ if 500 <= weather_id <= 531:
                return "🌧️"
            case _ if 600 <= weather_id <= 622:
                return "❄️"
            case _ if 701 <= weather_id <= 741:
                return "🌫️"
            case 762:
                return "🌋"
            case 771:
                return "🍃"
            case 781:
                return "🌪️"
            case 800:
                return "☀️"
            case _ if 801 <= weather_id <= 804:
                return "☁️"
            case  _:
                return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = weatherapp()
    weather_app.show() 
    sys.exit(app.exec_())