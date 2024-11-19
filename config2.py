import os
import zlib
from datetime import datetime

def read_object(sha):
    path = os.path.join('.git', 'objects', sha[:2], sha[2:])
    print(path)
    if not os.path.isfile(path):
        return None, None
    with open(path, 'rb') as f:
        data = f.read()
    data = zlib.decompress(data)
    size, type, content = parse_git_object(data)
    return type, content

def parse_git_object(data):
    header_end = data.index(b'\0')
    header = data[:header_end].decode()
    type, size = header.split(' ')
    content = data[header_end + 1:]
    return size, type, content

def get_commit_info(commit_sha):
    type, content = read_object(commit_sha)
    print(type)
    if type != 'commit':
        return None
    lines = content.decode().splitlines()
    commit_info = {}
    commit_info['hash'] = commit_sha
    commit_info['parent'] = None
    for line in lines:
        if line.startswith('parent'):
            hash = line.split()[1]
            commit_info['parent']= get_commit_info(hash)
        elif line.startswith('author'):
            commit_info['author'] = line.split(' ', 2)[2]
    return commit_info

def get_commit_history(repo_path):
    os.chdir(repo_path)
    branch_path = os.path.join('.git', 'refs', 'tags', '2.0') # branch
    with open(branch_path, 'r', encoding = 'utf-8') as f:
        commit_sha = f.read().strip()
        commit_info = get_commit_info(commit_sha)
        print(commit_info)
        return comp(translate(commit_info))

def translate(dictionary):
  if dictionary is None:
    return []
  author, timestamp, _ = dictionary['author'].split()
  ts = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
  return [(dictionary['hash'], author, ts)] + translate(dictionary['parent'])


def comp(commits):
  output = ['@startuml']
  for hash, author, date in commits:
    output.append(f'{hash} : {date}')
    output.append(f'{hash} : {author}(author)')
  window_size = 2
  for i in range(len(commits) - window_size + 1):
    a, b = (commits[i: i + window_size])
    output.append(f'{a[0]} <|-- {b[0]}')
  output.append(f'@enduml')
  return '\n'.join(output)
    

if __name__ == "__main__":
    print(get_commit_history('C:\\Users\\user\\Desktop\\demo'))
