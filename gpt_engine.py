import openai
import yaml
import os

DB_PATH = "db/plant_db.yaml"
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def save_db(db):
    os.makedirs("db", exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        yaml.dump(db, f, allow_unicode=True)

def get_or_generate_plant_info(plant_name: str):
    db = load_db()
    if plant_name in db:
        return db[plant_name]

    system_prompt = "Ты — агроном. Дай подробную информацию о растении в формате YAML: название, тип, описание, уход (полив, обрезка, подкормка), болезни и вредители, приживаемость по регионам России, размножение."
    user_prompt = f"Расскажи про {plant_name}. Ответ строго в YAML."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
    )

    content = response['choices'][0]['message']['content']
    try:
        parsed = yaml.safe_load(content)
        db[plant_name] = parsed
        save_db(db)
        return parsed
    except:
        return {"название": plant_name, "описание": "Ошибка: не удалось разобрать ответ от GPT."}
