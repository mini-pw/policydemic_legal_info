import unittest
from tasks import *

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

if __name__ == 'main':
   unittest.main()
