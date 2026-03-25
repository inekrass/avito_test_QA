## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/inekrass/avito_test_QA.git
cd avito_test_QA/t-2.2
```

### 2. Создание и активация виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate  # На macOS/Linux
# или
.venv\Scripts\activate  # На Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск тестов

```bash
pytest -v
```