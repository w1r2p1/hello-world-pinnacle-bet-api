# Hello World using Pinnacle API with Python

This is a simple example to implement an automatic betting strategy using [Pinnacle API](https://pinnacleapi.github.io) and his [Python wrapper](https://github.com/rozzac90/pinnacle).

# Strategy implemented

During the first period of pre filtered match series. The system bets 5 euros to Over 0.5 if the odd is bigger than 1.8 and the match result is 0 - 0.

# To install

```bash
$ git clone https://github.com/bukosabino/hello-world-pinnacle-bet-api
$ cd hello-world-pinnacle-bet-api
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install requests
$ pip install pandas
$ pip install pinnacle
```

# To run

1. You need an available API Pinnacle account. In settings.py you should to fill USERNAME and PASSWORD variables. If your Pinnacle account has not API Pinnacle available you can contact with b2b@pinnaclesolution.com

2. You need to fill LISTA_IDS variable with ids pre-match filtered using statistics software like Betpractice (for example).

3. Run:

```bash
$ cd strategy
$ python bet_system.py
```

4. By default the system simulate the purchases. If you want enable this option, you need update the variable BUY_AVAILABLE with True value.

```
BUY_AVAILABLE = True
```

5. You can check the results.csv file using Microsoft Excel or Libre Office Calc. You can check how open a a file with .csv format.

# Pinnacle API Documentation

* https://pinnacleapi.github.io

* https://github.com/rozzac90/pinnacle

# Credits

Developed by Bukosabino - bukosabino@gmail.com

Please, let me know about any comment or feedback.

Note: This is a proof of concept software, you should use it at your own risk.
