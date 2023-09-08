import streamlit as st
import requests

# Добавить заголовок
st.title('Bootcamp hackaton')

# Заголовок приложения
st.title('Автоматический подбор параметров самодиффузии по результатам ЯМР')

# Адрес сервера для обработки видео
url = 'http://host.docker.internal:8000/application'

# Вводимый пользователем файл
uploaded_file = st.file_uploader("Загрузите файл с данными эксперимента в формате csv", type=['csv', 'xls', 'xlsx'])

if uploaded_file is not None:
    st.write('Файл успешно загружен. Нажмите "Анализировать" для начала обработки.')
    
    # При нажатии кнопки "Анализировать" отправляем видео на сервер для обработки
    if st.button('Анализировать'):
        files = {'video': ('video.mp4', uploaded_file.read(), 'application/octet-stream')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            st.write('Анализ завершен. Результаты:')
            results = response.json()

            summary = results['summary']

        else:
            st.write('Произошла ошибка при обработке файла.')
            st.write(response.text)
