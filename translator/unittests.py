from translator.tasks import translate
import unittest


class TestTasks(unittest.TestCase):
    def testTranslate(self):
        response = translate("testowy tekst")
        self.assertEqual(
            response,
            {
                'translation_type': 'auto',
                'original_text': 'testowy tekst',
                'translated_text': 'test text',
                'language': 'Polish'})


if __name__ == '__main__':
    unittest.main()
