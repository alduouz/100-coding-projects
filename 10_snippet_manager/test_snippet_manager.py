#!/usr/bin/env python3
import unittest
import tempfile
import os
import json
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
import snippet_manager


class TestSnippetManager(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, 'test_snippets.json')
        
        self.sample_snippet = {
            'id': 'test-id-123',
            'description': 'Test function',
            'code': 'def test():\n    return True',
            'tags': ['python', 'test'],
            'created_at': '2023-01-01T12:00:00'
        }
    
    def tearDown(self):
        self.temp_dir.cleanup()


class TestStorageFunctions(TestSnippetManager):
    
    def test_load_snippets_empty_file(self):
        snippets = snippet_manager.load_snippets(self.test_file)
        self.assertEqual(snippets, [])
    
    def test_load_snippets_with_data(self):
        test_data = [self.sample_snippet]
        with open(self.test_file, 'w') as f:
            json.dump(test_data, f)
        
        snippets = snippet_manager.load_snippets(self.test_file)
        self.assertEqual(snippets, test_data)
    
    def test_load_snippets_invalid_json(self):
        with open(self.test_file, 'w') as f:
            f.write('invalid json')
        
        snippets = snippet_manager.load_snippets(self.test_file)
        self.assertEqual(snippets, [])
    
    def test_save_snippets(self):
        test_data = [self.sample_snippet]
        snippet_manager.save_snippets(test_data, self.test_file)
        
        with open(self.test_file, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data, test_data)
    
    def test_atomic_save_on_error(self):
        test_data = [self.sample_snippet]
        
        with patch('builtins.open', side_effect=IOError("Test error")):
            with self.assertRaises(IOError):
                snippet_manager.save_snippets(test_data, self.test_file)
        
        self.assertFalse(os.path.exists(self.test_file + '.tmp'))


class TestAddSnippet(TestSnippetManager):
    
    @patch('builtins.input')
    @patch('uuid.uuid4')
    @patch('datetime.datetime')
    def test_add_snippet_interactive(self, mock_datetime, mock_uuid, mock_input):
        mock_uuid.return_value = MagicMock()
        mock_uuid.return_value.__str__ = lambda x: 'test-uuid'
        mock_datetime.now.return_value.isoformat.return_value = '2023-01-01T12:00:00'
        
        mock_input.side_effect = [
            'Test description',
            'print("hello")',
            EOFError(),
            'python,test'
        ]
        
        result = snippet_manager.add_snippet(self.test_file)
        
        self.assertTrue(result)
        snippets = snippet_manager.load_snippets(self.test_file)
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0]['description'], 'Test description')
        self.assertEqual(snippets[0]['tags'], ['python', 'test'])
    
    def test_add_snippet_with_arguments(self):
        with patch('uuid.uuid4') as mock_uuid, patch('datetime.datetime') as mock_datetime:
            mock_uuid.return_value.__str__ = lambda x: 'test-uuid'
            mock_datetime.now.return_value.isoformat.return_value = '2023-01-01T12:00:00'
            
            result = snippet_manager.add_snippet(
                self.test_file,
                description='Test snippet',
                code='print("test")',
                tags='python,cli'
            )
        
        self.assertTrue(result)
        snippets = snippet_manager.load_snippets(self.test_file)
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0]['description'], 'Test snippet')
        self.assertEqual(snippets[0]['code'], 'print("test")')
        self.assertEqual(snippets[0]['tags'], ['python', 'cli'])
    
    @patch('builtins.input', return_value='')
    def test_add_snippet_empty_description(self, mock_input):
        with patch('builtins.print') as mock_print:
            result = snippet_manager.add_snippet(self.test_file)
        
        self.assertFalse(result)
        mock_print.assert_called_with("Error: Description is required")
    
    @patch('builtins.input')
    def test_add_snippet_empty_code(self, mock_input):
        mock_input.side_effect = ['Valid description', EOFError()]
        
        with patch('builtins.print') as mock_print:
            result = snippet_manager.add_snippet(self.test_file)
        
        self.assertFalse(result)


class TestListSnippets(TestSnippetManager):
    
    def test_list_snippets_empty(self):
        with patch('builtins.print') as mock_print:
            snippet_manager.list_snippets(self.test_file)
        
        mock_print.assert_called_with("No snippets found.")
    
    def test_list_snippets_with_data(self):
        snippet_manager.save_snippets([self.sample_snippet], self.test_file)
        
        with patch('builtins.print') as mock_print:
            snippet_manager.list_snippets(self.test_file)
        
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn('ID: test-id-123', calls)
        self.assertIn('Description: Test function', calls)
        self.assertIn('Tags: python, test', calls)


