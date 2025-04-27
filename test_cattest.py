import requests
import unittest
from unittest.mock import patch, Mock
from cattest import CatFactProcessor, APIError


class TestCatFactProcessor(unittest.TestCase):
    @patch('cattest.requests.get')
    def test_get_fact_success(self, mock_get):
        mock_response = Mock()
        expected_fact = "Cats are amazing!"
        mock_response.json.return_value = {"fact": expected_fact}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        processor = CatFactProcessor()
        fact = processor.get_fact()

        self.assertEqual(fact, expected_fact)
        self.assertEqual(processor.last_fact, expected_fact)

    @patch('cattest.requests.get')
    def test_get_fact_api_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        processor = CatFactProcessor()

        with self.assertRaises(APIError) as context:
            processor.get_fact()

        self.assertIn("Ошибка при запросе к API", str(context.exception))

    def test_get_fact_analysis_with_fact(self):
        processor = CatFactProcessor()
        processor.last_fact = "Cat"

        analysis = processor.get_fact_analysis()

        expected = {
            "length": 3,
            "letter_frequencies": {
                'c': 1,
                'a': 1,
                't': 1,
            }
        }

        self.assertEqual(analysis, expected)

    def test_get_fact_analysis_without_fact(self):
        processor = CatFactProcessor()

        analysis = processor.get_fact_analysis()

        expected = {
            "length": 0,
            "letter_frequencies": {}
        }

        self.assertEqual(analysis, expected)


if __name__ == '__main__':
    unittest.main()