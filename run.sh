#!/bin/bash

echo "========================================"
echo "   🤖 AI Рекрутер - Запуск проекта"
echo "========================================"

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python не найден!"
    exit 1
fi

echo "🐍 Обнаружен Python $(python3 --version)"
echo ""

# Виртуальное окружение
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация
source venv/bin/activate

# Зависимости
echo "📥 Установка зависимостей..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Зависимости установлены"
echo ""

# Данные для обучения
if [ ! -f "train_data.json" ]; then
    echo "🔄 Генерация обучающих данных..."
    python generate_data.py
    echo ""
fi

# Обучение
if [ ! -d "my_hr_model" ]; then
    echo "🧠 Обучение модели..."
    python train_model.py
    echo ""
fi

# Запуск
echo "🚀 Запуск Streamlit: http://localhost:8501"
streamlit run app.py --server.port=8501