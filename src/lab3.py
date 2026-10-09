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
import sys


# 1. Початкова база даних ресторанного меню
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
    """Додає нову страву до меню з унікальним ID."""
    new_id = max([d["id"] for d in data], default=0) + 1
    dish["id"] = new_id
    data.append(dish)
    print(f"\n[+] Страву '{dish['name']}' успішно додано під ID #{new_id}.")


def remove_dish(data: List[Dict[str, Any]], dish_id: int) -> bool:
    """Видаляє страву з меню за ID."""
    for index, dish in enumerate(data):
        if dish["id"] == dish_id:
            removed = data.pop(index)
            print(f"\n[-] Страву '{removed['name']}' (ID #{dish_id}) видалено.")
            return True
    print("\n[!] Помилка: страву з таким ID не знайдено.")
    return False


def update_dish(data: List[Dict[str, Any]], dish_id: int, field: str, value: Any) -> bool:
    """Оновлює інформацію про страву."""
    for dish in data:
        if dish["id"] == dish_id:
            if field in ["price", "weight_g"]:
                try:
                    dish[field] = float(value) if field == "price" else int(value)
                except ValueError:
                    print("\n[!] Помилка: ціна чи вага мають бути числовими значеннями.")
                    return False
            elif field == "ingredients":
                dish[field] = {item.strip().lower() for item in str(value).split(",") if item.strip()}
            elif field in ["name", "category"]:
                dish[field] = str(value).strip()
            else:
                print("\n[!] Невідоме поле.")
                return False
            print(f"\n[+] Поле '{field}' страви #{dish_id} успішно оновлено.")
            return True
    print("\n[!] Страву з таким ID не знайдено.")
    return False


# 3. Пошук, фільтрація та операції з множинами

def find_dishes_by_ingredient(data: List[Dict[str, Any]], ingredient: str) -> List[Dict[str, Any]]:
    """Фільтрація страв за наявністю інгредієнта (filter)."""
    target = ingredient.strip().lower()
    return list(filter(lambda dish: target in dish["ingredients"], data))


def filter_dishes_by_max_price(data: List[Dict[str, Any]], max_price: float) -> List[Dict[str, Any]]:
    """Фільтрація страв за максимальною ціною."""
    return list(filter(lambda dish: dish["price"] <= max_price, data))


def get_all_unique_ingredients(data: List[Dict[str, Any]]) -> Set[str]:
    """Об'єднання множин для отримання всіх унікальних інгредієнтів."""
    if not data:
        return set()
    return set().union(*(dish["ingredients"] for dish in data))


def find_dishes_without_allergens(data: List[Dict[str, Any]], allergens: Set[str]) -> List[Dict[str, Any]]:
    """Пошук страв без алергенів через перетин множин (&)."""
    return [dish for dish in data if not (dish["ingredients"] & allergens)]


# 4. Обчислення статистик (map, reduce, min/max)

def calculate_average_price(data: List[Dict[str, Any]]) -> float:
    """Обчислення середньої ціни за допомогою map()."""
    if not data:
        return 0.0
    prices = list(map(lambda d: d["price"], data))
    return round(sum(prices) / len(prices), 2)


def calculate_total_menu_value(data: List[Dict[str, Any]]) -> float:
    """Обчислення загальної суми меню через reduce()."""
    if not data:
        return 0.0
    return round(reduce(lambda acc, d: acc + d["price"], data, 0.0), 2)


