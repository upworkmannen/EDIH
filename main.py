import re
import pymupdf  # PyMuPDF

RECEIPT_WIDTH = 40


def extract_text_items(pdf_path):
    """Extract text from a PDF file."""
    doc = pymupdf.open(pdf_path)
    text = doc[0]

    tables = text.find_tables()
    table = tables[0].extract()
    for row in table:
        #dit voegt het eurosymbool en de prijscijfers samen
        row[4] += str(row.pop(5))
        row[5] += str(row.pop(6))
        row.pop(3)
        #loopen door de individuele kolommen van items
        for index, column in enumerate(row):
            #fixt de newline door het te vervangen door een spatie
            no_newline = re.sub("\n", " ", column)

            #fixt het feit dat "ti" wordt weergegeven als "\ue0ae"?? geen idee waarom
            ti_fixed = re.sub("\ue0ae", "ti", no_newline)

            row[index] = ti_fixed
    return table

def make_text_neat(text):
    format = f"""
        AANTAL    PRODUCT        OMSCHRIJVING        STUKPRIJS    PRIJS
    =======================================================================
    """


    for item in text:
        beschrijving_items = item[2].split('|')
        print(beschrijving_items)
        format += f""" \n
        {item[0]}, {item[1]}, {item[3]}, {item[4]}\n
        """
        for sub_item in beschrijving_items:
            format += f"""       {sub_item}\n"""

        """======================================================================="""
    print(format)






# Extract text from PDF
path = r"C:\\Users\\j\Downloads\\bon.pdf"
pdf_text = extract_text_items(path)
print(pdf_text)
make_text_neat(pdf_text)


# Export the information to a text file
export_to_txt(metadata, complete_order, r"C:\\Users\\j\\Downloads\\order_receipt.txt")