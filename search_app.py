
import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

st.set_page_config(page_title="Asset Classifier", layout="centered")
st.title("🔍 Asset Classification Report Generator")

@st.cache_data
def load_data():
    df = pd.read_excel("assetv4.xlsx", header=1)
    df = df[df.columns.dropna()]
    df = df.dropna(subset=["Asset Description"])
    return df

df = load_data()
descriptions = df["Asset Description"].astype(str).tolist()

user_input = st.text_input("Enter part of the asset description (e.g., printer, device):")

if user_input:
    matches = [desc for desc in descriptions if user_input.lower() in desc.lower()]
    selected_desc = st.selectbox("Matching Descriptions:", matches)

    if selected_desc:
        selected_row = df[df["Asset Description"] == selected_desc].iloc[0]

        st.markdown("### Selected Description:")
        st.markdown(f"**{selected_desc}**")

        with st.expander("📊 Classification (English Only)"):
            mapping = [
                ("Level 1 FA Module Code", "Level 1 FA Module - English Description"),
                ("Level 2 FA Module Code", "Level 2 FA Module - English Description"),
                ("Level 3 FA Module Code", "Level 3 FA Module - English Description"),
                ("accounting group Code", "accounting group English Description"),
                ("Asset Code For Accounting Purpose", "")
            ]

            table_data = []
            for code_field, en_field in mapping:
                table_data.append({
                    "Code": selected_row.get(code_field, ""),
                    "English": selected_row.get(en_field, "")
                })

            st.dataframe(pd.DataFrame(table_data))

            if st.button("📥 Export to PDF"):
                class PDF(FPDF):
                    def __init__(self):
                        super().__init__()
                        self.set_font("Arial", "", 12)

                    def header(self):
                        self.set_font("Arial", "B", 14)
                        self.cell(0, 10, "Asset Classification Report", ln=True, align="C")

                    def add_data(self, table_data):
                        self.set_font("Arial", "", 12)
                        self.ln(10)
                        self.set_fill_color(230, 230, 230)
                        self.cell(40, 10, "Code", 1, 0, "C", True)
                        self.cell(140, 10, "English", 1, 1, "C", True)

                        for row in table_data:
                            self.cell(40, 10, str(row["Code"]), 1)
                            self.cell(140, 10, str(row["English"]), 1, 1)

                pdf = PDF()
                pdf.add_page()
                pdf.add_data(table_data)

                pdf_bytes = pdf.output(dest="S").encode("latin1")

                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name="asset_report.pdf",
                    mime="application/pdf"
                )
