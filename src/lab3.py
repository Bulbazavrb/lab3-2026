"""
Лабораторна робота № 3: Структури даних у Python
Варіант: 12
Тема: Система управління ресторанним меню (страви, інгредієнти, ціни)
Студент: Шульга Дмитро Ігорович
Група: 12
"""

from collections import defaultdict
from functools import reduce
from typing import List, Dict, Set, Any


# 1. Початкова база даних ресторанного меню (список словників із множинами)
menu_data: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Борщ український",
        "category": "Перші страви",
        "price": 160.0,
        "weight_g": 350,
        "ingredients": {"яловичина", "буряк", "капуста", "картопля", "морква", "сметана"}
    },
    {
        "id": 2,
        "name": "Грибна юшка",
        "category": "Перші страви",
        "price": 140.0,
        "weight_g": 300,
        "ingredients": {"білі гриби", "картопля", "цибуля", "морква", "вершки"}
    },
    {
        "id": 3,
        "name": "Стейк Рібай",
        "category": "Основні страви",
        "price": 450.0,
        "weight_g": 300,
        "ingredients": {"яловичина", "розмарин", "часник", "вершкове масло"}
    },
    {
        "id": 4,
        "name": "Вареники з картоплею",
        "category": "Основні страви",
        "price": 130.0,
        "weight_g": 250,
        "ingredients": {"борошно", "картопля", "цибуля", "вершкове масло", "сметана"}
    },
    {
        "id": 5,
        "name": "Салат Цезар",
        "category": "Салати",
        "price": 210.0,
        "weight_g": 220,
        "ingredients": {"куряче філе", "салат ромен", "помідори чері", "пармезан", "соус цезар"}
    },
    {
        "id": 6,
        "name": "Салат Грецький",
        "category": "Салати",
        "price": 175.0,
        "weight_g": 240,
        "ingredients": {"помідори", "огірки", "сир фета", "маслини", "оливкова олія"}
    },
    {
        "id": 7,
        "name": "Чизкейк Нью-Йорк",
        "category": "Десерти",
        "price": 150.0,
        "weight_g": 150,
        "ingredients": {"крем-сир", "пісочне печиво", "вершкове масло", "ваніль"}
    },
    {
        "id": 8,
        "name": "Узвар",
        "category": "Напої",
        "price": 50.0,
        "weight_g": 400,
        "ingredients": {"сухофрукти", "яблука", "груші", "мед"}
    }
]


# 2. Функції базового управління (CRUD)

def add_dish(data: List[Dict[str, Any]], dish: Dict[str, Any]) -> None:
    """Додає нову страву до меню з унікальним числовим ID."""
    new_id = max([d["id"] for d in data], default=0) + 1
    dish["id"] = new_id
    data.append(dish)
    print(f"-> Страву '{dish['name']}' успішно додано під ID #{new_id}.")


def remove_dish(data: List[Dict[str, Any]], dish_id: int) -> bool:
    """Видаляє страву з меню за її ID."""
    for index, dish in enumerate(data):
        if dish["id"] == dish_id:
            removed = data.pop(index)
            print(f"-> Страву '{removed['name']}' (ID #{dish_id}) видалено.")
            return True
    print("-> Страву з таким ID не знайдено.")
    return False


def update_dish(data: List[Dict[str, Any]], dish_id: int, field: str, value: Any) -> bool:
    """Оновлює поле страви із перевіркою коректності типів даних."""
    for dish in data:
        if dish["id"] == dish_id:
            if field in ["price", "weight_g"]:
                try:
                    dish[field] = float(value) if field == "price" else int(value)
                except ValueError:
                    print("-> Помилка: ціна чи вага мають бути числами.")
                    return False
            elif field == "ingredients":
                dish[field] = {item.strip().lower() for item in str(value).split(",") if item.strip()}
            elif field in ["name", "category"]:
                dish[field] = str(value).strip()
            else:
                print("-> Невідоме поле для редагування.")
                return False
            print(f"-> Поле '{field}' страви #{dish_id} успішно оновлено.")
            return True
    print("-> Страву з таким ID не знайдено.")
    return False


# 3. Пошук, фільтрація та операції з множинами

def find_dishes_by_ingredient(data: List[Dict[str, Any]], ingredient: str) -> List[Dict[str, Any]]:
    """Знаходить страви за інгредієнтом за допомогою функції filter()."""
    target = ingredient.strip().lower()
    return list(filter(lambda dish: target in dish["ingredients"], data))


def filter_dishes_by_max_price(data: List[Dict[str, Any]], max_price: float) -> List[Dict[str, Any]]:
    """Фільтрує меню за максимальною вартістю."""
    return list(filter(lambda dish: dish["price"] <= max_price, data))


def get_all_unique_ingredients(data: List[Dict[str, Any]]) -> Set[str]:
    """Формує повний перелік усіх унікальних інгредієнтів через об'єднання множин (union)."""
    if not data:
        return set()
    return set().union(*(dish["ingredients"] for dish in data))


def find_dishes_without_allergens(data: List[Dict[str, Any]], allergens: Set[str]) -> List[Dict[str, Any]]:
    """
    Повертає страви без небажаних алергенів.
    Використовує перетин множин (&).
    """
    return [dish for dish in data if not (dish["ingredients"] & allergens)]


# 4. Обчислення статистик (map, reduce, min/max)

def calculate_average_price(data: List[Dict[str, Any]]) -> float:
    """Обчислює середню ціну позицій меню за допомогою map()."""
    if not data:
        return 0.0
    prices = list(map(lambda d: d["price"], data))
    return round(sum(prices) / len(prices), 2)


def calculate_total_menu_value(data: List[Dict[str, Any]]) -> float:
    """Обчислює вартість усього меню за допомогою reduce()."""
    if not data:
        return 0.0
    return round(reduce(lambda acc, d: acc + d["price"], data, 0.0), 2)


def get_price_extremums(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Знаходить найдорожчу та найдешевшу страву меню."""
    if not data:
        return {}
    cheapest = min(data, key=lambda d: d["price"])
    expensive = max(data, key=lambda d: d["price"])
    return {"cheapest": cheapest, "expensive": expensive}


# 5. Групування, сортування та зрізи

def group_dishes_by_category(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Групує страви за категоріями за допомогою defaultdict."""
    grouped = defaultdict(list)
    for dish in data:
        grouped[dish["category"]].append(dish)
    return dict(grouped)


def get_top_expensive_dishes(data: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
    """
    Сортує страви за спаданням ціни та повертає топ-N найдорожчих позицій
    за допомогою sorted() та зрізів списку [:limit].
    """
    sorted_dishes = sorted(data, key=lambda d: d["price"], reverse=True)
    return sorted_dishes[:limit]


# 6. Допоміжні функції інтерфейсу

def format_dish(dish: Dict[str, Any]) -> str:
    """Форматує інформацію про страву для зручного виведення."""
    ingr_str = ", ".join(sorted(dish["ingredients"]))
    return (f