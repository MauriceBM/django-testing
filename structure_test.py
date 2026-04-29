import os
import sys


def check_structure():
    """Проверка структуры проекта."""
    errors = []
    success = []

    ya_news_path = os.path.join("ya_news", "news")
    ya_note_path = os.path.join("ya_note", "notes")

    required_items = [
        "requirements.txt",
        ".gitignore",
        "ya_news",
        "ya_news/manage.py",
        "ya_news/pytest.ini",
        "ya_news/yanews",
        "ya_news/templates",
        ya_news_path,
        os.path.join(ya_news_path, "pytest_tests"),
        os.path.join(
            ya_news_path, "pytest_tests", "test_routes.py"
        ),
        os.path.join(
            ya_news_path, "pytest_tests", "test_content.py"
        ),
        os.path.join(
            ya_news_path, "pytest_tests", "test_logic.py"
        ),
        os.path.join(
            ya_news_path, "pytest_tests", "conftest.py"
        ),
        os.path.join(ya_news_path, "__init__.py"),
        os.path.join(ya_news_path, "models.py"),
        os.path.join(ya_news_path, "views.py"),
        os.path.join(ya_news_path, "urls.py"),
        "ya_note",
        "ya_note/manage.py",
        "ya_note/pytest.ini",
        "ya_note/yanote",
        "ya_note/templates",
        ya_note_path,
        os.path.join(ya_note_path, "tests"),
        os.path.join(
            ya_note_path, "tests", "test_routes.py"
        ),
        os.path.join(
            ya_note_path, "tests", "test_content.py"
        ),
        os.path.join(
            ya_note_path, "tests", "test_logic.py"
        ),
        os.path.join(ya_note_path, "__init__.py"),
        os.path.join(ya_note_path, "models.py"),
        os.path.join(ya_note_path, "views.py"),
        os.path.join(ya_note_path, "urls.py"),
    ]

    for item in required_items:
        if os.path.exists(item):
            success.append(f"[OK] {item}")
        else:
            errors.append(f"[ОШИБКА] Отсутствует: {item}")

    if errors:
        print("Проверка завершена с ошибками:")
        for err in errors:
            print(err)
        print("Исправьте отсутствующие элементы.")
        return False

    print("Структура проекта соответствует требованиям!")
    print("Обнаруженные файлы и папки:")
    for item in success:
        print(item)
    return True


if __name__ == "__main__":
    if check_structure():
        sys.exit(0)
    else:
        sys.exit(1)
