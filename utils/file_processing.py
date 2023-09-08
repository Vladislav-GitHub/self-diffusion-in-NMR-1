import pandas as pd

def create_DataFrame(file_path: str):
    """
    Создание DataFrame из текстового файла, выведенного в определенном формате
    """
    with open(file_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        file_text = []
        for line in lines:
            list_of_str = list_split(line)
            for l in list_of_str:
                file_text.append(l)
        idx = find_index(file_text)
        table = create_table(file_text, idx)
        data = pd.DataFrame(table[1:], columns=table[0])
        data.head()
        return data

def create_table(file_text: list, index: int) -> list:
    """
    Создание таблицы в виде списка
    """
    table = []
    for text in file_text[:-1]:
        if file_text.index(text) >= index:
            table.append(text.split())
    return table

def find_index(file_text: list) -> int:
    """
    Поиск индекса строки с ключевым словом "Point"
    """
    for text in file_text:
        if 'Point' in text.split():
            idx = file_text.index(text)
            return idx

def list_split(line):
    """
    Разделение и фильтрация пробелов строки
    """
    list_of_str = line.split("\n")
    list_of_str = list(filter(None, map(str.strip, list_of_str)))
    return list_of_str

def read_file(file_path: str):
    """
    Считывание 1 таблицы
    """
    if file_path.endswith(".csv"):
        data1 = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        data1 = pd.read_excel(file_path)
    else:
        data1 = create_DataFrame(file_path)
    return data1