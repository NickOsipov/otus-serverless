import os
import pickle
import boto3
import numpy as np
from io import BytesIO
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def train_model():
    """
    Обучает модель Random Forest на датасете Iris
    """
    print("Загрузка датасета Iris...")
    
    # Загружаем датасет Iris
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Разделяем данные на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Размер обучающей выборки: {X_train.shape}")
    print(f"Размер тестовой выборки: {X_test.shape}")
    
    # Создаем и обучаем модель
    print("Обучение модели Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1
    )
    
    model.fit(X_train, y_train)
    
    # Оценка модели
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, train_pred)
    test_accuracy = accuracy_score(y_test, test_pred)
    
    print(f"Точность на обучающей выборке: {train_accuracy:.4f}")
    print(f"Точность на тестовой выборке: {test_accuracy:.4f}")
    
    # Выводим подробный отчет
    print("Отчет по классификации:")
    print(f"\n{classification_report(y_test, test_pred, target_names=iris.target_names)}")
    
    return model

def upload_model_to_s3(model):
    """
    Загружает обученную модель в S3 хранилище Yandex Cloud
    """
    print("Подготовка к загрузке модели в S3...")
    
    # Проверяем наличие необходимых переменных окружения
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')

    if not S3_ACCESS_KEY or not S3_SECRET_KEY:
        raise ValueError("Не заданы S3_ACCESS_KEY или S3_SECRET_KEY")

    print(f"Используем S3_ACCESS_KEY: {S3_ACCESS_KEY}")
    
    # Настройки для Yandex Cloud S3
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )
    
    bucket_name = os.getenv('S3_BUCKET_NAME', 'ml-model-storage')
    model_key = 'models/iris_model.pkl'
    
    try:
        # Сериализуем модель в байты
        model_buffer = BytesIO()
        pickle.dump(model, model_buffer)
        model_buffer.seek(0)
        
        # Загружаем модель в S3
        print(f"Загрузка модели в bucket: {bucket_name}, key: {model_key}")
        s3.put_object(
            Bucket=bucket_name,
            Key=model_key,
            Body=model_buffer.getvalue(),
            ContentType='application/octet-stream'
        )
        
        print("Модель успешно загружена в S3!")
        
        # Проверяем, что модель действительно загружена
        response = s3.head_object(Bucket=bucket_name, Key=model_key)
        print(f"Размер загруженной модели: {response['ContentLength']} байт")
        
    except Exception as e:
        print(f"Ошибка при загрузке модели в S3: {e}")
        raise e

def main():
    """
    Основная функция для обучения и сохранения модели
    """
    try:
        print("Начало процесса обучения модели Iris...")
        
        # Обучаем модель
        model = train_model()
        
        # Загружаем модель в S3
        upload_model_to_s3(model)
        
        print("Процесс обучения и загрузки модели завершен успешно!")
        
    except Exception as e:
        print(f"Ошибка в процессе обучения: {e}")
        raise e

if __name__ == "__main__":
    main()
