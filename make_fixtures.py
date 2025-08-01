# make_fixtures.py
import os
import django
from django.core import management

# Инициализация Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  # Укажите правильное имя вашего settings модуля
django.setup()

def create_fixtures_products():
    try:
        # Указываем полный путь к файлу, чтобы избежать проблем с директориями
        with open('fixtures/goods/products.json', 'w', encoding='utf-8') as f:
            management.call_command('dumpdata', 'goods.Products', stdout=f)
        print("Фикстуры Products успешно созданы")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def create_fixtures_categories():
    try:
        # Указываем полный путь к файлу, чтобы избежать проблем с директориями
        with open('fixtures/goods/categories.json', 'w', encoding='utf-8') as f:
            management.call_command('dumpdata', 'goods.Categories', stdout=f)
        print("Фикстуры Categories успешно созданы")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def create_fixtures_subcategories():
    try:
        # Указываем полный путь к файлу, чтобы избежать проблем с директориями
        with open('fixtures/goods/subcategories.json', 'w', encoding='utf-8') as f:
            management.call_command('dumpdata', 'goods.SubCategories', stdout=f)
        print("Фикстуры SubCategories успешно созданы")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def create_fixtures_productrelationship():
    try:
        # Указываем полный путь к файлу, чтобы избежать проблем с директориями
        with open('fixtures/goods/productrelationship.json', 'w', encoding='utf-8') as f:
            management.call_command('dumpdata', 'goods.ProductRelationship', stdout=f)
        print("Фикстуры ProductRelationship успешно созданы")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    create_fixtures_products()
    create_fixtures_categories()
    create_fixtures_subcategories()
    create_fixtures_productrelationship()
