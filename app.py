import streamlit as st
from utils import (
    load_model, preprocess_text, calculate_similarity, 
    extract_keywords, get_match_level, extract_text_from_pdf
)
import time

# --- Конфигурация страницы ---
st.set_page_config(
    page_title="AI Рекрутер",
    page_icon="🤖",
    layout="wide"
)

# --- Загрузка модели ---
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

# --- Заголовок ---
st.title("🤖 AI Рекрутер: Анализ соответствия резюме")
st.markdown("""
Этот сервис использует NLP и нейросети для оценки соответствия резюме требованиям вакансии.
Загрузите файлы или вставьте текст, чтобы получить оценку совместимости.
""")

# --- Боковая панель ---
st.sidebar.header("⚙️ Настройки")
show_details = st.sidebar.checkbox("Показать технические детали", value=False)
model_name = st.sidebar.text_input("Модель", value="paraphrase-multilingual-MiniLM-L12-v2", disabled=True)

# --- Основная часть ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Текст вакансии")
    vacancy_input_method = st.radio("Ввод вакансии", ["Текст", "Файл"], key="vacancy_method")
    
    vacancy_text = ""
    if vacancy_input_method == "Текст":
        vacancy_text = st.text_area("Вставьте описание вакансии", height=200, 
                                    placeholder="Требуется Python разработчик...")
    else:
        uploaded_vac = st.file_uploader("Загрузить файл (TXT, PDF)", type=['txt', 'pdf'], key="vac_file")
        if uploaded_vac:
            if uploaded_vac.name.endswith('.pdf'):
                vacancy_text = extract_text_from_pdf(uploaded_vac)
            else:
                vacancy_text = str(uploaded_vac.read(), "utf-8")
            st.text_area("Извлеченный текст", vacancy_text, height=200)

with col2:
    st.subheader("👤 Текст резюме")
    resume_input_method = st.radio("Ввод резюме", ["Текст", "Файл"], key="resume_method")
    
    resume_text = ""
    if resume_input_method == "Текст":
        resume_text = st.text_area("Вставьте текст резюме", height=200,
                                   placeholder="Опыт работы: 5 лет, навыки: Python...")
    else:
        uploaded_res = st.file_uploader("Загрузить файл (TXT, PDF)", type=['txt', 'pdf'], key="res_file")
        if uploaded_res:
            if uploaded_res.name.endswith('.pdf'):
                resume_text = extract_text_from_pdf(uploaded_res)
            else:
                resume_text = str(uploaded_res.read(), "utf-8")
            st.text_area("Извлеченный текст", resume_text, height=200)

# --- Кнопка анализа ---
st.divider()
if st.button("🚀 Оценить соответствие", type="primary", use_container_width=True):
    if vacancy_text and resume_text:
        # Прогресс бар
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Шаг 1: Предобработка
        status_text.text("⏳ Предобработка текста (лемматизация)...")
        time.sleep(0.5)
        vacancy_processed = preprocess_text(vacancy_text)
        resume_processed = preprocess_text(resume_text)
        progress_bar.progress(33)
        
        # Шаг 2: Векторизация и сходство
        status_text.text("🧠 Анализ семантики (BERT)...")
        time.sleep(0.5)
        similarity_score = calculate_similarity(vacancy_processed, resume_processed, model)
        progress_bar.progress(66)
        
        # Шаг 3: Ключевые слова
        status_text.text("🔑 Извлечение ключевых навыков...")
        time.sleep(0.5)
        vacancy_keywords = extract_keywords(vacancy_processed)
        resume_keywords = extract_keywords(resume_processed)
        progress_bar.progress(100)
        
        status_text.text("✅ Готово!")
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        # --- Результаты ---
        st.subheader("📊 Результаты анализа")
        
        # Метрика
        level, icon = get_match_level(similarity_score)
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        with col_metric1:
            st.metric("Оценка соответствия", f"{similarity_score:.2%}", delta=level)
        
        with col_metric2:
            st.metric("Уровень", level)
            
        with col_metric3:
            st.metric("Статус", icon)

        # Визуализация прогресса
        st.progress(similarity_score)
        
        # Детальный анализ
        if show_details:
            st.markdown("### 🔍 Технические детали")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.write("**Обработанный текст вакансии (превью):**")
                st.code(vacancy_processed[:300] + "...")
            with col_t2:
                st.write("**Обработанный текст резюме (превью):**")
                st.code(resume_processed[:300] + "...")

        # Ключевые слова
        st.markdown("### 🔑 Ключевые слова")
        col_kw1, col_kw2 = st.columns(2)
        
        with col_kw1:
            st.info(f"**Требования вакансии:** {', '.join(vacancy_keywords)}")
        
        with col_kw2:
            st.success(f"**Навыки в резюме:** {', '.join(resume_keywords)}")
            
        # Пересечение навыков
        common_skills = set(vacancy_keywords) & set(resume_keywords)
        if common_skills:
            st.success(f"✅ **Совпадающие навыки:** {', '.join(common_skills)}")
        else:
            st.warning("⚠️ Явных совпадений ключевых слов не найдено (возможно, использованы синонимы)")
            
        # Рекомендации
        st.markdown("### 💡 Рекомендации")
        if similarity_score >= 0.8:
            st.success("Кандидат отлично подходит! Рекомендуется пригласить на собеседование.")
        elif similarity_score >= 0.6:
            st.info("Кандидат подходит, но есть небольшие расхождения. Стоит уточнить детали на интервью.")
        elif similarity_score >= 0.4:
            st.warning("Соответствие среднее. Внимательно проверьте конкретные навыки.")
        else:
            st.error("Низкое соответствие. Скорее всего, кандидат не подходит под требования.")
            
    else:
        st.error("⚠️ Пожалуйста, заполните оба поля (вакансия и резюме)!")

# --- Футер ---
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Учебный проект | NLP & ML | 2024</small>
</div>
""", unsafe_allow_html=True)