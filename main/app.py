from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QToolBar,
    QLabel,
    QMessageBox,
    QTextBrowser

)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QAction, QIcon, QPixmap
import requests
import json
from datetime import datetime, timedelta, date
from pathlib import Path
from dotenv import load_dotenv
import os
import re


class gui(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        self.setWindowTitle('Sparrow News Fetcher')
        self.setWindowIcon(
            QIcon('logo/sparrow.png'))
        self.resize(1000, 600)

        vlabel = QVBoxLayout()
        # hlable = QHBoxLayout()

        load_dotenv()

        self.api_key = os.getenv("API_KEY")
        self.default_url = os.getenv("DEFAULT_URL")

        toolbar = QToolBar("ToolBar")
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        new_action = QAction(QIcon(), "API KEY", self)
        new_action.setStatusTip("Enter the API KEY")
        new_action.triggered.connect(self.open_api_key_win)
        toolbar.addAction(new_action)

        self.QuerySearchBox = QLineEdit()
        self.QuerySearchBox.setFixedSize(450, 50)
        self.QuerySearchBox.setFont(QFont("Arial", 10, QFont.Weight.DemiBold))

        self.QuerySearchBox.setPlaceholderText('e.g. Iphone and Press Enter')
        self.QuerySearchBox.setObjectName('QuerySearcherBox')

        self.output = QTextBrowser()
        self.output.setPlaceholderText('fetch latest news by using Newsapi!')
        self.output.setReadOnly(True)
        self.output.setObjectName('output')

        self.get_news_btn = QPushButton()
        self.get_news_btn.setFont(QFont("Arial", 10, QFont.Weight.DemiBold))
        self.get_news_btn.setObjectName('get-news-button')
        self.get_news_btn.setFixedSize(250, 30)
        self.get_news_btn.clicked.connect(self.get_news)

        self.QuerySearchBox.returnPressed.connect(self.get_news_btn.click)

        vlabel.addWidget(
            self.QuerySearchBox, alignment=Qt.AlignmentFlag.AlignCenter)
        vlabel.addWidget(self.output)

        central_widget.setLayout(vlabel)

    def convert_urls_to_links(self, text):
        url_pattern = re.compile(r'(https?://\S+)')
        return url_pattern.sub(r'<a href="\1">\1</a>', text)

    def get_news(self):
        try:
            api_key = os.getenv('API_KEY')
            query = self.QuerySearchBox.text().strip()
            from_date = datetime.today() - timedelta(days=30)
            url = f'https://newsapi.org/v2/everything?q={query}&from={from_date}&sortBy=publishedAt&apiKey={api_key}'
            if not query:
                QMessageBox.warning(
                    self,
                    'something went wrong',
                    str('Please enter a search query.'),
                    QMessageBox.StandardButton.Ok
                )
                return

            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                formatted = json.dumps(json_data, indent=4)

                html_output = f"<pre>{self.convert_urls_to_links(formatted)}</pre>"

                self.output.setOpenExternalLinks(True)
                self.output.setTextInteractionFlags(
                    Qt.TextInteractionFlag.TextSelectableByMouse |
                    Qt.TextInteractionFlag.LinksAccessibleByMouse
                )
                self.output.setHtml(html_output)
        except requests.exceptions.ConnectionError as e:
            QMessageBox.critical(
                self,
                'something went wrong',
                str(e),
                QMessageBox.StandardButton.Close
            )
        except requests.exceptions.HTTPError as e:
            QMessageBox.critical(
                self,
                'something went wrong',
                str(e),
                QMessageBox.StandardButton.Close
            )
        except requests.exceptions.Timeout as e:
            QMessageBox.critical(
                self,
                'something went wrong',
                str(e),
                QMessageBox.StandardButton.Close
            )

    def open_api_key_win(self):
        self.api_key_win = API_KEY_WINDOW()
        self.api_key_win.show()


class API_KEY_WINDOW(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        self.setWindowTitle('Enter News API KEY')
        self.setWindowIcon(
            QIcon('logo/sparrow.png'))
        self.setFixedSize(400, 240)

        vlabel = QVBoxLayout()

        self.banner_label = QLabel(self)
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap(
            "imgs/api_key_banner.png")
        scaled_pixmap = pixmap.scaled(
            QSize(self.width(), 100),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.banner_label.setPixmap(scaled_pixmap)
        self.banner_label.setFixedHeight(100)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setObjectName('api-key-lineEdit')
        self.api_key_edit.setFixedSize(250, 30)

        btn = QPushButton()
        btn.setText('Enter')
        btn.setFont(QFont("Arial", 10, QFont.Weight.DemiBold))
        btn.setObjectName('api-key-enter-btn')
        btn.setFixedSize(100, 40)
        btn.clicked.connect(self.check_api_key)

        vlabel.addWidget(self.banner_label)
        vlabel.addWidget(self.api_key_edit,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        vlabel.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        central_widget.setLayout(vlabel)

    def check_api_key(self):
        try:
            if not self.api_key_edit.text().strip():
                mesasge = 'Please enter the API Key!'
                QMessageBox.warning(
                    self,
                    'something went wrong',
                    mesasge,
                    QMessageBox.StandardButton.Ok
                )
                return

            api_key = str(self.api_key_edit.text().strip())
            default_url = f'https://newsapi.org/v2/everything?q=tesla&from={date.today()}&sortBy=publishedAt&apiKey={api_key}'

            check = requests.get(default_url)

            if check.status_code != 200:
                QMessageBox.critical(
                    self,
                    'Invalid API Key',
                    str(f'your provided API Key {self.api_key_edit.text()} is invalid. Please try again with different API Key, if you don\'t know from where to claim News API Key then please visit https://newsapi.org to claim your News API Key'),
                    QMessageBox.StandardButton.Ok
                )
                return

            else:
                QMessageBox.information(
                    self,
                    f'{check.status_code}',
                    str(
                        f'your provided API Key {self.api_key_edit.text()} is valid :)\nstatus: {check.status_code}'),
                    QMessageBox.StandardButton.Ok
                )

                env_file = Path(
                    'C:/Users/1973r/OneDrive/Desktop/Python/sparrow/.env')
                lines = []

                if env_file.exists():
                    with env_file.open("r") as f:
                        for line in f:
                            if not line.startswith("API_KEY=") and not line.startswith("DEFAULT_URL="):
                                lines.append(line.strip())

                lines.append(f"API_KEY={self.api_key_edit.text()}")
                lines.append(f"DEFAULT_URL={default_url}")

                # Write back
                with env_file.open("w") as f:
                    f.write("\n".join(lines) + "\n")

                print(f".env file updated with API_KEY and DEFAULT_URL")
                return

        except requests.exceptions.ConnectionError as e:
            QMessageBox.critical(
                self,
                'something went wrong',
                str(e),
                QMessageBox.StandardButton.Close
            )
        except requests.exceptions.HTTPError as e:
            QMessageBox.critical(
                self,
                'something went wrong',
                str(e),
                QMessageBox.StandardButton.Close
            )
        except requests.exceptions.Timeout as e:
            QMessageBox.critical(
                self,
                'something went wrong',
                str(e),
                QMessageBox.StandardButton.Close
            )
