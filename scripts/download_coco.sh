set -e  # Останавливаем скрипт при ошибке

DATASET_DIR="/datasets"
ZIP_FILE="$DATASET_DIR/coco128.zip"

# Создаем папку для датасетов
mkdir -p "$DATASET_DIR"

# Если архив с датасетом отсутствует, скачиваем
if [ ! -f "$ZIP_FILE" ]; then
    echo "⚡️ COCO128 dataset zip file not found. Downloading..."
    wget -O "$ZIP_FILE" https://github.com/ultralytics/assets/releases/download/v0.0.0/coco128.zip

    echo "✅ COCO128 dataset zip file successfully downloaded."
else
    echo "✅ COCO128 dataset zip file already exists. Skipping download."
fi