import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

st.title("Excel to PDF Report Generator")

# Upload Excel File
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Read Excel data
    df = pd.read_excel(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(df)

    # Allow user to select rows
    preview_limit = 100
    index_list = df.index[:preview_limit]
    selected_rows = st.multiselect(
        f"Select up to {preview_limit} rows to include in the PDF",
        index_list
    )

    # Generate PDF button
    if st.button("Generate PDF Report"):
        selected_data = df.loc[selected_rows]

        # Create PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for index, row in selected_data.iterrows():
            for col, val in row.items():
                pdf.cell(200, 10, txt=f"{col}: {val}", ln=True)
            pdf.ln(5)

        # Save PDF
        pdf_output_path = "report.pdf"
        pdf.output(pdf_output_path)

        # Let user download the PDF
        with open(pdf_output_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="report.pdf", mime="application/pdf")

        os.remove(pdf_output_path)