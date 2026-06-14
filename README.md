# 💬 Student Messenger Project

<div align="center">
  <img src="https://img.shields.io/badge/python-3.10-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/deployed-PythonAnywhere-1E415E?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" />
</div>

<br>

<div align="center">
[![🌐 ЖИВОЙ ПРОЕКТ](https://img.shields.io/badge/🌐_ЖИВОЙ_ПРОЕКТ-открыть-1E415E?style=for-the-badge)](https://studentppk2026.pythonanywhere.com)
  [![📂 GITHUB](https://img.shields.io/badge/📂_GITHUB-репозиторий-181717?style=for-the-badge&logo=github)](https://github.com/sv2001eta-svg/student_PPK)
</div>

<br>

## 📖 О проекте

**Student Messenger** — это веб-приложение для обмена сообщениями, разработанное на Python с использованием фреймворка **Flask** и базы данных **MySQL**. Проект реализует полный цикл взаимодействия пользователя: от регистрации до личного чата.

### ✨ Ключевые возможности:
- 📝 **Регистрация и Авторизация:** Система учетных записей с хранением данных в БД (Flask-Login).
- 💬 **Личный чат:** Возможность переписки между зарегистрированными пользователями.
- 👥 **Список пользователей:** Интерфейс для выбора собеседника с аватарками.
- 🕐 **История сообщений:** Сохранение переписки в базе данных.
- 🔄 **Real-time обновление:** Автоматическая проверка новых сообщений каждые 2 секунды.
- 🟢 **Статусы онлайн/офлайн:** Отображение последней активности пользователей.
- 🎨 **Дизайн:** Адаптивный и современный интерфейс с градиентами.

---

### 🔗 Ссылки:
- **🌐 Живой проект:** https://studentppk2026.pythonanywhere.com
- **📂 GitHub репозиторий:** https://github.com/sv2001eta-svg/student_PPK
>
> **🚀 Проект развёрнут на PythonAnywhere и доступен 24/7!**

---

### 🔐 Тестовые аккаунты для проверки:

| Логин | Пароль | Описание |
|-------|--------|----------|
| `teacher` | `test123` | Первый пользователь |
| `student` | `123456` | Второй пользователь |
| `test3` | `123` | Третий пользователь |
| `testuser99` | `123` | Четвёртый пользователь |
| `demo` | `123` | Пятый пользователь |

> 💡 **Совет:** Откройте сайт в **двух разных браузерах** (или в режиме инкогнито `Ctrl+Shift+N`), войдите под разными аккаунтами и отправляйте сообщения друг другу!

---

## 🛠️ Технологический стек

| Технология | Назначение |
| :--- | :--- |
| **Python 3.10** | Основной язык программирования |
| **Flask** | Веб-фреймворк (Backend) |
| **Flask-Login** | Управление сессиями пользователей |
| **SQLite** | Система управления базами данных |
| **Werkzeug** | Хеширование паролей |
| **HTML5/CSS3** | Верстка и стилизация (Frontend) |
| **JavaScript** | Интерактивность и AJAX-запросы |
| **PythonAnywhere** | Хостинг и деплой |

---

## 👥 Команда

| Участник | Роль | Задачи |
|----------|------|--------|
| **sv2001eta-svg** | Full-stack | Frontend, Backend, интеграция, деплой |
| **budniks246-cloud** | Backend & DB | База данных, API, маршруты |

---

## 📁 Структура проекта
```
student_PPK/
│
── 📄 app.py # Основной файл приложения (Flask)
├── 🗄️ database.db # База данных SQLite
├── 📋 requirements.txt # Зависимости Python
├── 📘 README.md # Документация проекта
├── 📝 BACKLOG.md # Product Backlog
├── .gitignore # Исключения для Git
│
├── 📁 templates/ # HTML-шаблоны
│ ├── Registration.html # Страница регистрации
│ ├── 📄 avtorization.html # Страница входа
│ ├── 📄 users.html # Список пользователей
│ ├── 📄 chat.html # Страница чата
│ ├── 📄 index.html # Главная страница
│ ├── 📄 help.html # Страница помощи
│ └── 📄 teacher_check.html # Страница для преподавателя
│
└── 📁 static/ # Статические файлы
├── css/
│ └── style.css # Стили приложения
├── js/
│ └── script.js # JavaScript код
└── 📁 avatars/ # Папка для аватарок пользователей
```

---

## 🚀 Как запустить проект

### 📋 Требования:
- Python 3.8 или выше
- MySQL Server
- Git
- VS Code (рекомендуется)

---

### 🔧 Шаг 1: Установка Python

Если Python не установлен:
1. Скачай с [python.org](https://www.python.org/downloads/)
2. При установке **обязательно** поставь галочку ✅ "Add Python to PATH"

---

### 💻 Шаг 2: Подготовка (Терминал)

> **Важно:** Все команды ниже нужно вводить в **Терминал** (Command Line), а не в редактор кода.

**1. Откройте терминал:**
*   **Вне VS Code:** Нажмите `Win + R`, введите `cmd` и нажмите Enter.
*   **Внутри VS Code:** В верхнем меню выберите **Terminal** → **New Terminal** (или нажмите `` Ctrl + ` ``).

**2. Склонируйте репозиторий (если вы еще этого не сделали):**
```bash
git clone https://github.com/sv2001eta-svg/student_PPK.git
cd student_PPK
```

**3. Установите зависимости:**
```bash
pip install -r requirements.txt
```

**4. Запустите приложение:**
```bash
python app.py
```

**5. Откройте браузер и перейдите:**

**Онлайн версия (рекомендуется):**

https://studentppk2026.pythonanywhere.com

**Или локально:**

http://127.0.0.1:5000

(только если запустили `python app.py`)

**6. Остановить сервер: нажмите Ctrl+C в терминале**

---

## 🌍 Деплой на PythonAnywhere

### 📍 Основная информация:
- **Платформа:** [PythonAnywhere](https://www.pythonanywhere.com/)
- **URL проекта:** https://studentppk2026.pythonanywhere.com
- **База данных:** SQLite (локальный файл `database.db`)
- **WSGI конфигурация:** Настроен для Flask
- **Тариф:** Бесплатный

### ⚙️ Технические особенности:
- 🔄 **Миграция БД:** С MySQL на SQLite  
  (для совместимости с бесплатным тарифом)
- 📁 **Структура папок:**
  - `/mysite/templates/` — HTML-шаблоны
  - `/mysite/static/` — статические файлы
- 🔧 **Авто-инициализация:** База данных создаётся автоматически при первом запуске
- 🔐 **Безопасность:** Хеширование паролей через Werkzeug

---

*Учебный проект. Дисциплина "Современные способы программирования". Магистратура 2026*
