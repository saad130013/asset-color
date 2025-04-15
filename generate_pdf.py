
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

data = [
    {"code": "13", "en": "Information Technology Assets", "ar": "أصول تقنية المعلومات"},
    {"code": "02", "en": "Office IT and Communication Equipment", "ar": "تكنولوجيا المعلومات ومعدات الاتصالات المكتبية"},
    {"code": "04", "en": "Laptops & Computers", "ar": "أجهزة الكمبيوتر المحمولة وأجهزة الكمبيوتر المكتبية"},
    {"code": "01", "en": "PPE", "ar": "الآلات والمعدات والعقارات"},
    {"code": "13020401", "en": "", "ar": ""}
]

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, "Asset Classification Report", 0, 1, "C")
        self.ln(5)

    def table(self, data):
        self.set_fill_color(220, 220, 220)
        self.set_font("DejaVu", "B", 12)
        self.cell(40, 10, "Code", 1, 0, "C", fill=True)
        self.cell(80, 10, "English", 1, 0, "C", fill=True)
        self.cell(70, 10, "Arabic", 1, 1, "C", fill=True)

        self.set_font("DejaVu", "", 12)
        for row in data:
            reshaped_text = arabic_reshaper.reshape(row["ar"])
            bidi_text = get_display(reshaped_text)
            self.cell(40, 10, row["code"], 1)
            self.cell(80, 10, row["en"], 1)
            self.cell(70, 10, bidi_text, 1, 1)

pdf = PDF()
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)
pdf.add_page()
pdf.table(data)
pdf.output("asset_classification_report.pdf")
