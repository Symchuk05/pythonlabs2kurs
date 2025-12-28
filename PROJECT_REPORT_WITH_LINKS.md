# 📋 Технічний звіт: Реалізований Функціонал (Clean Version)

## 🛠 Налаштування та Середовище
| Task | GitHub Link |
|------|-------------|
| [1] Налаштувати Github-репозиторій | https://github.com/Symchuk05/pythonlabs2kurs |
| [1] requirements.txt / pyproject.toml | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/requirements.txt |
| [1] Віртуальне середовище (venv) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/.gitignore#L4 |
| [1] Збереження даних (Pickle) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L210 |
| [1] Обробка клавіатури | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L178 |

## 🐍 Ігрова Механіка (Сутності)
| Task | GitHub Link |
|------|-------------|
| [4] Вертикальний рух | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/position.py#L47-L56 |
| [4] Горизонтальний рух | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/position.py#L52 |
| [4] Непрохідні стіни | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/game_field.py#L46-L53 |
| [4] Спавн їжі (генерація) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L115 |
| [4] Збільшення змійки (+1) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L72-L79 |
| [4] Бонусне збільшення (+3) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/food.py#L53-L62 |
| [4] Поразка (стіна/хвіст) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L164-L168 |
| [4] Збір предметів (їжа) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L74 |

## 💾 Збереження та Рівні
| Task | GitHub Link |
|------|-------------|
| [4] Збереження сесії (Save) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L199 |
| [4] Завантаження сесії (Load) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L223 |
| [4] Таблиця рекордів | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L261 |
| [3] Завантаження рівнів (txt) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L7 |

## 🎓 Python Lab Tasks (ВСІ ВИМОГИ)

### Lab #1: Базовий синтаксис
| Task | GitHub Link |
|------|-------------|
| 🟦 Вивести поле | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/game_field.py#L66 |
| 🟦 Перемістити гравця | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L72 |
| 🟦 Ігровий цикл | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L137 |
| 🟩 Функції (*args, **kwargs) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L13 |
| 🟦 Зчитати клавішу | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L181 |

### Lab #2: Типи та Логіка
| Task | GitHub Link |
|------|-------------|
| 🟦 Перевірка клітинки | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/game_field.py#L53 |
| 🟦 Власні функції | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L7 |
| 🟩 Типи (str, int, bool) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/position.py#L14 |
| 🟩 If / Elif / Else | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L55 |
| 🟩 And / Or / Not | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L132 |
| 🟩 Ланцюжкові (a < b < c) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L80 |
| 🟩 Цикли (for, while) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L73 |
| 🟩 Break / Continue | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L148 |
| 🟩 Else у циклах | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L61 |
| 🟩 Lambda | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L337 |
| 🟩 Global / Nonlocal | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L17 |

### Lab #3: Структури даних
| Task | GitHub Link |
|------|-------------|
| 🟦 Матриця | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/game_field.py#L38 |
| 🟦 Текстові файли | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L10 |
| 🟩 Бінарні файли (pickle) | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L219 |
| 🟦 Словники | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L185 |
| 🟩 Зрізи | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/game/engine.py#L338 |
| 🟩 List Comprehension | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/game_field.py#L314 |
| 🟩 Кортежі/Множини | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/core/snake.py#L19 |

### Lab #4: Advanced
| Task | GitHub Link |
|------|-------------|
| 🟩 Генератори | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/generators.py#L38 |
| 🟩 Замикання/Декоратори | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/utils/decorators.py#L10 |
| 🟩 Тестування | https://github.com/Symchuk05/pythonlabs2kurs/tree/main/tests |
| 🟦 Винятки | https://github.com/Symchuk05/pythonlabs2kurs/blob/main/snake_game/exceptions.py |
| 🟦 Модулі/Пакети | https://github.com/Symchuk05/pythonlabs2kurs/tree/main/snake_game |
