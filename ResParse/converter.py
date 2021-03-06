"""

A utility to convert the given resume into text file.

"""
import re
import logging

import configurations as regex

from subprocess import Popen, PIPE
from docx import opendocx, getdocumenttext

# for converting pdfs to text
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

logging.basicConfig(level=logging.DEBUG)

"""

Utility Function to convert pdfs to plain txt format.
Derived from the examples provided by the pdfminer package documentation.
Params: file_name type: string
returns string

"""
def pdf_to_txt(file_name):
  try:
    file_pointer = open(file_name,'rb')

    # Setting up pdf reader
    pdf_resource_manager = PDFResourceManager()
    return_string = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(pdf_resource_manager, return_string, codec=codec, \
      laparams=laparams)
    interpreter = PDFPageInterpreter(pdf_resource_manager, device)

    for page in PDFPage.get_pages(file_pointer, set(), maxpages=0, password="",
      caching=True, check_extractable=True):
      interpreter.process_page(page)
    file_pointer.close()
    device.close()

    # Get full string from PDF
    txt = return_string.getvalue()
    return_string.close()

    # logging.debug(pdf_txt)

    # Formatting removing and replacing special characters
    txt = txt.replace("\r", "\n")
    txt = re.sub(regex.bullet, " ", txt)

    return txt.decode('ascii', errors='ignore')

  except Exception as exception_instance:
    logging.error('Error converting pdf to txt: '+str(exception_instance))
    return ''

def document_to_text(file_name, file_path):
    if filename[-4:] == ".doc":
        cmd = ['antiword', file_path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')
    elif filename[-5:] == ".docx":
        document = opendocx(file_path)
        paratextlist = getdocumenttext(document)
        newparatextlist = []
        for paratext in paratextlist:
            newparatextlist.append(paratext.encode("utf-8"))
        return '\n\n'.join(newparatextlist)
    elif filename[-4:] == ".pdf":
        return pdf_to_txt(file_path)