import os
import json
import pickle
import boto3
import numpy as np
from io import BytesIO
from dotenv import load_dotenv


# Загружаем переменные окружения из .env файла
load_dotenv()

# Глобальная переменная для кэширования модели
model = None

def load_model_from_s3():
    """Загружает модель из S3 хранилища"""
    global model
    
    if model is not None:
        print("Модель уже загружена, возвращаем кэшированную версию.")
        return model
    
    print("Загрузка модели из S3...")
    # Проверяем наличие необходимых переменных окружения
    s3_access_key = os.getenv('S3_ACCESS_KEY')
    s3_secret_key = os.getenv('S3_SECRET_KEY')

    print(f"Используем AWS_ACCESS_KEY_ID: {s3_access_key}")
    
    # Настройки для Yandex Cloud S3
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key
    )
    
    bucket_name = os.getenv('S3_BUCKET_NAME', 'ml-model-storage')
    model_key = 'models/iris_model.pkl'
    
    try:
        # Загружаем модель из S3
        response = s3.get_object(Bucket=bucket_name, Key=model_key)
        model_data = response['Body'].read()
        
        # Десериализуем модель
        model = pickle.load(BytesIO(model_data))
        print("Модель успешно загружена из S3")
        return model
        
    except Exception as e:
        print(f"Ошибка при загрузке модели из S3: {e}")
        raise e

def predict(model, features):
    """
    Функция для предсказания класса и вероятностей
    Возвращает кортеж (predicted_class, probabilities)
    """
    X = np.array([features])
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    return prediction, probability

def handler(event, context):
    """
    Функция-обработчик для Yandex Cloud Functions
    Принимает данные о цветке ириса и возвращает предсказание вида
    """
    global model

    try:
        # Загружаем модель если она еще не загружена
        print("Загрузка модели для предсказания...")
        model = load_model_from_s3()
        
        # Парсим входные данные
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        print(f"Полученные данные: {body}")
        # Извлекаем признаки с переименованными полями
        features = [
            body.get('sepal_length', 0),
            body.get('sepal_width', 0),
            body.get('petal_length', 0),
            body.get('petal_width', 0)
        ]
        
        print(f"Извлеченные признаки: {features}")
        # Проверяем корректность входных данных
        if any(f <= 0 for f in features):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Все признаки должны быть положительными числами'
                })
            }
        
        # Преобразуем в numpy массив для предсказания
        X = np.array([features])
        
        
        # Делаем предсказание
        print("Делаем предсказание...")
        prediction, probability = predict(model, features)
        
        # Мапинг классов на названия видов
        species_names = ['setosa', 'versicolor', 'virginica']
        predicted_species = species_names[prediction]

        # Формируем ответ
        print(f"Предсказанный вид: {predicted_species}, вероятности: {probability}")
        
        response = {
            'predicted_species': predicted_species,
            'predicted_class': int(prediction),
            'probabilities': {
                species_names[i]: float(prob) 
                for i, prob in enumerate(probability)
            },
            'confidence': float(max(probability))
        }

        print("Предсказание успешно выполнено")
        
        return {
            'statusCode': 200,
            'body': json.dumps(response, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Ошибка при обработке запроса: {str(e)}'
            }, ensure_ascii=False)
        }