class TestSearchSnippets(TestSnippetManager):
    
    def setUp(self):
        super().setUp()
        self.snippets = [
            {
                'id': '1',
                'description': 'Python function',
                'code': 'def hello():\n    print("world")',
                'tags': ['python', 'function'],
                'created_at': '2023-01-01T12:00:00'
            },
            {
                'id': '2',
                'description': 'JavaScript alert',
                'code': 'alert("Hello");',
                'tags': ['javascript', 'browser'],
                'created_at': '2023-01-02T12:00:00'
            }
        ]
        snippet_manager.save_snippets(self.snippets, self.test_file)
    
    def test_search_by_description(self):
        with patch('builtins.print') as mock_print:
            snippet_manager.search_snippets(self.test_file, 'Python')
        
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn('Found 1 snippet(s) matching \'Python\':', calls)
        self.assertIn('ID: 1', calls)
    
    def test_search_by_code(self):
        with patch('builtins.print') as mock_print:
            snippet_manager.search_snippets(self.test_file, 'alert')
        
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn('Found 1 snippet(s) matching \'alert\':', calls)
        self.assertIn('ID: 2', calls)
    
    def test_search_by_tags(self):
        with patch('builtins.print') as mock_print:
            snippet_manager.search_snippets(self.test_file, 'javascript')
        
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn('Found 1 snippet(s) matching \'javascript\':', calls)
        self.assertIn('ID: 2', calls)
    
    def test_search_case_insensitive(self):
        with patch('builtins.print') as mock_print:
            snippet_manager.search_snippets(self.test_file, 'PYTHON')
        
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn('Found 1 snippet(s) matching \'PYTHON\':', calls)
    
    def test_search_no_results(self):
        with patch('builtins.print') as mock_print:
            snippet_manager.search_snippets(self.test_file, 'nonexistent')
        
        mock_print.assert_called_with("No snippets found matching 'nonexistent'")


class TestExportSnippets(TestSnippetManager):
    
    def setUp(self):
        super().setUp()
        snippet_manager.save_snippets([self.sample_snippet], self.test_file)
    
    def test_export_markdown(self):
        output_file = os.path.join(self.temp_dir.name, 'test_export.md')
        
        with patch('builtins.print') as mock_print:
            snippet_manager.export_snippets(self.test_file, 'md', output_file)
        
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            content = f.read()
        
        self.assertIn('# Code Snippets', content)
        self.assertIn('## Test function', content)
        self.assertIn('```', content)
        self.assertIn('def test():', content)
        mock_print.assert_called_with(f"Snippets exported to {output_file}")
    
    def test_export_text(self):
        output_file = os.path.join(self.temp_dir.name, 'test_export.txt')
        
        with patch('builtins.print') as mock_print:
            snippet_manager.export_snippets(self.test_file, 'txt', output_file)
        
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            content = f.read()
        
        self.assertIn('CODE SNIPPETS', content)
        self.assertIn('Description: Test function', content)
        self.assertIn('def test():', content)
        mock_print.assert_called_with(f"Snippets exported to {output_file}")
    
    def test_export_empty_snippets(self):
        empty_file = os.path.join(self.temp_dir.name, 'empty.json')
        
        with patch('builtins.print') as mock_print:
            snippet_manager.export_snippets(empty_file, 'md')
        
        mock_print.assert_called_with("No snippets to export.")
    
    def test_export_default_filename(self):
        with patch('builtins.print'):
            snippet_manager.export_snippets(self.test_file, 'md')
        
        self.assertTrue(os.path.exists('snippets_export.md'))
        os.remove('snippets_export.md')


class TestCLIIntegration(TestSnippetManager):
    
    def test_cli_add_non_interactive(self):
        test_args = [
            'snippet_manager.py', 'add',
            '--file', self.test_file,
            '--description', 'CLI test',
            '--code', 'print("cli")',
            '--tags', 'cli,test'
        ]
        
        with patch('sys.argv', test_args), patch('uuid.uuid4') as mock_uuid, patch('datetime.datetime') as mock_datetime:
            mock_uuid.return_value.__str__ = lambda x: 'cli-test-uuid'
            mock_datetime.now.return_value.isoformat.return_value = '2023-01-01T12:00:00'
            
            with patch('builtins.print'):
                snippet_manager.main()
        
        snippets = snippet_manager.load_snippets(self.test_file)
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0]['description'], 'CLI test')
        self.assertEqual(snippets[0]['code'], 'print("cli")')
        self.assertEqual(snippets[0]['tags'], ['cli', 'test'])
    
    def test_cli_list(self):
        snippet_manager.save_snippets([self.sample_snippet], self.test_file)
        
        test_args = ['snippet_manager.py', 'list', '--file', self.test_file]
        
        with patch('sys.argv', test_args), patch('builtins.print') as mock_print:
            snippet_manager.main()
        
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn('ID: test-id-123', calls)
    
    def test_cli_search(self):
        snippet_manager.save_snippets([self.sample_snippet], self.test_file)
        
        test_args = ['snippet_manager.py', 'search', '--file', self.test_file, 'Test']
        
        with patch('sys.argv', test_args), patch('builtins.print') as mock_print:
            snippet_manager.main()
        
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn('Found 1 snippet(s) matching \'Test\':', calls)
    
    def test_cli_export(self):
        snippet_manager.save_snippets([self.sample_snippet], self.test_file)
        output_file = os.path.join(self.temp_dir.name, 'cli_export.md')
        
        test_args = [
            'snippet_manager.py', 'export',
            '--file', self.test_file,
            '--format', 'md',
            '--output', output_file
        ]
        
        with patch('sys.argv', test_args), patch('builtins.print'):
            snippet_manager.main()
        
        self.assertTrue(os.path.exists(output_file))
    
    def test_cli_no_command(self):
        test_args = ['snippet_manager.py']
        
        with patch('sys.argv', test_args), patch('argparse.ArgumentParser.print_help') as mock_help:
            snippet_manager.main()
        
        mock_help.assert_called_once()


if __name__ == '__main__':
    unittest.main()