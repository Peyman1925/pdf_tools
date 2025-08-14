from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
from .forms import *
from PIL import Image
import tempfile
import os
from cryptosteganography import CryptoSteganography
import zipfile
from .forms import ImageExtractForm
from cryptosteganography import CryptoSteganography

def home(request):
    return render(request, 'home.html')

def merge_pdfs(request):
    if request.method == 'POST':
        form = MultiplePDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdfs = form.cleaned_data['pdfs']
            merger = PdfWriter()
            
            for pdf in pdfs:
                reader = PdfReader(pdf)
                for page in reader.pages:
                    merger.add_page(page)
            
            output_path = 'merged.pdf'
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            
            with open(output_path, 'rb') as output_file:
                response = HttpResponse(output_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{output_path}"'
                return response
    else:
        form = MultiplePDFUploadForm()

    return render(request, 'merge.html', {'form': form})

def split_pdf(request):
    if request.method == 'POST':
        form = SinglePDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = request.FILES['pdf']
            reader = PdfReader(pdf)
            for page_num, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                output_path = f'split_page_{page_num + 1}.pdf'
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
            
            return HttpResponse('PDF split successfully!')
    else:
        form = SinglePDFUploadForm()

    return render(request, 'split.html', {'form': form})

def extract_pages(request):
    if request.method == 'POST':
        form = ExtractPagesForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = request.FILES['pdf']
            start_page = form.cleaned_data['start_page'] - 1
            end_page = form.cleaned_data['end_page']
            reader = PdfReader(pdf)
            writer = PdfWriter()
            
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            output_path = 'extracted_pages.pdf'
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            with open(output_path, 'rb') as output_file:
                response = HttpResponse(output_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{output_path}"'
                return response
    else:
        form = ExtractPagesForm()

    return render(request, 'extract.html', {'form': form})

def encrypt_pdf(request):
    if request.method == 'POST':
        form = EncryptPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = request.FILES['pdf']
            password = form.cleaned_data['password']
            reader = PdfReader(pdf)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(password)
            
            output_path = 'encrypted.pdf'
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            with open(output_path, 'rb') as output_file:
                response = HttpResponse(output_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{output_path}"'
                return response
    else:
        form = EncryptPDFForm()

    return render(request, 'encrypt.html', {'form': form})


#=========================================================
#=========================================================
#===================For other Files=======================
#=========================================================
#=========================================================

def hide_file_in_image(request):
    if request.method == 'POST':
        form = FileHideForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            file = request.FILES['file']
            
            image_bytes = image_file.read()
            
            file_data = file.read()
            combined_data = image_bytes + file_data
            
            response = HttpResponse(content_type='image/jpeg')
            response['Content-Disposition'] = 'attachment; filename="combined_image.jpg"'
            response.write(combined_data)
            
            return response
    else:
        form = FileHideForm()
    
    return render(request, 'hide_file.html', {'form': form})

def extract_file_from_images(request):
    if request.method == 'POST':
        form = ImageExtractForm(request.POST, request.FILES)
        if form.is_valid():
            images = form.files.getlist('images') 
            secret_key = 'my_secret_key'  
            crypto_steganography = CryptoSteganography(secret_key)
            
            all_data = b''
            for image in images:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image:
                    for chunk in image.chunks():
                        temp_image.write(chunk)
                    image_path = temp_image.name
                
                img = Image.open(image_path)
                hidden_data = crypto_steganography.retrieve(img)
                all_data += hidden_data.encode('latin-1')
                
                os.remove(image_path)

            zip_path = 'extracted_files.zip'
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                with zipfile.ZipFile(temp_zip, 'w') as zipf:
                    zipf.writestr('extracted_data', all_data)
                zip_path = temp_zip.name
            
            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="extracted_files.zip"'
                return response
    else:
        form = ImageExtractForm()

    return render(request, 'extract_file_from_image.html', {'form': form})