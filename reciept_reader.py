import pandas as pd
from PyPDF2 import PdfReader

file_path = r'C:\Users\Alex Feng\Documents\Bitches_Finance\2023\04\receipts\eReceipt_1638_Green Square Town Centre_18Apr2023__hccxd.pdf'
reader = PdfReader(file_path)
page = reader.pages[0]
receipt_text = page.extract_text()
items_string = receipt_text.splitlines()[2]
item_list = [items_string[i:i+56] for i in range(0, len(items_string), 56)]
print(item_list)