def get_price_extremums(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Знаходження найдешевшої та найдорожчої страви."""
    if not data:
        return {}
    cheapest = min(data, key=lambda d: d["price"])
    expensive = max(data, key=lambda d: d["price"])
    return {"cheapest": cheapest, "expensive": expensive}


# 5. Групування, сортування та зрізи

def group_dishes_by_category(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Групування страв за категоріями за допомогою defaultdict."""
    grouped = defaultdict(list)
    for dish in data:
        grouped[dish["category"]].append(dish)
    return dict(grouped)


def get_top_expensive_dishes(data: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
    """Повертає топ найдорожчих страв через sorted() та зріз списку."""
    sorted_dishes = sorted(data, key=lambda d: d["price"], reverse=True)
    return sorted_dishes[:limit]


# 6. Виведення на екран

def format_dish(dish: Dict[str, Any]) -> str:
    """Форматування страви у зручний рядок."""
    ingr_str = ", ".join(sorted(dish["ingredients"]))
    return (f"#{dish['id']} [{dish['category']}] {dish['name']} | "
            f"Ціна: {dish['price']:.2f} грн | Вага: {dish['weight_g']}г\n"
            f"   Склад: {ingr_str}")


def print_menu_list(dishes: List[Dict[str, Any]]) -> None:
    if not dishes:
        print("-> Список страв порожній.")
        return
    for dish in dishes:
        print(format_dish(dish))


def show_main_menu() -> None:
    print("\n" + "=" * 55)
    print(" СИСТЕМА УПРАВЛІННЯ РЕСТОРАННИМ МЕНЮ (Варіант 12)")
    print("=" * 55)
    print("1. Показати все меню")
    print("2. Додати нову страву")
    print("3. Видалити страву за ID")
    print("4. Оновити інформацію про страву")
    print("5. Знайти страви за інгредієнтом (filter)")
    print("6. Фільтр страв за бюджетом (ціна <= X)")
    print("7. Меню без алергенів (перетин множин &)")
    print("8. Переглянути всі унікальні інгредієнти кухні (set)")
    print("9. Статистика цін (map, reduce, min/max)")
    print("10. Меню згруповане за категоріями (defaultdict)")
    print("11. Топ-3 найдорожчі позиції (зрізи [:3])")
    print("0. Вийти з програми")


# 7. Головна логіка

def run_app() -> None:
    while True:
        show_main_menu()
        choice = input("\nОберіть дію (0-11): ").strip()

        try:
            if choice == "1":
                print("\n--- Поточне ресторанне меню ---")
                print_menu_list(menu_data)

            elif choice == "2":
                print("\n--- Додавання нової страви ---")
                name = input("Назва страви: ").strip()
                category = input("Категорія (Перші страви/Основні страви/Салати/Десерти/Напої): ").strip()
                price = float(input("Ціна (грн): "))
                weight = int(input("Вага порції (грами): "))
                raw_ingr = input("Інгредієнти (через кому): ")

                if price < 0 or weight <= 0:
                    raise ValueError("Ціна не може бути від'ємною, а вага має бути більшою за 0.")

                ingredients_set = {i.strip().lower() for i in raw_ingr.split(",") if i.strip()}
                new_item = {
                    "name": name,
                    "category": category,
                    "price": price,
                    "weight_g": weight,
                    "ingredients": ingredients_set
                }
                add_dish(menu_data, new_item)

            elif choice == "3":
                d_id = int(input("Введіть ID страви для видалення: "))
                remove_dish(menu_data, d_id)

            elif choice == "4":
                d_id = int(input("Введіть ID страви для редагування: "))
                field = input("Яке поле змінити (name, category, price, weight_g, ingredients): ").strip()
                val = input("Введіть нове значення: ").strip()
                update_dish(menu_data, d_id, field, val)

            elif choice == "5":
                ingr = input("Введіть назву інгредієнта для пошуку: ").strip()
                found = find_dishes_by_ingredient(menu_data, ingr)
                print(f"\n--- Страви з інгредієнтом '{ingr}' ---")
                print_menu_list(found)

            elif choice == "6":
                budget = float(input("Введіть максимальну ціну (грн): "))
                affordable = filter_dishes_by_max_price(menu_data, budget)
                print(f"\n--- Страви вартістю до {budget:.2f} грн ---")
                print_menu_list(affordable)

            elif choice == "7":
                raw_allergens = input("Введіть алергени через кому: ")
                allergens = {a.strip().lower() for a in raw_allergens.split(",") if a.strip()}
                safe_dishes = find_dishes_without_allergens(menu_data, allergens)
                print(f"\n--- Безпечні страви (без: {', '.join(allergens)}) ---")
                print_menu_list(safe_dishes)

            elif choice == "8":
                all_ingrs = get_all_unique_ingredients(menu_data)
                print(f"\n--- Всі унікальні інгредієнти кухні ({len(all_ingrs)} шт.) ---")
                for ing in sorted(all_ingrs):
                    print(f" • {ing}")

            elif choice == "9":
                avg_p = calculate_average_price(menu_data)
                total_v = calculate_total_menu_value(menu_data)
                extremums = get_price_extremums(menu_data)
                print("\n--- Цінова аналітика ресторану ---")
                print(f"Середня ціна страви (map):            {avg_p:.2f} грн")
                print(f"Сумарна вартість усього меню (reduce): {total_v:.2f} грн")
                if extremums:
                    print(f"Найдешевша: {extremums['cheapest']['name']} ({extremums['cheapest']['price']:.2f} грн)")
                    print(f"Найдорожча: {extremums['expensive']['name']} ({extremums['expensive']['price']:.2f} грн)")

            elif choice == "10":
                grouped = group_dishes_by_category(menu_data)
                print("\n--- Меню за категоріями ---")
                for cat, items in grouped.items():
                    print(f"\n=== {cat.upper()} ({len(items)}) ===")
                    for item in items:
                        print(f"  • {item['name']} - {item['price']:.2f} грн")

            elif choice == "11":
                top = get_top_expensive_dishes(menu_data, limit=3)
                print("\n--- Топ-3 найдорожчі страви ресторану (зріз [:3]) ---")
                print_menu_list(top)

            elif choice == "0":
                print("\nРоботу завершено.")
                break
            else:
                print("\n[!] Невідомий пункт меню. Оберіть число від 0 до 11.")

        except ValueError as err:
            print(f"\n[!] Помилка введення: {err}. Спробуйте ще раз.")


if __name__ == "__main__":
    try:
        run_app()
    except Exception as e:
        print(f"\nКритична помилка виконання: {e}")
    finally:
        # Цей рядок блокує закриття вікна при подвійному кліку
        input("\nНатисніть Enter для закриття вікна...")