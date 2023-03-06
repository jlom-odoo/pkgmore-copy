from odoo.tests import common, tagged
import unittest

@tagged('please', 'standard', 'package')
class PleaseWork(unittest.TestCase):

    def test_1(self):
        self.assertEqual(0,1)