login# Django Barter Platform – Тестовое задание

- [Текст тестового задания](./task.pdf)

> Это мини-платформа для обмена вещами между пользователями. Каждый может создать объявление, просматривать чужие, предлагать обмен и управлять своими предложениями.



https://github.com/user-attachments/assets/06d4bf17-97fe-4a81-a26e-16acd482a12d



## 🔧 Стек технологий

- Python 3.13
- Django 5.2
- SQLite
- HTML (Django Templates)
- matcha.css

---

## 🚀 Как запустить проект локально

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Reagent992/test_assignment_barter_platform
cd test_assignment_barter_platform
```
### 2. Создать и активировать виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```
### 3. Установить зависимости
```bash
pip install -r requirements.txt
# или(опционально)
uv sync
```
### 4. Аккаунт суперпользователя
```
login: rea
password: rea
```
### 5. Запустить сервер разработки
```bash
python manage.py runserver
```

# 📄 Примечания
- До сюда все равно никто не дочитает🤣
- У меня нету времени на тесты и DRF

Как я пишу тесты и DRF есть в моих других репо:
- [Пример django unittest](https://github.com/Reagent992/stamps/blob/master/src/mainapp/tests/test_views.py)
- [Пример pytest, правда это не Django](https://github.com/Reagent992/async_rutube_downloader/blob/main/tests/test_downloader.py)
- [Пример DRF](https://github.com/Lozhkin-pa/hackathon-crm-ambassadors/blob/main/api/v1/views/ambassadors_view.py)
