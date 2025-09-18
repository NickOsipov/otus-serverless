# Пример настройки секретов для GitHub Actions
# Скопируйте это в Settings → Secrets and variables → Actions вашего GitHub репозитория

# S3 секреты (для работы с Object Storage)
S3_ACCESS_KEY=YOUR_ACCESS_KEY_HERE
S3_SECRET_KEY=YOUR_SECRET_KEY_HERE

# Yandex Cloud секреты (для автоматического деплоя функций)
YC_FOLDER_ID=b1g123456789abcdef  # ID каталога в Yandex Cloud
YC_SA_JSON_CREDENTIALS={
  "id": "aje123456789abcdef",
  "service_account_id": "aje123456789abcdef", 
  "created_at": "2023-01-01T00:00:00Z",
  "key_algorithm": "RSA_2048",
  "public_key": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
}

# Команды для получения реальных значений:
```bash
yc resource-manager folder list  # для YC_FOLDER_ID
yc iam service-account create --name github-actions-sa
yc iam key create --service-account-name github-actions-sa --output key.json
```
