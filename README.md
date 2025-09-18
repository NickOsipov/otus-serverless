# Otus Serverless ML Project

Проект по развертыванию модели машинного обучения в виде serverless-функции в Yandex Cloud.

## Описание

Этот проект демонстрирует полный цикл MLOps для модели классификации ирисов:
- Обучение модели на датасете Iris
- Сохранение модели в S3 хранилище Yandex Cloud
- Развертывание модели в виде serverless-функции
- CI/CD пайплайн с GitHub Actions

## Структура проекта

```
otus-serverless/
├── src/
│   ├── main.py         # Serverless функция для предсказаний
│   └── train.py        # Скрипт обучения модели
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml  # CI/CD пайплайн
├── requirements.txt    # Зависимости Python
└── README.md          # Документация
```

## Компоненты

### 1. Обучение модели (`src/train.py`)
- Загружает датасет Iris из scikit-learn
- Обучает модель Random Forest
- Сохраняет модель в S3 bucket `ml-model-storage`

### 2. Serverless функция (`src/main.py`)
- Загружает модель из S3
- Принимает данные о цветке ириса
- Возвращает предсказание вида

### 3. CI/CD пайплайн (`.github/workflows/ml-pipeline.yml`)
- **Job 1**: Обучение модели и загрузка в S3
- **Job 2**: Развертывание исходного кода в S3
- **Job 3**: Интеграционные тесты

## Настройка

### 1. Переменные окружения
Добавьте в GitHub Secrets следующие переменные:
- `AWS_ACCESS_KEY_ID` - ID ключа доступа для Yandex Cloud
- `AWS_SECRET_ACCESS_KEY` - Секретный ключ доступа для Yandex Cloud

### 2. S3 buckets в Yandex Cloud
Создайте два bucket'а:
- `ml-model-storage` - для хранения обученных моделей
- `ml-serverless-source-code` - для хранения исходного кода

### 3. Локальная разработка
```bash
# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
echo "AWS_ACCESS_KEY_ID=your_key_id" > .env
echo "AWS_SECRET_ACCESS_KEY=your_secret_key" >> .env

# Обучение модели
cd src
python train.py
```

## API функции

### Запрос
```json
{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
```

### Ответ
```json
{
    "predicted_species": "setosa",
    "predicted_class": 0,
    "probabilities": {
        "setosa": 0.95,
        "versicolor": 0.03,
        "virginica": 0.02
    },
    "confidence": 0.95
}
```

## Развертывание в Yandex Cloud

1. Создайте Cloud Function в Yandex Cloud
2. Настройте переменные окружения в функции
3. Загрузите код из bucket `ml-serverless-source-code`
4. Настройте API Gateway для HTTP доступа

## Мониторинг

Пайплайн включает:
- Проверку загрузки модели
- Тестирование предсказаний
- Верификацию загрузки файлов в S3

## Структура данных Iris

| Признак | Описание |
|---------|----------|
| sepal_length | Длина чашелистика |
| sepal_width | Ширина чашелистика |
| petal_length | Длина лепестка |
| petal_width | Ширина лепестка |

**Классы:**
- 0: setosa
- 1: versicolor  
- 2: virginica
