import streamlit as st
import fitz  
import io

st.title("KE254 Ikuro_PDF Page Extractor")
st.markdown("Upload your PDF and enter the pages you want to extract (Example 1,3,7)")

uploaded_file = st.file_uploader("Choose your PDF", type="pdf")
page_input = st.text_input("Pages to extract (comma-separated):", placeholder="1,3,7")

if uploaded_file and page_input:
    try:
        # Read the PDF using fitz library
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        total_pages = len(doc)

        # Create new blank PDF
        new_doc = fitz.open()

        # Parse users input
        pages = page_input.split(",")
        for p in pages:
            try:
                page_index = int(p.strip()) - 1
                if 0 <= page_index < total_pages:
                    new_doc.insert_pdf(doc, from_page=page_index, to_page=page_index)
                else:
                    st.warning(f"Page {page_index+1} is out of range.")
            except ValueError:
                st.warning(f"Invalid page: {p}")

        # Save to in-memory buffer
        output_buffer = io.BytesIO()
        new_doc.save(output_buffer)
        new_doc.close()
        doc.close()

        # Download button
        st.download_button(
            label="Download Extracted PDF",
            data=output_buffer.getvalue(),
            file_name="extracted_pages.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Something went wrong: {e}")