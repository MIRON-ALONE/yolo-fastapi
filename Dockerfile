# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы, включая OpenGL
RUN apt-get update && apt-get install -y libgl1-mesa-glx ffmpeg libsm6 libxext6

# Копируем файлы проекта
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

