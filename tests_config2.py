import os
import zlib
from datetime import datetime
from config2 import *

def test_read_object():
    sha = 'abc123'
    path = os.path.join('.git', 'objects', 'ab', 'c123')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    data = zlib.compress(b'commit 123\0content here')
    with open(path, 'wb') as f:
        f.write(data)

    obj_type, content = read_object(sha)
    assert obj_type == 'commit'
    assert b'content here' in content

def test_parse_git_object():
    data = zlib.compress(b'commit 123\0Hello World!')
    size, obj_type, content = parse_git_object(zlib.decompress(data))
    
    assert size == '123'
    assert obj_type == 'commit'
    assert content == b'Hello World!'

def test_get_commit_info():
    sha = 'abc123'
    path = os.path.join('.git', 'objects', 'ab', 'c123')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    data = zlib.compress(b'commit 123\0parent def456\nauthor unknown <John> 1731431007 +0300\n')
    with open(path, 'wb') as f:
        f.write(data)

    commit_info = get_commit_info(sha)
    assert commit_info is not None
    assert commit_info['hash'] == sha
    assert commit_info['author'] == '<John> 1731431007 +0300'

def test_get_commit_history():
    # Создаем тестовый репозиторий с ссылкой на коммит
    repo_path = '.'  # Замените на ваш тестовый путь
    os.makedirs(os.path.join(repo_path, '.git', 'refs', 'tags'), exist_ok=True)
    
    # Создаем тестовый коммит
    sha = 'abc123'
    branch_path = os.path.join(repo_path, '.git', 'refs', 'tags', '2.0')
    with open(branch_path, 'w') as f:
        f.write(sha)

    # Создаем объект для тестирования
    path = os.path.join(repo_path, '.git', 'objects', 'ab', 'c123')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    data = zlib.compress(b'commit 123\0parent def456\nauthor John Doe 1610000000 +0300\n')
    with open(path, 'wb') as f:
        f.write(data)

    os.chdir(repo_path)
    history = get_commit_history(repo_path)
    assert '@startuml' in history
    assert '@enduml' in history

def test_translate():
    example_dict = {'hash': 'abc123', 'author': 'John 1610000000 +0300', 'parent': None}
    result = translate(example_dict)
    
    assert len(result) == 1
    assert result[0][0] == 'abc123'

def test_comp():
    test_commits = [('abc123', 'John Doe', '2021-01-01 00:00:00')]
    result = comp(test_commits)
    
    assert '@startuml' in result, "Start of UML not found in output"
    assert '@enduml' in result, "End of UML not found in output"


# Основная функция для запуска тестов
if __name__ == "__main__":
    test_read_object()
    test_parse_git_object()
    test_get_commit_info()
    test_get_commit_history()
    test_translate()
    test_comp()
    print("Все тесты прошли успешно!")
