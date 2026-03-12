## Linux
### Скачивание
```bash
git clone https://github.com/hungryarthur/ai-resume
code ai-resume
```

### Дообучение модели
```bash
python train_model.py
```

### Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install --r requirements.txt
```


### Запуск программы
```bash
streamlit app.py
```



## Структура проекта
```
resume_matcher/
│
├── 📄 app.py                    # Главное приложение Streamlit (интерфейс)
├── 📄 utils.py                  # Вспомогательные функции (NLP, загрузка модели)
├── 📄 generate_data.py          # Генератор синтетических данных для обучения
├── 📄 train_model.py            # Скрипт дообучения модели (Fine-tuning)
│
├── 📄 requirements.txt          # Зависимости Python
├── 📄 .gitignore                # Игнорируемые файлы
├── 📄 README.md                 # Документация проекта
│
├── 📄 train_data.json           # Обучающая выборка (генерируется автоматически) ⚠️
└── 📂 my_hr_model/              # Дообученная модель (папка >500MB) ⚠️
```