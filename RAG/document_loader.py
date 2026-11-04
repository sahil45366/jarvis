import os
import pytesseract

from pdf2image import convert_from_path


PDF_FOLDER = "knowledge/pdf"


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def load_pdfs():

    documents = []


    for root, dirs, files in os.walk(PDF_FOLDER):

        for file in files:

            if file.endswith(".pdf"):

                path = os.path.join(root,file)

                print("OCR Loading:", path)


                pages = convert_from_path(path)

                text = ""


                for page in pages:

                    text += pytesseract.image_to_string(
                        page
                    )


                documents.append({
                    "file":file,
                    "text":text
                })


    print("Total PDFs:",len(documents))

    return documents