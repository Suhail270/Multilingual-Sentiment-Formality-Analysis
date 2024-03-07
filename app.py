import streamlit as st
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from streamlit_extras.switch_page_button import switch_page


# Function for reading PDF using PyPDF2

def read_pdf_page(file, page_number):
    pdfReader = PdfReader(file)
    page = pdfReader.pages[page_number]
    text = page.extract_text()
    text = text.split("\n")
    return page.extract_text()


def on_text_area_change():
    st.session_state.page_text = st.session_state.my_text_area


def main():
    st.set_page_config(page_title="PDF Upload and Display")
    st.title("PDF Upload and Display")
    # PDF file upload
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file:
        # Create a selectbox to choose the page number
        if st.button("Read PDF"):
            switch_page("read")

        pdfReader = PdfReader(pdf_file)
        page_numbers = list(range(1, len(pdfReader.pages) + 1))
        selected_page = st.selectbox("Select a page", page_numbers)
        selected_page -= 1
        # Convert the selected page to an image
        images = convert_from_bytes(pdf_file.getvalue())
        image = images[selected_page]

        # Create two columns to display the image and text
        col1, col2 = st.columns(2)

        pdf_content = read_pdf_page(pdf_file, selected_page)

        st.session_state['pdf_content'] = pdf_content

        # Display the image in the first column
        col1.image(image, caption=f"Page {selected_page + 1}")

        col2.text_area("Page Text", height=800, value=pdf_content,
                       key="my_text_area", on_change=on_text_area_change)
        

if __name__ == '__main__':
    main()
