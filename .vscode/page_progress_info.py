import subprocess
import time
import sys
import os


# Check if PyMuPDF is installed, and install it if it's missing
def check_and_install_pymupdf():
    try:
        import fitz  # Try to import PyMuPDF (fitz)
    except ImportError:
        # If not installed, install it via pip
        print('PyMuPDF is not installed. Installing now...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyMuPDF'])
        print('PyMuPDF installed successfully!')
        import fitz  # Re-import after installation


# Call the function to check/install PyMuPDF
check_and_install_pymupdf()


import fitz


def is_blank_or_image(page):
    """Checks if a page is either blank or contains only an image."""
    text = page.get_text('text').strip()
    # If no text is present, consider it blank or image-only
    if len(text) == 0:
        return True
    return False


def count_text_pages_in_pdf(pdf_path):
    """Counts pages that contain Arabic numerals and have text content."""
    doc = fitz.open(pdf_path)
    main_started = False
    text_page_count = 0

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text('text')

        # Check if the main content has started
        if text.startswith('Chapter 1') and not main_started:
            main_started = True

        if main_started:
            # Check if the page is already sources -> end of main content
            if text.startswith('Bibliography') or text.startswith('Appendix'):
                break
            # Only count pages that are not blank or image-only
            if not is_blank_or_image(page):
                text_page_count += 1

    doc.close()
    return text_page_count


# Get current time
end_time = time.time()

# Get the path to the script and the PDF file
script_path = os.path.dirname(os.path.realpath(__file__))
pdf_path = os.path.join(script_path, '..', 'src', 'thesis.pdf')

if not os.path.exists(pdf_path):
    print('Error: The PDF file does not exist!')
    
    # Check and read temp time file
    temp_file_path = os.path.join(script_path, 'start.temp')
    if os.path.exists(temp_file_path):
        with open(temp_file_path, 'r') as temp_file:
            start_time = float(temp_file.read())
        
        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        
        print(f'\nNeeded time for build: {elapsed_time:.2f} seconds')

        # Remove the temporary file
        os.remove(temp_file_path)
        
else:
    # Count the pages and print progress for 20 and 30 pages
    page_list = [20, 30]
    text_pages = count_text_pages_in_pdf(pdf_path)

    page_completed = [text_pages / page for page in page_list]
    for i, page in enumerate(page_list):
        print(f'Progress for {page} pages: {text_pages}/{page} ({page_completed[i] * 100:.2f}%)')

    avg_completion = sum(page_completed) / len(page_list)
    length_of_line = 35
    completed_length = int(avg_completion * length_of_line)
    remaining_length = length_of_line - completed_length
    print(f'[{"#" * completed_length}{"-" * remaining_length}]')

    # Check and read temp time file
    temp_file_path = os.path.join(script_path, 'start.temp')
    if os.path.exists(temp_file_path):
        with open(temp_file_path, 'r') as temp_file:
            start_time = float(temp_file.read())

        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        
        # Get the total amount of pages in the PDF
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        doc.close()

        # Calculate the average time per page
        avg_time_per_page = elapsed_time / total_pages
        print(f'\nNeeded time for build: {elapsed_time:.2f} seconds (~{avg_time_per_page:.2f} s/page)')

        # Remove the temporary file
        os.remove(temp_file_path)

