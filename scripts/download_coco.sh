#!/bin/bash
set -e  # Останавливаем скрипт при ошибке

DATASET_DIR="/app/datasets/coco128"
CONFIG_FILE="/app/datasets/coco128.yaml"

# Создаем папку для датасетов
mkdir -p /app/datasets

# Если датасет отсутствует, скачиваем
if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚡️ COCO128 dataset not found. Downloading..."
    wget -O /app/datasets/coco128.yaml https://ultralytics.com/assets/coco128.yaml

    mkdir -p "$DATASET_DIR"
    wget -O /app/datasets/coco128.zip https://ultralytics.com/assets/coco128.zip
    unzip /app/datasets/coco128.zip -d /app/datasets/
    rm /app/datasets/coco128.zip  # Удаляем архив после распаковки

    echo "✅ COCO128 dataset successfully downloaded."
else
    echo "✅ COCO128 dataset already exists. Skipping download."
fi