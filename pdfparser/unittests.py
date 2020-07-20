import unittest
from pdfparser.tasks import *


class TestTasks(unittest.TestCase):
   def test_simple_crit(self):
      # Simple crit

      ## If the word exist
      self.assertEqual(
         simple_crit(
            'a b c',
            {'a'},
            without=set(),
            at_least=1,
            at_most=1
         ),
         True
      )

      # If it doesn't exist
      self.assertEqual(
         simple_crit(
            'a b c',
            {'d'},
            without=set(),
            at_least=1,
            at_most=1
         ),
         False
      )

      # There isn't any word from the without set
      self.assertEqual(
         simple_crit(
            'a b c',
            {'a'},
            without={'d'},
            at_least=1,
            at_most=1
         ),
         True
      )

      # There is a word from without set
      self.assertEqual(
         simple_crit(
            'a b c',
            {'a'},
            without={'b'},
            at_least=1,
            at_most=1
         ),
         False
      )

      ## There are 3 words, at_least=3
      self.assertEqual(
         simple_crit(
            'a b c d e',
            {'a', 'c', 'e'},
            without=set(),
            at_least=3,
            at_most=1
         ),
         True
      )

      ## There is not enough words, at_least=3
      self.assertEqual(
         simple_crit(
            'a b c d e',
            {'a', 'c', 'z'},
            without=set(),
            at_least=3,
            at_most=1
         ),
         False
      )

   def test_complex_crit(self):
      # Simple crit

      ## If the word exist
      self.assertEqual(
         complex_crit(
            'a b c',
            {'a'},
            without=set(),
            at_least=1,
            at_most=1,
            similarity="embedding_cosine",
            threshold=0.9
         ),
         True
      )

      # If it doesn't exist
      self.assertEqual(
         complex_crit(
            'a b c',
            {'d'},
            without=set(),
            at_least=1,
            at_most=1,
            similarity="embedding_cosine",
            threshold=0.9
         ),
         False
      )

      # There isn't any word from the without set
      self.assertEqual(
         complex_crit(
            'a b c',
            {'a'},
            without={'d'},
            at_least=1,
            at_most=1,
            similarity="embedding_cosine",
            threshold=0.9
         ),
         True
      )

      # There is a word from without set
      self.assertEqual(
         complex_crit(
            'a b c',
            {'a'},
            without={'b'},
            at_least=1,
            at_most=1,
            similarity="embedding_cosine",
            threshold=0.9
         ),
         False
      )

      ## There are 3 words, at_least=3
      self.assertEqual(
         complex_crit(
            'a b c d e',
            {'a', 'c', 'e'},
            without=set(),
            at_least=3,
            at_most=1,
            similarity="embedding_cosine",
            threshold=0.9
         ),
         True
      )

      ## There is not enough words, at_least=3
      self.assertEqual(
         complex_crit(
            'a b c d e',
            {'a', 'c', 'z'},
            without=set(),
            at_least=3,
            at_most=1,
            similarity="embedding_cosine",
            threshold=0.9
         ),
         False
      )

   def complex_crit_hamming(self):

      ## If the word exist
      self.assertEqual(
         complex_crit(
            'asdf bsdf csdf',
            {'asdf'},
            without=set(),
            at_least=1,
            at_most=1,
            similarity="hamming",
            threshold=3
         ),
         True
      )

      # If it doesn't exist
      self.assertEqual(
         complex_crit(
            'asdf bsdf csdf',
            {'gggg'},
            without=set(),
            at_least=1,
            at_most=1,
            similarity="hamming",
            threshold=3
         ),
         False
      )

      # There isn't any word from the without set
      self.assertEqual(
         complex_crit(
            'asdf bsdf csdf',
            {'asdf'},
            without={'dddd'},
            at_least=1,
            at_most=1,
            similarity="hamming",
            threshold=3
         ),
         True
      )

      # There is a word from without set
      self.assertEqual(
         complex_crit(
            'asdf bsdf csdf',
            {'asdf'},
            without={'dsdf'},
            at_least=1,
            at_most=1,
            similarity="hamming",
            threshold=3
         ),
         False
      )

      ## There are 3 words, at_least=3
      self.assertEqual(
         complex_crit(
            'asdf bsdf csdf dsdf esdf',
            {'asdf', 'csdf', 'esdf'},
            without=set(),
            at_least=3,
            at_most=1,
            similarity="hamming",
            threshold=3
         ),
         True
      )

      ## There is not enough words, at_least=3
      self.assertEqual(
         complex_crit(
            'asdf bsdf csdf dsdf esdf',
            {'asdf', 'csdf', 'gggg'},
            without=set(),
            at_least=3,
            at_most=1,
            similarity="hamming",
            threshold=3
         ),
         False
      )

   def test_parser_small_file(self):
      parsed_text = parse("pdfparser/small.pdf")
      expected_text="Here is a small document\n!"\
      "Testing how\n!"\
      "PDF Parser will work"
      self.assertEqual(parsed_text,expected_text)

   def test_parser_longer_file(self):
      parsed_text = parse("pdfparser/longer.pdf")
      expected_text="Here is a another document\n!"\
      "Bigger this time!"\
      "Testing how\n!"\
      "PDF Parser will work on a bigger one!"\
      "This document contains an image!"\
      "And then\" " \
      "There is another page\n"\
      "!That should also be parsed!"

      self.assertEqual(parsed_text,expected_text)

   def test_pdfocr_small_file(self):
      recognized_text = pdfocr("small.pdf")
      expected_text = ["Here is a small document\n" \
                      "Testing how\n" \
                      "PDF Parser will work"]

      self.assertEqual(recognized_text, expected_text)

   def test_pdfocr_easy_page_ocrtest_file(self):
      recognized_text = pdfocr("ocrtest.pdf", pages=[1])
      expected_text = ["This is another sample document.\n"\
                        "The first page is quality.\n"\
                        "\nSample random text."]

      self.assertEqual(recognized_text,expected_text)

   def test_pdfocr_hard_pages_ocrtest_file(self):
      recognized_text = pdfocr("ocrtest.pdf", pages=[2,3])
      expected_text = ["The second page contains a photo of the text.\n\n"\
                        "This is text in paint.\n"\
                        "Only ocr can read this."\
                        ,"The last page contains\n"\
                        "only text in paint."]
      self.assertEqual(recognized_text, expected_text)

if __name__ == '__main__':
   unittest.main()
