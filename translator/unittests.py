from translator.tasks import translate
import unittest


class TestTasks(unittest.TestCase):
    def testTranslate(self):
        response = translate("Gatunek bardzo zmienny morfologicznie. Organizm jednokomórkowy, o kształcie niesymetrycznym, silnie spłaszczony grzbietobrzusznie, ale z wyraźnymi kolcami (rogami). Komórki o długości od 40 do 450 μm i szerokości 30-75 μm")
        self.assertEqual(
            response,
            {
                'translation_type': 'auto',
                'original_text': 'Gatunek bardzo zmienny morfologicznie. Organizm jednokomórkowy, o kształcie niesymetrycznym, silnie spłaszczony grzbietobrzusznie, ale z wyraźnymi kolcami (rogami). Komórki o długości od 40 do 450 μm i szerokości 30-75 μm',
                'translated_text': 'A species that is very morphologically variable. A single-celled organism, with a non-symmetrical shape, strongly flattened dorsal, but with clear collars (horns). Cells with a length of 40 to 450 μm and a width of 30-75 μm',
                'language': 'Polish'})


if __name__ == '__main__':
    unittest.main()
