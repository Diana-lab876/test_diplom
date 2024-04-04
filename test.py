import py_compile
import os

def test_syntax_of_another_file():
    file_path = '2.py'  # Путь к вашему файлу с кодом

    # Проверяем, существует ли файл
    assert os.path.exists(file_path), f"Файл {file_path} не найден"

    try:
        # Читаем содержимое файла с явным указанием кодировки UTF-8
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Пытаемся скомпилировать код
        py_compile.compile(file_path, cfile=None, doraise=True)
    except py_compile.PyCompileError as e:
        # Если возникает ошибка компиляции, значит есть синтаксическая ошибка
        assert False, f"Синтаксическая ошибка в файле {file_path}: {e}"
