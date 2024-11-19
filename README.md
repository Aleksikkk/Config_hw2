# Документация по проекту

## 1. Общее описание
Данный проект представляет собой набор функций на Python, предназначенных для работы с Git-объектами. Программа позволяет извлекать информацию о коммитах из Git-репозитория, а также формировать историю коммитов в удобном для анализа формате. Проект использует стандартные библиотеки Python, такие как `os`, `zlib` и `datetime`, что делает его легким в использовании и интеграции.

## 2. Описание функций

### Функции:
- **read_object(sha)**: Читает объект из Git-репозитория по указанному SHA. Возвращает тип и содержимое объекта.
- **parse_git_object(data)**: Парсит данные Git-объекта, извлекая размер, тип и содержимое.
- **get_commit_info(commit_sha)**: Извлекает информацию о коммите, включая автора и родительский коммит, по указанному SHA.
- **get_commit_history(repo_path)**: Получает историю коммитов для указанного репозитория и формирует её в удобном формате.
- **translate(dictionary)**: Преобразует информацию о коммите в список кортежей с хэшом, автором и временной меткой.
- **comp(commits)**: Формирует строку в формате PlantUML для визуализации истории коммитов.

### Переменные и настройки
- **repo_path**: Путь к Git-репозиторию, из которого извлекается информация о коммитах.
- **branch_path**: Путь к файлу, содержащему SHA текущей ветки (например, `.git/refs/tags/2.0`).

## 3. Описание команд для сборки проекта
Для работы с проектом вам потребуется Python, установленный на вашей системе.

### Установка зависимостей
Не требуется установка дополнительных библиотек, так как используются стандартные библиотеки Python.

### Запуск приложения
1. Убедитесь, что у вас есть доступ к Git-репозиторию с необходимыми объектами.
2. Сохраните код в файл, например, `git_history.py`.
3. Откройте терминал или командную строку и выполните команду:
   ```bash
   python git_history.py
   ```
   Замените `git_history.py` на имя вашего файла с кодом.

## 4. Примеры использования
### Примеры вызовов функций
- **Получение информации о коммите**:
  ```python
  commit_info = get_commit_info('abc123')
  ```

- **Получение истории коммитов**:
  ```python
  history = get_commit_history('/path/to/repo')
  ```

- **Преобразование информации о коммитах в формат PlantUML**:
  ```python
  commits = translate(commit_info)
  diagram = comp(commits)
  ```

## 5. Результаты прогона тестов
Тесты функциональности:

- **Тест read_object**: Функция корректно извлекает объект Git по SHA.
- **Тест parse_git_object**: Корректный парсинг данных Git-объекта.
- **Тест get_commit_info**: Успешное извлечение информации о коммите, включая автора и родительский коммит.
- **Тест get_commit_history**: Корректное получение истории коммитов из репозитория.
- **Тест translate**: Успешное преобразование информации о коммите в нужный формат.
- **Тест comp**: Корректное формирование выходных данных для визуализации.

### Проверка на ошибки
Все функции были протестированы на наличие возможных ошибок, и приложение корректно обрабатывало их. В случае отсутствия объекта по указанному SHA функция `read_object` возвращает `None`, что позволяет избежать сбоев в работе программы.
