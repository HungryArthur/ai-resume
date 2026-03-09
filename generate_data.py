import json
import random

# --- Шаблоны вакансий (Расширено) ---
VACANCIES = [
    {"role": "Python Backend", "text": "Требуется Python разработчик. Навыки: Django, REST API, PostgreSQL, Docker, Git. Опыт от 3 лет.", "category": "backend"},
    {"role": "Python Backend 2", "text": "Вакансия Backend Developer. Стек: Python, FastAPI, SQLAlchemy, Redis, Linux. Удаленная работа.", "category": "backend"},
    {"role": "Frontend Dev", "text": "Ищем фронтенд разработчика. Требуется: React, TypeScript, HTML, CSS, Webpack. Опыт коммерческой разработки.", "category": "frontend"},
    {"role": "Frontend Dev 2", "text": "Разработчик интерфейсов. JavaScript, Vue.js, Redux, API integration. Работа в офисе.", "category": "frontend"},
    {"role": "Data Scientist", "text": "Вакансия Data Scientist. Стек: Python, Pandas, Scikit-learn, PyTorch, SQL, ML. Высшее техническое образование.", "category": "data"},
    {"role": "Data Analyst", "text": "Аналитик данных. SQL, Python, Tableau, Excel. Дашборды, A/B тесты, статистика, отчетность.", "category": "data"},
    {"role": "DevOps", "text": "Требуется DevOps инженер. Обязанности: CI/CD, Kubernetes, Linux, AWS, Terraform, Monitoring.", "category": "devops"},
    {"role": "DevOps 2", "text": "Инженер инфраструктуры. Docker, Ansible, Jenkins, Prometheus, Grafana, Bash scripting.", "category": "devops"},
    {"role": "Java Dev", "text": "Разработчик Java. Требования: Spring Boot, Maven, Hibernate, PostgreSQL, Microservices, Git.", "category": "java"},
    {"role": "QA Engineer", "text": "Тестировщик ПО. Manual testing, Selenium, Pytest, JIRA. Автотесты, баг репорты, регресс.", "category": "qa"},
    {"role": "Manager", "text": "Менеджер проектов. Agile, Scrum, Jira, Confluence. Управление командой, планирование, коммуникация.", "category": "other"},
    {"role": "Designer", "text": "UX/UI Дизайнер. Figma, Adobe XD, прототипирование, дизайн-системы, мобильные приложения.", "category": "other"},
]

