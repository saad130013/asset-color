
from fpdf import FPDF
from datetime import datetime

# وصف الأصل التجريبي
asset_name = "Laptop Device 💻"

# بيانات التصنيف
data = [
    {"code": "13", "en": "Information Technology Assets", "icon": "💻"},
    {"code": "02", "en": "Office IT and Communication Equipment", "icon": "🖥️"},
    {"code": "04", "en": "Laptops & Computers", "icon": "🧳"},
    {"code": "01", "en": "PPE", "icon": "🛠️"},
    {"code": "13020401", "en": "Asset Code For Accounting Purpose", "icon": "📄"}
]

class PDF(FPDF):
    def header(self):
        self.set_fill_color(240, 240, 240)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "📄 Asset Classification Report", 0, 1, "C", fill=True)
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"📝 Asset: {asset_name}", 0, 1, "L")
        self.cell(0, 10, f"🕒 Date: {datetime.today().strftime('%Y-%m-%d')}", 0, 1, "L")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Generated electronically - Not an official copy", 0, 0, "C")

    def table(self, data):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 200, 200)
        self.cell(30, 10, "Code", 1, 0, "C", fill=True)
        self.cell(140, 10, "Classification (with Icon)", 1, 1, "C", fill=True)

        self.set_font("Arial", "", 12)
        fill = False
        for row in data:
            self.set_fill_color(245, 245, 245) if fill else self.set_fill_color(255, 255, 255)
            self.cell(30, 10, row["code"], 1, 0, "C", fill=True)
            self.cell(140, 10, f'{row["icon"]} {row["en"]}', 1, 1, "L", fill=True)
            fill = not fill

pdf = PDF()
pdf.add_page()
pdf.table(data)
pdf.output("styled_asset_report.pdf")
