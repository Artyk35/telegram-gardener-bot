import yaml

def format_plant_info(data):
    if "описание" in data and "Ошибка" in data["описание"]:
        return data["описание"]

    response = f"""🌿 *{data.get('название', 'Неизвестно')}*
Тип: {data.get('тип', '-')}
Описание: {data.get('описание', '-')}

🧪 *Уход:*
Полив: {data.get('уход', {}).get('полив', '-')}
Обрезка: {data.get('уход', {}).get('обрезка', '-')}
Подкормка: {data.get('уход', {}).get('подкормка', '-')}

🦠 *Болезни и вредители:* {", ".join(data.get('болезни_и_вредители', []))}

📍 *Приживаемость по регионам:*
```yaml
{yaml.dump(data.get('приживаемость', {}), allow_unicode=True)}
```

🌱 *Размножение:* {data.get('размножение', '-')}
"""
    return response
