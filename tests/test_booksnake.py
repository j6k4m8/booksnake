#!/usr/bin/env python3

import unittest
from booksnake import Booksnake, _truncate, _pad, print_results

class TestBooksnake(unittest.TestCase):

    def test_search(self):
        b = Booksnake()
        self.assertIsInstance(
            b.search("Moby Dick"),
            list
        )

    def test_print_table(self):
        b = Booksnake()
        print_results(b.search("Moby Dick"))

    def test_truncate(self):
        self.assertEqual(_truncate('Test', 10), 'Test')
        self.assertEqual(_truncate('One Two Three', 13), 'One Two Three')
        self.assertEqual(_truncate('One Two Three', 10), 'One Two T…')

    def test_pad(self):
        self.assertEqual(
            _pad('Tests', 5),
            'Tests'
        )
        self.assertEqual(
            _pad('Test', 10),
            'Test      '
        )
        self.assertEqual(
            _pad('One Two Three', 10),
            'One Two T…'
        )
        self.assertEqual(
            _pad('One Two Three', 20),
            'One Two Three       '
        )
