import pandas as pd

# Создаем примеры ошибок и их исправлений
data = {
    'error': [
        'print("Hello, World!"',
        'print("Hello, World!)',
        'print"Hello, World!")',
        'prin("Hello, World")'
    ],

    'correction': [
        "Попробуйте добавить закрывающую скобку",
        "Попробуйте добавить закрывающие кавычки",
        "Попробуйте добавить открывающую скобку",
        "Посмотрите как правильно пишется название функции"
    ]
}

# Создаем DataFrame из данных
df = pd.DataFrame(data)

# Сохраняем DataFrame в CSV-файл
df.to_csv('error_correction_dataset.csv', index=False)