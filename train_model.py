import json
from sentence_transformers import SentenceTransformer, InputExample, losses, util
from torch.utils.data import DataLoader
import os

def load_training_data(path='train_data.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_pair_examples(data):
    """Создаем пары (anchor, positive) для MultipleNegativesRankingLoss"""
    examples = []
    for item in data:
        # Для этой функции потерь нужны только пары (положительные примеры)
        # Отрицательные примеры формируются внутри батча автоматически
        example = InputExample(texts=[item['anchor'], item['positive']])
        examples.append(example)
    return examples

def train_model(
    model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
    output_path='./my_hr_model',
    epochs=5,
    batch_size=16
):
    print()
    print(f"Загрузка базовой модели: {model_name}")
    print()
    model = SentenceTransformer(model_name)
    
    print()
    print("📂 Загрузка данных...")
    data = load_training_data()
    examples = create_pair_examples(data)
    print(f"📊 Примеров для обучения: {len(examples)}")
    
    train_dataloader = DataLoader(examples, shuffle=True, batch_size=batch_size)
    
    # Более стабильная функция потерь
    train_loss = losses.MultipleNegativesRankingLoss(model=model)
    
    print(f"🚀 Начало обучения ({epochs} эпох)...")
    
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=100,
        output_path=output_path,
        show_progress_bar=True
    )
    
    print(f"✅ Модель сохранена в: {output_path}")
    
    # Тестирование
    print("\n🧪 Быстрый тест модели...")
    test_vac = "Требуется Python разработчик Django PostgreSQL"
    test_good = "Разработчик Python Django опыт 5 лет PostgreSQL"
    test_bad = "Дизайнер интерфейсов Figma UX UI"
    
    emb_vac = model.encode(test_vac, convert_to_tensor=True, normalize_embeddings=True)
    emb_good = model.encode(test_good, convert_to_tensor=True, normalize_embeddings=True)
    emb_bad = model.encode(test_bad, convert_to_tensor=True, normalize_embeddings=True)
    
    score_good = util.cos_sim(emb_vac, emb_good)[0][0].item()
    score_bad = util.cos_sim(emb_vac, emb_bad)[0][0].item()
    
    print(f"Сходство с подходящим резюме: {score_good:.4f}")
    print(f"Сходство с неподходящим резюме: {score_bad:.4f}")
    print(f"Разрыв (Gap): {score_good - score_bad:.4f}")
    
    if score_good > score_bad and score_good > 0.5:
        print("✅ Модель работает корректно!")
    else:
        print("⚠️ Модель требует дообучения")

if __name__ == "__main__":
    if not os.path.exists('train_data.json'):
        print("❌ Файл train_data.json не найден! Запустите generate_data.py")
    else:
        train_model()