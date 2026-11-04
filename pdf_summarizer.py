from pypdf import PdfReader


def read_pdf(path):

    try:

        reader = PdfReader(path)

        text = ""


        for page in reader.pages:

            text += page.extract_text() + "\n"


        return text



    except Exception as e:

        print("PDF Error:", e)

        return None



def summarize_pdf(path):

    text = read_pdf(path)


    if not text:

        return "I cannot read this PDF."


    # Basic summary (first version)

    words = text.split()

    summary = " ".join(
        words[:150]
    )


    return summary