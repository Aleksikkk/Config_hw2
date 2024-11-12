import subprocess
import os
import re
import datetime

def generate_graph(repo_path, tag, output_path, plantuml_path):


  # Получаем список коммитов для указанного тега
  commits = subprocess.check_output(
    ['git', '-C', repo_path, 'log', '--pretty=format:"%ad %an %H"', tag],
    universal_newlines=True
  ).splitlines()

  # Преобразуем список коммитов в формат PlantUML
  plantuml_code = "@startuml\n"
  for commit in commits:
    date, author, commit_hash = commit.split(' ', 2)
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
    plantuml_code += f"({commit_hash}) as {author}\n"
    plantuml_code += f"{commit_hash} : {date} - {author}\n"
  plantuml_code += "@enduml\n"

  # Записываем код PlantUML в файл
  with open(os.path.join(repo_path, 'graph.puml'), 'w') as f:
    f.write(plantuml_code)

  # Выполняем визуализацию графа PlantUML
  subprocess.run([plantuml_path, '-tpng', '-o', output_path, os.path.join(repo_path, 'graph.puml')])
  os.remove(os.path.join(repo_path, 'graph.puml'))

# Считываем конфигурационные данные из файла ini
config_path = 'config2.ini'
with open(config_path, 'r') as f:
  config = {}
  for line in f:
    key, value = line.strip().split('=', 1)
    config[key] = value.strip('"')

# Получаем данные из конфигурационного файла
repo_path = config
'''
import subprocess

def git_cat_file(object_type, object_name):
  """
  Выполняет команду git cat-file -p для указанного объекта.

  Args:
      object_type: Тип объекта (например, "commit", "tree", "blob").
      object_name: Имя объекта (например, "HEAD", "master", "1234567890abcdef").

  Returns:
      Строка с содержимым объекта, если объект найден.
      None, если объект не найден.
  """

  try:
    process = subprocess.run(
        ["git", "cat-file", "-p", f"{object_type}:{object_name}"],
        stdout=subprocess.PIPE,
        check=True,
        text=True,
    )
    return process.stdout
  except subprocess.CalledProcessError:
    return None

# Пример использования
object_type = "commit"
object_name = "HEAD"

content = git_cat_file(object_type, object_name)

if content is not None:
  print(f"Содержимое объекта {object_type}:{object_name}:\n{content}")
else:
  print(f"Объект {object_type}:{object_name} не найден.")
'''