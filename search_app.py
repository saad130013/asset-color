
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import io

st.set_page_config(page_title="🔍 Smart Asset Lookup", layout="centered", page_icon="🔍")
st.title("🔍 Smart Asset Description Autocomplete with PDF Export (Arabic + English)")

@st.cache_data
def load_data():
    df = pd.read_excel("assetv4.xlsx", header=1)
    df = df[df.columns.dropna()]
    df = df.dropna(subset=["Asset Description"])
    return df

df = load_data()
descriptions = df["Asset Description"].astype(str).tolist()

@st.cache_resource
def create_vectorizer():
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(descriptions)
    return vectorizer, vectors

vectorizer, description_vectors = create_vectorizer()

user_input = st.text_input("✍️ Start typing asset description:")

if user_input:
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, description_vectors).flatten()
    top_indices = similarities.argsort()[-5:][::-1]

    suggestions = [descriptions[i] for i in top_indices]
    selected_suggestion = st.selectbox("💡 Suggestions:", suggestions)

    if selected_suggestion:
        st.markdown("### 🧾 Selected Description:")
        st.markdown(f"**{selected_suggestion}**")

        selected_row = df[df["Asset Description"] == selected_suggestion].iloc[0]

        with st.expander("📊 Classification Details"):
            st.markdown("### 🔄 Accounting Classification Matrix")

            # جدول التصنيف المزدوج
            mapping = [
                ("Level 1 FA Module Code", "Level 1 FA Module - English Description", "Level 1 FA Module - Arabic Description"),
                ("Level 2 FA Module Code", "Level 2 FA Module - English Description", "Level 2 FA Module - Arabic Description"),
                ("Level 3 FA Module Code", "Level 3 FA Module - English Description", "Level 3 FA Module - Arabic Description"),
                ("accounting group Code", "accounting group English Description", "accounting group Arabic Description"),
                ("Asset Code For Accounting Purpose", "", "")
            ]

            table_data = []
            for code_field, en_field, ar_field in mapping:
                table_data.append({
                    "Code": selected_row.get(code_field, ""),
                    "English": selected_row.get(en_field, ""),
                    "Arabic": selected_row.get(ar_field, "")
                })

            table_df = pd.DataFrame(table_data)
            st.dataframe(table_df.style.set_properties(subset=["Arabic"], **{
                "color": "green", "font-weight": "bold"
            }))

            if st.button("📥 Export to PDF"):
                class PDF(FPDF):
                    def __init__(self):
                        super().__init__()
                        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
                        self.set_font('DejaVu', '', 12)

                    def header(self):
                        self.set_font("DejaVu", "", 14)
                        self.cell(0, 10, "Asset Classification Report", ln=True, align="C")

                    def footer(self):
                        self.set_y(-15)
                        self.set_font("DejaVu", "", 8)
                        self.cell(0, 10, f"Page {self.page_no()}", align="C")

                    def add_data(self, table_data):
        self.set_font("DejaVu", "", 12)
        self.ln(10)
        self.set_fill_color(230, 230, 230)
        self.cell(40, 10, "Code", 1, 0, "C", True)
        self.cell(140, 10, "English", 1, 1, "C", True)
        for row in table_data:
            self.cell(40, 10, str(row["Code"]), 1)
            self.cell(140, 10, str(row["English"]), 1, 1)

                        self.set_font("DejaVu", "", 12)
                        self.ln(10)
                        self.set_fill_color(230, 230, 230)
                        self.cell(40, 10, "Code", 1, 0, "C", True)
                        self.cell(75, 10, "English", 1, 0, "C", True)
                        self.cell(75, 10, "Arabic", 1, 1, "C", True)

                        for row in table_data:
                            self.cell(40, 10, str(row["Code"]), 1)
                            self.cell(75, 10, str(row["English"]), 1)
                            self.cell(75, 10, str(row["Arabic"]), 1, 1)

                pdf = PDF()
                pdf.add_page()
                pdf.add_data(table_data)

                pdf_buffer = io.BytesIO()
                pdf.output(pdf_buffer)

                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_buffer.getvalue(),
                    file_name="asset_classification.pdf",
                    mime="application/pdf"
                )
