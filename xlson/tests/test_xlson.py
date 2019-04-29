import os
import unittest
import json

from xlson.constants import TESTS_PATH, xlson_logger
from xlson.handlers import XLSonHandler
from xlson import xl_preparation


PACKAGE_TEST_DATA_DIR = "xlson"
INPUT_DIR = os.path.join(TESTS_PATH, 'test_data', PACKAGE_TEST_DATA_DIR)
OUTPUT_DIR = os.path.join(TESTS_PATH, 'test_results', PACKAGE_TEST_DATA_DIR)

try:
    os.makedirs(OUTPUT_DIR)
except OSError:
    pass


class TestXlPreparation(unittest.TestCase):


     xl_fix_bill_path = os.path.join(INPUT_DIR, 'xl_fict_bill.xlsx')
     prep_fix_bill_path = os.path.join(INPUT_DIR, "prep_fict_bill.json")
     new_prep_fix_bill_path = os.path.join(OUTPUT_DIR, "new_prep_fict_bill.json")

     def test_prepare_new_xl(self, save_prep_res=False):
         prep_bill = xl_preparation.prepare_xl(self.xl_fix_bill_path, data_only=True)
         if save_prep_res:
             prep_bill.dump(self.new_prep_fix_bill_path)
             xlson_logger.info("New json saved to %s" % self.new_prep_fix_bill_path)
             return
         ch_prep_bill = XLSonHandler.load(self.prep_fix_bill_path)
         # This code is for normalization of paths
         ch_prep_bill["main_sheet"]["source_path"] = prep_bill["main_sheet"]["source_path"]
         ch_prep_bill["supp_sheets"][0]["source_path"] = prep_bill["supp_sheets"][0]["source_path"]
         ch_prep_bill["supp_sheets"][1]["source_path"] = prep_bill["supp_sheets"][1]["source_path"]

         self.assertEqual(prep_bill, ch_prep_bill)


if __name__ == "main":
    unittest.main()
