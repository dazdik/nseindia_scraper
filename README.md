
# Веб-скрапинг NSEIndia

## Описание
Этот проект содержит скрипт на Python, который использует Selenium для сбора данных с веб-сайта Национальной фондовой биржи Индии (https://www.nseindia.com/). Скрипт осуществляет навигацию по сайту, взаимодействует с элементами меню, переходит по страницам и извлекает конкретные финансовые данные, выводя итоговые результаты в файл CSV.

## Зависимости
- Python 3.x
- Selenium
- pandas
- fake_useragent
- Chrome WebDriver

Зависимости устанавливаются с помощью `poetry`. Для установки запустите:
```
poetry install
```

## Использование
Запустите скрипт с помощью Python 3.x. Убедитесь, что Chrome WebDriver правильно настроен в вашем PATH.

```
python scraper.py
```

## Рабочий процесс скрипта
- Скрипт инициализирует WebDriver Selenium с опциями Chrome.
- Переходит на сайт NSE Индия.
- Наводит курсор на меню 'Market Data' и выбирает 'Pre Open Market'.
- Извлекает данные о 'Final Price' из таблицы.
- Следует сценарию пользователя, переходя на различные части сайта и взаимодействуя с разными элементами.
- Выводит собранные данные в файл `final_prices.csv`.

## Выходные данные
Скрипт генерирует файл CSV под названием `final_prices.csv`, содержащий два столбца: `Имя` и `Цена`.

