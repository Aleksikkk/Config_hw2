import unittest
from unittest.mock import patch, mock_open
import os
import zlib
from datetime import datetime

def read_object(sha):
    path = os.path.join('.git', 'objects', sha[:2], sha[2:])
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
    if type != 'commit':
        return None
    lines = content.decode().splitlines()
    commit_info = {}
    commit_info['hash'] = commit_sha
    commit_info['parent'] = None
    for line in lines:
        if line.startswith('parent'):
            hash = line.split()[1]
            commit_info['parent'] = get_commit_info(hash)
        elif line.startswith('author'):
            commit_info['author'] = line.split(' ', 2)[2]
    return commit_info

def get_commit_history(repo_path):
    os.chdir(repo_path)
    branch_path = os.path.join('.git', 'refs', 'tags', '2.0')  # branch
    with open(branch_path, 'r', encoding='utf-8') as f:
        commit_sha = f.read().strip()
        commit_info = get_commit_info(commit_sha)
        return comp(translate(commit_info))

def translate(dictionary):
    if dictionary is None:
        return []
    author = dictionary['author']
    timestamp = dictionary['date']
    ts = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y %z').strftime('%Y-%m-%d %H:%M:%S')
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
    output.append('@enduml')
    return '\n'.join(output)

class TestGitFunctions(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=b'commit 123\nparent abcdef\nauthor John Doe <john@example.com>\ndate Wed Jun 30 21:49:01 2021 +0300\n')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_read_object(self, mock_join, mock_isfile, mock_file):
        type, content = read_object('abc123')
        self.assertEqual(type, 'commit')
        self.assertIn(b'This is a test commit', content)

    def test_parse_git_object(self):
        data = b'commit 123\n\nThis is a test commit'
        size, type, content = parse_git_object(data)
        self.assertEqual(size, '123')
        self.assertEqual(type, 'commit')
        self.assertEqual(content, b'This is a test commit')

    @patch('builtins.open', new_callable=mock_open, read_data=b'commit 123\nparent abcdef\nauthor John Doe <john@example.com>\ndate Wed Jun 30 21:49:01 2021 +0300\n')
    def test_get_commit_info(self, mock_file):
        commit_info = get_commit_info('abc123')
        self.assertEqual(commit_info['hash'], 'abc123')
        self.assertEqual(commit_info['author'], 'John Doe <john@example.com>')
        self.assertEqual(commit_info['date'], 'Wed Jun 30 21:49:01 2021 +0300')

    @patch('os.chdir')
    @patch('builtins.open', new_callable=mock_open, read_data='abc123')
    def test_get_commit_history(self, mock_file, mock_chdir):
        with patch('builtins.open', new_callable=mock_open, read_data=b'commit 123\nparent abcdef\nauthor John Doe <john@example.com>\ndate Wed Jun 30 21:49:01 2021 +0300\n'):
            history = get_commit_history('fake_path')
            self.assertIn('abc123', history)

    def test_translate(self):
        commit_info = {
            'hash': 'abc123',
            'author': 'John Doe <john@example.com>',
            'date': 'Wed Jun 30 21:49:01 2021 +0300',
            'parent': None
        }
        result = translate(commit_info)
        expected_result = [('abc123', 'John Doe <john@example.com>', '2021-06-30 21:49:01')]
        self.assertEqual(result, expected_result)

    def test_comp(self):
        commits = [('abc123', 'John Doe', '2021-06-30 21:49:01')]
        result = comp(commits)
        expected_result = '@startuml\nabc123 : 2021-06-30 21:49:01\nabc123 : John Doe(author)\n@enduml'
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