# --- Шаблоны резюме (Расширено) ---
RESUMES = {
    "backend": [
        "Разработчик Python. Опыт 5 лет. Стек: Django, FastAPI, PostgreSQL, Docker. Делал REST API для финтеха.",
        "Backend инженер. Пишу на Python 3 года. Знаю Flask, SQLAlchemy, Redis, Celery, Git, Linux.",
        "Senior Python Developer. Архитектура микросервисов, Kubernetes, CI/CD, PostgreSQL, оптимизация запросов.",
        "Python программист. Разработка веб-приложений, Django REST Framework, MySQL, Nginx, Gunicorn.",
        "Backend Developer. Python, asyncio, aiohttp, RabbitMQ, MongoDB, микросервисная архитектура."
    ],
    "frontend": [
        "Frontend разработчик. React, Redux, TypeScript. Опыт 4 года. Верстка, адаптив, работа с дизайнерами.",
        "JavaScript разработчик. Vue.js, Webpack, HTML5, CSS3. Делал SPA приложения для e-commerce.",
        "Senior Frontend. React Native, Next.js, GraphQL. Менторство, код ревью, архитектура фронтенда.",
        "Web разработчик. Angular, RxJS, SASS, Bootstrap. Интеграция с бэкендом, оптимизация производительности.",
        "UI Developer. JavaScript ES6+, React Hooks, Tailwind CSS, Storybook, тестирование Jest."
    ],
    "data": [
        "Data Scientist. ML модели, Python, Pandas, Scikit-learn, PyTorch. Анализ данных, прогнозирование.",
        "Аналитик данных. SQL, Python, Tableau, Excel. Дашборды, A/B тесты, статистика, отчетность.",
        "Machine Learning Engineer. Deep Learning, NLP, Computer Vision, TensorFlow, Kubernetes, MLOps.",
        "Data Engineer. ETL пайплайны, Apache Spark, Airflow, Kafka, BigQuery, облачные хранилища.",
        "Аналитик BI. Power BI, SQL, DAX, моделирование данных, визуализация, бизнес-метрики."
    ],
    "devops": [
        "DevOps инженер. AWS, Docker, Kubernetes, Terraform. CI/CD пайплайны, мониторинг Prometheus, Grafana.",
        "Системный администратор. Linux, Bash, Python, Ansible. Настройка серверов, безопасность, бэкапы.",
        "Cloud Engineer. Azure, GCP, Terraform, Helm. Миграция в облако, оптимизация затрат, инфраструктура.",
        "SRE инженер. Мониторинг, инцидент-менеджмент, SLA, автоматизация, отказоустойчивость систем.",
        "Infrastructure Developer. Vagrant, Packer, Consul, Vault, service mesh, Istio, networking."
    ],
    "java": [
        "Java разработчик. Spring Framework, Hibernate, Maven, Gradle. Микросервисы, REST, SOAP.",
        "Backend Java. JPA, MySQL, Oracle, Tomcat, Jetty. Многопоточность, оптимизация JVM.",
        "Senior Java Developer. Kafka, Redis, Elasticsearch, Docker, Kubernetes, CI/CD.",
        "Java программист. Android, Kotlin, Gradle, Retrofit, Room, MVVM архитектура.",
        "Enterprise Java. JEE, EJB, JMS, WebLogic, WebSphere, корпоративные системы."
    ],
    "qa": [
        "QA Engineer. Manual testing, Selenium, Pytest, JIRA. Автотесты, баг репорты, регрессионное тестирование.",
        "Тестировщик ПО. Postman, Swagger, API testing, SQL, клиент-серверная архитектура.",
        "SDET. Java, TestNG, Cucumber, Jenkins, GitLab CI, автоматизация тестирования.",
        "QA Lead. Управление командой тестирования, стратегия тестирования, метрики качества.",
        "Performance Tester. JMeter, LoadRunner, нагрузочное тестирование, профилирование."
    ],
    "other": [
        "Менеджер проектов. Agile, Scrum, Jira. Управление командой 10 человек, планирование спринтов.",
        "Дизайнер интерфейсов. Figma, UX/UI, прототипирование. Дизайн мобильных приложений и веб.",
        "Маркетолог. Контекстная реклама, Яндекс Директ, Google Ads, аналитика, SEO продвижение.",
        "HR менеджер. Рекрутинг, собеседования, адаптация сотрудников, HR-бренд, KPI.",
        "Продакт менеджер. Product Vision, Roadmap, CustDev, метрики продукта, гипотезы."
    ]
}

def generate_training_data(num_samples=1000):
    """Генерация пар для обучения"""
    train_data = []
    categories = list(RESUMES.keys())
    
    for i in range(num_samples):
        vacancy = random.choice(VACANCIES)
        vac_category = vacancy['category']
        
        # Positive: резюме из той же категории
        positive_resume = random.choice(RESUMES.get(vac_category, RESUMES['backend']))
        
        # Negative: резюме из ДРУГОЙ категории
        other_categories = [c for c in categories if c != vac_category]
        negative_resume = random.choice(RESUMES[random.choice(other_categories)])
        
        train_data.append({
            "anchor": vacancy["text"],
            "positive": positive_resume,
            "negative": negative_resume
        })
    
    return train_data

if __name__ == "__main__":
    print("🔄 Генерация синтетических данных...")
    data = generate_training_data(1000)
    
    with open('train_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Создано {len(data)} обучающих примеров")
    print("📁 Файл сохранен: train_data.json")