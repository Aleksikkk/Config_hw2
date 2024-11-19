import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import zlib
from datetime import datetime
from config2 import *

class TestGitFunctions(unittest.TestCase):

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data=b'commit 123\nparent abcdef\nauthor Alice <alice@example.com> 1622505600\n\nThis is a commit message.')
    @patch('zlib.decompress')
    def test_read_object(self, mock_decompress, mock_open, mock_isfile):
        mock_isfile.return_value = True
        mock_decompress.return_value = b'commit 123\nparent abcdef\nauthor Alice <alice@example.com> 1622505600\n\nThis is a commit message.'
        
        type, content = read_object('abcdef1234567890')
        self.assertEqual(type, 'commit')
        self.assertIn(b'parent abcdef', content)

    def test_parse_git_object(self):
        data = b'commit 123\nparent abcdef\nauthor Alice <alice@example.com> 1622505600\n\nThis is a commit message.'
        size, type, content = parse_git_object(data)
        self.assertEqual(size, '123')
        self.assertEqual(type, 'commit')
        self.assertIn(b'parent abcdef', content)

    @patch('read_object')
    def test_get_commit_info(self, mock_read_object):
        mock_read_object.return_value = ('commit', b'parent abcdef\nauthor Alice <alice@example.com> 1622505600\n\nThis is a commit message.')
        
        commit_info = get_commit_info('abcdef1234567890')
        self.assertEqual(commit_info['hash'], 'abcdef1234567890')
        self.assertEqual(commit_info['parent'], None)
        self.assertEqual(commit_info['author'], 'Alice <alice@example.com>')

    @patch('os.chdir')
    @patch('builtins.open', new_callable=mock_open, read_data='abcdef1234567890')
    @patch('get_commit_info')
    def test_get_commit_history(self, mock_get_commit_info, mock_open, mock_chdir):
        mock_get_commit_info.return_value = {'hash': 'abcdef1234567890', 'author': 'Alice <alice@example.com>', 'parent': None}
        
        commit_history = get_commit_history('C:\\Users\\user\\Desktop\\demo')
        self.assertIn('abcdef1234567890', commit_history)

    def test_translate(self):
        commit_info = {
            'hash': 'abcdef1234567890',
            'author': 'Alice <alice@example.com> 1622505600',
            'parent': None
        }
        result = translate(commit_info)
        self.assertEqual(result, [('abcdef1234567890', 'Alice', '2021-05-31 00:00:00')])

    def test_comp(self):
        commits = [('abcdef1234567890', 'Alice', '2021-05-31 00:00:00'), ('1234567890abcdef', 'Bob', '2021-06-01 00:00:00')]
        result = comp(commits)
        self.assertIn('@startuml', result)
        self.assertIn('abcdef1234567890 : 2021-05-31 00:00:00', result)
        self.assertIn('abcdef1234567890 <|-- 1234567890abcdef', result)
        self.assertIn('@enduml', result)

if __name__ == "__main__":
    unittest.main()
