import os
import unittest
import uuid
from pathlib import Path

from pdfrw import PdfReader

from tests.utils import get_resource_absolute_path
from pdf_filler import PdfFiller

current_path = Path(os.path.dirname(os.path.realpath(__file__)))

ANNOT_KEY = '/Annots'  # key for all annotations within a page
ANNOT_FIELD_KEY = '/T'  # Name of field. i.e. given ID of field
ANNOT_FORM_type = '/FT'  # Form type (e.g. text/button)
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
ANNOT_FIELD_PARENT_KEY = '/Parent'  # Parent key for older pdf versions


class TestPdfFiller(unittest.TestCase):
    maxDiff = None

    def test_fill(self):
        in_pdf_path = get_resource_absolute_path(current_path, 'fillable.pdf')
        out_pdf_path = f'/tmp/filled_{uuid.uuid1()}.pdf'
        changes = {
            'NameKey': 'MyName',
            'SurnameKey': 'MySurname',
            'AgeKey': 27
        }
        pdf_filler = PdfFiller()
        pdf_filler.fill(in_pdf_path, out_pdf_path, changes)
        self.assertEqual(len(pdf_filler.errors), 0)
        self.assertTrue(os.path.exists(out_pdf_path))
        self.assert_filled_values(changes, out_pdf_path)

    def test_fill_double(self):
        in_pdf_path = get_resource_absolute_path(current_path,
                                                 'double_same_name_form.pdf')
        out_pdf_path = f'/tmp/filled_{uuid.uuid1()}.pdf'
        changes = {
            'NameKey': 'MyName',
            'SurnameKey': 'MySurname',
            'AgeKey': 27
        }
        pdf_filler = PdfFiller()
        pdf_filler.fill(in_pdf_path, out_pdf_path, changes)
        self.assertEqual(len(pdf_filler.errors), 0)
        self.assertTrue(os.path.exists(out_pdf_path))
        self.assert_filled_values(changes, out_pdf_path)

    def test_fill_twice_double(self):
        in_pdf_path = get_resource_absolute_path(
            current_path, 'twice_double_same_name_form.pdf')
        out_pdf_path = f'/tmp/filled_{uuid.uuid1()}.pdf'
        changes = {
            'NameKey': 'MyName',
            'SurnameKey': 'MySurname',
            'AgeKey': 27
        }
        pdf_filler = PdfFiller()
        pdf_filler.fill(in_pdf_path, out_pdf_path, changes)

        self.assertEqual(len(pdf_filler.errors), 0)
        self.assertTrue(os.path.exists(out_pdf_path))
        self.assert_filled_values(changes, out_pdf_path)

    def assert_filled_values(self, changes, out_pdf_path):
        out_pdf = PdfReader(out_pdf_path)
        for Page in out_pdf.pages:
            if Page[ANNOT_KEY]:
                for annotation in Page[ANNOT_KEY]:
                    target = annotation if annotation[ANNOT_FIELD_KEY] else \
                        annotation[ANNOT_FIELD_PARENT_KEY]
                    if annotation[ANNOT_FORM_type] is None:
                        pass
                    if target and \
                            annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                        # Remove parentheses
                        key = target[ANNOT_FIELD_KEY][1:-1]
                        target_aux = target
                        while target_aux['/Parent']:
                            key = target['/Parent'][ANNOT_FIELD_KEY][
                                  1:-1] + '.' + key
                            target_aux = target_aux['/Parent']
                        print(f'Asserting KEY {key}')
                        form_value = annotation['/V'][1:-1]
                        expected_form_value = changes[annotation['/T'][1:-1]]
                        self.assertEqual(form_value, str(expected_form_value))
