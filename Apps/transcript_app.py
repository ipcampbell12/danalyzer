import pymupdf as fitz
from datetime import datetime
from task_manager import DataTaskManager
import os
import shutil
from pathlib import Path
from PyPDF2 import PdfWriter, PdfReader

manager = DataTaskManager()
folders = manager.return_folders()
assets_folder = folders["assets_folder"]


def add_images_to_pdf(input_pdf, images_info, add_date=False):
    try:
        # Open the PDF file
        pdf_document = fitz.open(input_pdf)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return
    
    num_pages = len(pdf_document)
    print(f"Number of pages in PDF: {num_pages}")
    
    seal_added = False
    current_date = datetime.now().strftime("%m/%d/%Y")
    
    for image_info in images_info:
        try:
            # Open the image file
            image = fitz.open(image_info["path"])
            if image.is_closed:
                raise Exception("Image file could not be opened.")
        except Exception as e:
            print(f"Error opening image file: {e}")
            continue
        
        try:
            # Adjust page number if the PDF only has one page
            page_num = image_info.get("page_num", 0)
            if num_pages == 1:
                page_num = 0  # Override to the first page if only one page exists
            
            if page_num >= num_pages:
                print(f"Invalid page number {page_num}. Skipping image.")
                continue
            
            # Select the page to add the image to
            page = pdf_document[page_num]
            
            # Check if the image is a seal and has already been added
            if num_pages == 1 and "seal" in str(image_info["path"]).lower() and seal_added:
                print(f"Seal already added. Skipping duplicate.")
                continue
            
            # Define the rectangle where the image will be placed
            image_rectangle = fitz.Rect(image_info["x"], image_info["y"], 
                                        image_info["x"] + image_info["width"], 
                                        image_info["y"] + image_info["height"])
            print(f"Image rectangle: {image_rectangle}")

            # Insert the image into the PDF
            page.insert_image(image_rectangle, filename=str(image_info["path"]))
            print("Image inserted successfully.")
            
            # Mark seal as added
            if "seal" in str(image_info["path"]).lower():
                seal_added = True
            
            # Add the current date near the signature if enabled
            if add_date and "signature" in str(image_info["path"]).lower():
                date_x = image_info["x"] + image_info["width"] + 10  # Adjust X position to the right of the signature
                date_y = image_info["y"] + 113  # Adjust Y position slightly down
                page.insert_text((date_x, date_y), current_date, fontsize=12, color=(0, 0, 0))  # Add date text
                print(f"Date added next to signature: {current_date}")
            
        except Exception as e:
            print(f"Error inserting image: {e}")
            continue
    
    name = str(input_pdf).rsplit('.pdf', 1)[0]

    output_pdf = f"{name} - Official.pdf"

    try:
        # Save the updated PDF
        pdf_document.save(output_pdf)
        print(f"PDF saved successfully as {output_pdf}.")
    except Exception as e:
        print(f"Error saving PDF file: {e}")
    
    # Close the PDF document
    pdf_document.close()
    
    return output_pdf

# Example usage
signature_image = assets_folder / "signature_transparent.png"
seal_image = assets_folder / "seal_transparent.png"

# Images information: path, coordinates, size, and page number
ps_images_info = [
    {"path": signature_image, "x": 320, "y": 624, "width": 150, "height": 200, "page_num": 1},  # Signature on second page if exists
    {"path": seal_image, "x": 410, "y": 650, "width": 125, "height": 125, "page_num": 0},  # Seal on first page
    {"path": seal_image, "x": 410, "y": 650, "width": 125, "height": 125, "page_num": 1}   # Seal on second page if exists
]

sassie_images_info = [
    {"path": signature_image, "x": 402, "y": 610, "width": 150, "height": 200, "page_num": 1},  # Signature on second page if exists
    {"path": seal_image, "x": 480, "y": 650, "width": 125, "height": 125, "page_num": 0},  # Seal on first page
    {"path": seal_image, "x": 470, "y": 650, "width": 125, "height": 125, "page_num": 1}   # Seal on second page if exists
]
upper_sassie_images_info = [
    {"path": signature_image, "x": 405, "y": 660, "width": 150, "height": 200, "page_num": 1},  # Signature on second page if exists
    {"path": seal_image, "x": 470, "y": 650, "width": 125, "height": 125, "page_num": 0},  # Seal on first page
    {"path": seal_image, "x": 475, "y": 670, "width": 125, "height": 125, "page_num": 1}   # Seal on second page if exists
]


def protect_pdf(input_pdf, password):
    # Initialize a PdfWriter object to handle encryption
    writer = PdfWriter()

    # Open the PDF to read
    with open(input_pdf, "rb") as file:
        reader = PdfReader(file)
        
        # Add all pages from the input PDF to the writer object
        for page in reader.pages:
            writer.add_page(page)

        # Encrypt the PDF with the given password
        writer.encrypt(password)

    # Save the password-protected PDF, overwriting the original file
    with open(input_pdf, "wb") as file:
        writer.write(file)
    
    print(f"PDF has been password protected and saved as {input_pdf}")


# Move the output file to a new folder

def proccess_transcript(transcript_file,processed_transcripts_folder):
    output_file = add_images_to_pdf(transcript_file, ps_images_info, add_date=False)
    # password = "password1"
    # protect_pdf(output_file,password)
    if output_file:
        try:
            output_file_path = Path(output_file)  # Convert to Path object
            shutil.move(output_file_path, processed_transcripts_folder / output_file_path.name)
            print(f"File moved to {processed_transcripts_folder / output_file_path.name}")
            os.startfile(processed_transcripts_folder / output_file_path.name)
        except Exception as e:
            print(f"Error moving file: {e}")


# proccess_transcript("BO Transcript.pdf",r"C:\Users\inpcampbell\Desktop\Processing Output\Processed Transcripts")
