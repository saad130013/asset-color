
from fpdf import FPDF
from deep_translator import GoogleTranslator

# إدخال اسم الأصل بالعربية
original_name = "طابعة كروت"

# ترجمة الاسم للإنجليزية
translated_name = GoogleTranslator(source='auto', target='en').translate(original_name)

# مثال على التصنيفات المحاسبية
data = [
    {"code": "13", "en": "Information Technology Assets"},
    {"code": "02", "en": "Office IT and Communication Equipment"},
    {"code": "07", "en": "Scanners & Printers"},
    {"code": "01", "en": "PPE"},
    {"code": "13020401", "en": ""}
]

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Asset Classification Report", 0, 1, "C")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Original Search: {original_name} - Translated: {translated_name}", 0, 1, "C")
        self.ln(5)

    def table(self, data):
        self.set_fill_color(220, 220, 220)
        self.set_font("Arial", "B", 12)
        self.cell(40, 10, "Code", 1, 0, "C", fill=True)
        self.cell(140, 10, "English Description", 1, 1, "C", fill=True)

        self.set_font("Arial", "", 12)
        for row in data:
            self.cell(40, 10, row["code"], 1)
            self.cell(140, 10, row["en"], 1, 1)

pdf = PDF()
pdf.add_page()
pdf.table(data)
pdf.output("asset_classification_translated.pdf")
