# Сервер для "Словарик-Смешарик"
Простой сервер на Flask, восстанавливающий функционал игры "Словарик-Смешарик" (2005).
Серверы игры закрылись много лет назад и она больше не функционирует, так как все необходимые слова хранились именно на серверах.

## Реализовано
* [x] Проверка слов
* [x] Лидерборд

## Установка
Рекомендуется проводить установку на системах на базе Linux (или используя WSL)
1. Клонируйте репозиторий:
```
git clone https://github.com/Nediorg/SlovSmesh.git
```
2. Создайте venv и активируйте:
```
python3 -m venv .venv
. .venv/bin/activate
```
3. (Необязательно) Поменяйте IP или порт в [\_\_main__.py](./slovsmesh/__main__.py)
4. Запустите сервер:
```
python3 -m slovsmesh
```

## License
This project is licensed under the MIT License. See the LICENSE file for more information.