from django.shortcuts import render
from django.http import HttpResponse
import pdfplumber
import re

def extract_from_pdf_title(pdf_stream):
    with pdfplumber.open(pdf_stream) as pdf:

        first_page = pdf.pages[0]
        text = first_page.extract_text()

        match = re.search(r'(\d{4})\s*-\s*(\d)\s*학기', text)
        if match:
            year = match.group(1) 
            semester = match.group(2) 
            return year, semester
        else:
            return None, None

def extract_from_pdf_table(pdf_stream):
    year, semester = extract_from_pdf_title(pdf_stream)
    pdf_stream.seek(0)

    with pdfplumber.open(pdf_stream) as pdf:
        table_data = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    if any(subject_type in row for subject_type in ["교양", "전필", "전선", "소전", "교필", "교선", "전공선택", "전공필수"]):
                        subject_data = {
                            '이수년도': year,
                            '학기': semester,
                            '이수구분': row[0],
                            '주제': row[1] if row[1].strip() else ' ',
                            '교과목명': row[4],
                            '학점': row[7],
                            '등급': row[9],
                        }
                        table_data.append(subject_data)
    return table_data