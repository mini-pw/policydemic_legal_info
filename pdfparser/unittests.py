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
            threshold=0.9
         ),
         False
      )

   def test_parser_metadata(self):
      metadata, _, _, _ = parse("pdfparser/rozp.pdf")
      self.assertEqual(metadata["title"],
                       "Ustawa z dnia 31 marca 2020 r. o zmianie niektórych ustaw w zakresie systemu "\
                       "ochrony zdrowia związanych z zapobieganiem, przeciwdziałaniem i zwalczaniem COVID-19")
      self.assertEqual(metadata["author"], "RCL")
      self.assertEqual(metadata["creator"],"Microsoft® Word 2010")
      self.assertEqual(metadata["producer"],"Microsoft® Word 2010; modified using iText 2.1.7 by 1T3XT")


   def test_parser_separated_text(self):
      _, separated_text, _, _ = parse("pdfparser/3_pages.pdf")
      self.assertEqual(separated_text, [['PDF with 3 pages\u2028\nText on the ﬁrst one\u2029\n'], [],
                                        ['Text on the 3rd one\n']])


   def test_parser_empty_pages(self):
      _, _, empty_pages, _ = parse("pdfparser/3_pages.pdf")
      self.assertEqual(empty_pages, [1])


   def test_parser_all_text(self):
      _, _, _, all_text = parse("pdfparser/small.pdf")
      self.assertEqual(all_text, "Here is a small document\n\nTesting how\n\nPDF Parser will work\n")

   # def test_pdfocr_small_file(self):
   #
   #    recognized_text = pdfocr("pdfparser/small.pdf")
   #    expected_text = "Here is a small document\n" \
   #                    "Testing how\n" \
   #                    "PDF Parser will work"
   #    print(recognized_text)
   #    print(expected_text)
   #    self.assertEqual(recognized_text, expected_text)
   #
   # def test_pdfocr_longer_file(self):
   #    recognized_text = pdfocr("pdfparser/longer.pdf")
   #    expected_text="Here is a another document\n!"\
   #    "Bigger this time!"\
   #    "Testing how\n!"\
   #    "PDF Parser will work on a bigger one!"\
   #    "This document contains an image!"\
   #    "And then\" " \
   #    "There is another page\n"\
   #    "!That should also be parsed!"
   #
   #    self.assertEqual(recognized_text,expected_text)

if __name__ == '__main__':
   unittest.main()
