import os.path

from fillpdf.fillpdfs import write_fillable_pdf
from pdfrw import PdfReader


class PdfFiller:

    def __init__(self) -> None:
        self.errors = []

    def fill(self, in_pdf_path, out_pdf_path, changes, flatten=True) -> None:
        if not os.path.exists(in_pdf_path):
            self.errors.append(f'File {in_pdf_path} does not exist')
            return
        if in_pdf_path.split('.')[-1] != 'pdf':
            self.errors.append(f'File {in_pdf_path} does not have PDF '
                               f'extension')
            return
        if len(PdfReader(in_pdf_path).pages) <= 0:
            self.errors.append("PDF has no pages")
            return

        write_fillable_pdf(in_pdf_path, out_pdf_path, changes, flatten=flatten)
