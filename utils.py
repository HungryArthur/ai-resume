import razdel
import nltk
import re
import os
import pdfplumber
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import stopwords

# ИНИЦИАЛИЗАЦИЯ
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('russian'))

# IT-навыки
IT_SKILLS = {
    'python', 'golang', 'go', 'java', 'javascript', 'typescript', 'cpp', 'c', 'c#', 'rust',
    'django', 'flask', 'fastapi', 'spring', 'react', 'vue', 'angular', 'gin', 'gorm',
    'postgresql', 'mysql', 'mongodb', 'redis', 'clickhouse', 'elasticsearch', 'sqlite',
    'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'jenkins', 'gitlab', 'github',
    'grpc', 'rest', 'graphql', 'kafka', 'rabbitmq', 'websocket', 'oauth', 'jwt', 'ci', 'cd',
    'microservice', 'microservices', 'solid', 'tdd', 'bdd', 'agile', 'scrum', 'node', 'js'
}

hr_stop_words = {
    'резюме', 'вакансия', 'требование', 'обязанность', 'условие', 
    'предлагать', 'искать', 'работать', 'опыт', 'год', 'месяц',
    'зарплата', 'оклад', 'рубль', 'должность', 'компания', 'фирма', "работа", "команда",
    'разработчик', 'программист', 'инженер', 'специалист', 'ведущий', 'старший', 'младший', "2gis", "2гис"
}
stop_words.update(hr_stop_words)

# ЗАГРУЗКА МОДЕЛИ
_model_cache = None # Кэшируем модель в глобальной переменной, чтобы не грузить каждый раз

def load_model():
    global _model_cache
    if _model_cache is not None:
        return _model_cache
    
    model_path = './my_hr_model' if os.path.exists('./my_hr_model') else 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
    print(f"Loading model from: {model_path}")
    _model_cache = SentenceTransformer(model_path)
    return _model_cache

def extract_text_from_pdf(file_path):
    """Извлечение текста с помощью pdfplumber (лучше сохраняет структуру)"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        return f"Ошибка чтения PDF: {str(e)}"

def clean_text(text):
    if not text:
        return ""
    # Убираем HTML, URL, Emails, Телефоны
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\+?\d[\d\s\-\(\)]{9,}', '', text)
    
    # Заменяем спецсимволы на пробелы, но оставляем буквы и цифры
    # C# -> C # -> (потом разобьется на слова)
    text = re.sub(r'[^\w\sа-яА-ЯёЁ]', ' ', text)
    return text.lower().strip()

def lemmatize_text(text):
    words = razdel.tokenize(text)
    lemmatized = []
    for token in words:
        word = token.text.lower()
        if word in stop_words or len(word) <= 2:
            continue
        lemmatized.append(word)  # razdel уже нормализует
    return ' '.join(lemmatized)

def preprocess_text(text):
    text = clean_text(text)
    text = lemmatize_text(text)
    return text

def calculate_similarity(vacancy_text, resume_text, model):
    # Убрали normalize_embeddings=True для совместимости версий
    embedding_vacancy = model.encode(vacancy_text, convert_to_tensor=True)
    embedding_resume = model.encode(resume_text, convert_to_tensor=True)
    
    # util.cos_sim сам считает косинусное сходство (нормализует внутри)
    cosine_score = util.cos_sim(embedding_vacancy, embedding_resume)
    return float(cosine_score[0][0])

def extract_keywords(text, top_n=15):
    """Извлечение ключевых навыков"""
    words = text.split()
    word_freq = {}
    
    for word in words:
        if word in stop_words or len(word) <= 2:
            continue
        
        # Бонус для IT-навыков
        # Проверяем и оригинал, и варианты (на случай если c# разбилось на c)
        bonus = 1
        if word in IT_SKILLS:
            bonus = 3
        # Дополнительная проверка для составных, если нужно (опционально)
            
        word_freq[word] = word_freq.get(word, 0) + bonus
    
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    result = []
    # Слова-паразиты, которые могут просочиться
    generic_words = {'который', 'также', 'продукт', 'сервис', 'работа', 'опыт', 'уметь', 'знать'}
    
    for word, freq in sorted_words:
        if word not in generic_words:
            result.append(word)
            if len(result) >= top_n:
                break
    return result

def get_match_level(score):
    if score >= 0.8:
        return "Отличное", "🟢"
    elif score >= 0.6:
        return "Хорошее", "🟡"
    elif score >= 0.4:
        return "Среднее", "🟠"
    else:
        return "Низкое", "🔴"
