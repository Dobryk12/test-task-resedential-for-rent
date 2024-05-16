# Асинхронний збір даних про нерухомість для оренди

Цей скрипт збирає дані про нерухомість для оренди з веб-сайту [realtylink.org](https://realtylink.org/en/properties~for-rent) за допомогою асинхронного підходу. Він використовує бібліотеку `asyncio` для асинхронного виконання запитів.

## Встановлення

1. Склонуйте репозиторій:

    ```bash
    git clone https://github.com/Dobryk12/test-task-resedential-for-rent.git
    ```

2. Встановіть залежності:

    ```bash
    pip install -r requirements.txt
    ```

3. Запустіть скрипт:

    ```bash
    python main.py
    ```

## Інструкція користувача

Скрипт автоматично збирає дані про нерухомість для оренди з веб-сайту [realtylink.org](https://realtylink.org/en/properties~for-rent). Результати зберігаються у файлі `realty_data.json`.

## Структура JSON-файлу

```json
[
    {
        "link": "Посилання на нерухомість",
        "title": "Назва нерухомості",
        "region": "Регіон",
        "address": "Адреса",
        "description": "Опис нерухомості",
        "images": ["Посилання на зображення"],
        "price": "Ціна",
        "rooms": "Кількість кімнат",
        "square": "Площа"
    },
    ...
]