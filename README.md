# AMONIC-airlines

### Создаем виртуальное окружение
```python -m venv venv```

### Активируем виртуальное окружение
```source ./venv/bin/activate```

### Устанавливаем все зависимости
```pip install -r requirements.txt```

### Делаем миграции
```./venv/bin/python manage.py migrate```

## Fixtures
1. Создать фикстуру: это надо создать в ручную fixtures/role.json
   ```
   python manage.py dumpdata role --indent 2 --output role/fixtures/role.json
   ```
2. Использовать фикстуру:
   ```
   python manage.py loaddata role
   ```
   