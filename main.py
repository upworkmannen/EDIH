import re
import pymupdf

RECEIPT_WIDTH = 40

ESC = b'\x1B'
FS = b'\x1C'
GS = b'\x1D'
RESET = ESC + b'@'
ALIGN_LEFT = ESC + b'a\x00'
ALIGN_CENTER = ESC + b'a\x01'
ALIGN_RIGHT = ESC + b'a\x02'
BOLD_ON = ESC + b'E\x01'
BOLD_OFF = ESC + b'E\x00'
DOUBLE_WIDTH_ON = ESC + b'!\x30'
DOUBLE_WIDTH_OFF = ESC + b'!\x00'
UNDERLINE_ON = ESC + b'-\x01'
UNDERLINE_OFF = ESC + b'-\x00'
CHARSET_GB18030 = FS + b'\x26'
CUT_PAPER = GS + b'V\x00'

def extract_info(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = doc[0]
    content = text.get_text()
    content = re.sub("\n", ' ', content)
    content = re.split('AANTAL', content)[0]
    content = re.split(r'\s{2,}', content)
    content[0] = re.split('\s(?=[A-Z])', content[0])
    content[0][1] += ' ' + content[0].pop(2)
    content.insert(0, content[0][1])
    content.insert(0, content[1][0])
    content.pop(2)
    content.pop(9)
    return content

def extract_text_items(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = doc[0]
    tables = text.find_tables()
    table = tables[0].extract()
    for row in table:
        row[4] += str(row.pop(5))
        row[5] += str(row.pop(6))
        for index, column in enumerate(row):
            no_newline = re.sub("\n", " ", column)
            ti_fixed = re.sub("\ue0ae", "ti", no_newline)
            row[index] = ti_fixed
    return table

def encode_text(text):
    return text.encode("gb18030")

def generate_escpos_receipt(text, klantinfo):
    receipt_data = bytearray()
    receipt_data += RESET + CHARSET_GB18030
    receipt_data += ALIGN_CENTER + BOLD_ON + DOUBLE_WIDTH_ON
    receipt_data += encode_text("Bedankt voor de bestelling\n")
    receipt_data += DOUBLE_WIDTH_OFF + BOLD_OFF
    receipt_data += ALIGN_LEFT
    for info in klantinfo:
        receipt_data += encode_text(info + "\n")
    receipt_data += encode_text("\nAANTAL   PRODUCT   OMSCHRIJVING   STUKPRIJS   PRIJS\n")
    receipt_data += encode_text("=" * RECEIPT_WIDTH + "\n")
    for item in text:
        beschrijving_items = item[2].split('|')
        receipt_data += encode_text(f"{item[0]}, {item[1]}, {item[4]}, {item[5]}\n")
        for sub_item in beschrijving_items:
            if re.findall("\Apoke", item[1].lower()):
                ingredient_list = re.split(r'\s(?=[A-Z])', item[3])
                for poke_ingredient in ingredient_list:
                    receipt_data += encode_text(f"   {poke_ingredient}\n")
            else:
                receipt_data += encode_text(f"   {sub_item}\n")
        receipt_data += encode_text("=" * RECEIPT_WIDTH + "\n")
    receipt_data += CUT_PAPER
    return receipt_data

path = r"/home/joep/EDIH/EDIH/bon.pdf"
pdf_text = extract_text_items(path)
klantinfo = extract_info(path)
escpos_receipt = generate_escpos_receipt(pdf_text, klantinfo)

with open("receipt_escpos.bin", "wb") as file:
    file.write(escpos_receipt)
