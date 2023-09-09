import streamlit as st
import requests

# Заголовок приложения
st.title('Автоматический подбор параметров самодиффузии по результатам ЯМР')

# Вводимый пользователем файл
uploaded_file = st.file_uploader("Загрузите файл с данными эксперимента", type=[])

if uploaded_file is not None:
    st.write('Файл успешно загружен. Нажмите "Анализировать" для начала обработки.')
    
    # При нажатии кнопки "Анализировать" отправляем файл на сервер для обработки
    if st.button('Анализировать'):

        # Отправка файла на сервер FastAPI для обучения модели
        response = requests.post("http://host.docker.internal:8000/train/", files={"file": uploaded_file})
        
        try:
            response_data = response.json()
        except ValueError:
            response_data = response.text

        if ("fitted_A" and "fitted_B") in response_data:
            st.write("Подобранные населенности: ", response_data["fitted_A"]) 
            st.write("Подобранные коэффициента самодиффузии: ",response_data["fitted_B"])
        else:
            st.write("Не удалось подобрать оптимальные параметры")
        
        # Получение и отображение истории потерь (если она есть в ответе)
        if "loss_history" in response.json():
            loss_history = response.json()["loss_history"]
            st.write("График обучения модели (функция ошибки):")
            st.line_chart(loss_history)
        else:
            st.write("Loss history not found in the server response.")
