import pdfplumber
import sys

pdf_path = "/home/pedro/Projetos/EconomicsWorkspace/companies/nvidia/inputs/sec-filings/10-q/2025-q3_form-10-q_oct26.pdf"

def extract_cash_flow_table():
    with pdfplumber.open(pdf_path) as pdf:
        # According to TOC, Cash Flows is on page 8 (0-indexed 7)
        page_index = 7
        page = pdf.pages[page_index]
        text = page.extract_text()
        print(f"--- Page {page_index + 1} ---")
        print(text)

        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"\nTable {j+1}:")
            for row in table:
                cleaned_row = [str(cell).replace('\n', ' ') for cell in row if cell is not None]
                if cleaned_row:
                    print(cleaned_row)

if __name__ == "__main__":
    extract_cash_flow_table()
