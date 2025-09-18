#!/bin/bash

# Создание сервисного аккаунта и ключа для GitHub Actions
SERVICE_ACCOUNT_NAME=$1

yc iam service-account create --name $SERVICE_ACCOUNT_NAME
yc iam key create --service-account-name $SERVICE_ACCOUNT_NAME --output key.json

# Назначение ролей для деплоя функций
FOLDER_ID=$(yc config get folder-id)
SA_ID=$(yc iam service-account get $SERVICE_ACCOUNT_NAME --format json | jq -r '.id')

# Основные роли для деплоя
yc resource-manager folder add-access-binding $FOLDER_ID --role functions.admin --subject serviceAccount:$SA_ID
yc resource-manager folder add-access-binding $FOLDER_ID --role iam.serviceAccounts.user --subject serviceAccount:$SA_ID

# Дополнительные роли для работы с S3
yc resource-manager folder add-access-binding $FOLDER_ID --role storage.admin --subject serviceAccount:$SA_ID
