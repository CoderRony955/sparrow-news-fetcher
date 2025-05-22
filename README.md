<p align="center">
  <img src="imgs\sparrow_news_fetcher.png">
</p>

# Sparrow News Fetcher

A simple and elegant desktop application built with Python and PyQt6 that fetches the latest news headlines using the [NewsAPI](https://newsapi.org/ ). This app provides an very simple GUI where user just add their auth-token and fetches the latest news by just searching a single word.

## Interface

<p align="center">
  <img src="screenshots\interface.png">
</p>

## Usage

<p align="center">
  <img src="screenshots\auth_token.png">
</p>

first go to the [NewsAPI](https://newsapi.org/ ) and get your api-key url, and the api-key url should like this `e.g. https://newsapi.org/v2/everything?q=tesla&from=2025-04-22&sortBy=publishedAt&apiKey=your-auth-token-here`. Then just add your auth-token and search a single keyword and hit enter in youtr keyboard. You will get the news headlines in `JSON` format in the app.

## Installation

1. Clone the repository
```
git clone https://github.com/CoderRony955/sparrow-news-fetcher.git
```
2. Move to the cloned directory
```
cd sparrow-news-fetcher
```

3. Create a virtual environment
- **Windows**
```
python -m venv venv
```
- **Linux**
```
python3 -m venv venv
```

4. Activate the virtual environment
- **Windows**
```
.\venv\Scripts\activate.ps1
```
- **Linux**
```
source venv/bin/activate
```

5. Install the dependencies
```
pip install -r requirements.txt
```

6. Move to the main app directory
```
cd main  
```

7. Run the application
```
python main.py
```

## License

This project is distributed under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license.

## Author

[Raunak Sharma](https://github.com/CoderRony955)
