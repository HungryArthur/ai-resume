@echo off
chcp 65001 >nul
title AI Рекрутер - Запуск

echo ========================================
echo    🤖 AI Рекрутер - Запуск проекта
echo ========================================
echo.

:: Проверка наличия Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python не найден! Установите Python 3.11+
    pause
    exit /b 1
)

:: Вывод версии Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo 🐍 Обнаружен Python %%i
echo.

:: Создание виртуального окружения (если нет)
if not exist "venv\" (
    echo 📦 Создание виртуального окружения...
    python -m venv venv
    echo ✅ Окружение создано
) else (
    echo ✅ Виртуальное окружение уже существует
)
echo.

:: Активация окружения
call venv\Scripts\activate.bat

:: Установка зависимостей
echo 📥 Установка зависимостей...
pip install --upgrade pip >nul 2>nul
pip install -r requirements.txt
echo ✅ Зависимости установлены
echo.

:: Генерация данных для обучения (если нет)
if not exist "train_data.json" (
    echo 🔄 Генерация обучающих данных...
    python generate_data.py
    echo.
) else (
    echo ✅ Файл train_data.json уже существует
    echo.
)

:: Обучение модели (если ещё не обучена)
if not exist "my_hr_model\" (
    echo 🧠 Обучение модели (это займёт несколько минут)...
    echo.
    python train_model.py
    echo.
) else (
    echo ✅ Модель уже обучена (папка my_hr_model существует)
    echo.
)

:: Запуск Streamlit
echo 🚀 Запуск веб-интерфейса Streamlit...
echo.
echo 🌐 Открывайте браузер: http://localhost:8501
echo.
echo ⚠️ Для остановки нажмите Ctrl+C
echo ========================================
echo.

streamlit run app.py --server.port=8501

:: Если Streamlit закрыт
echo.
echo 👋 Приложение остановлено
pause