from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PyPDF2 import PdfReader, PdfWriter
from django.http import HttpResponse
from PIL import Image
from .serializers import FileHideSerializer, MultiplePDFUploadSerializer, SinglePDFUploadSerializer, ExtractPagesSerializer, EncryptPDFSerializer
import zipfile

class FileHideAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileHideSerializer(data=request.data)
        if serializer.is_valid():
            image_file = request.FILES['image']
            file = request.FILES['file']
            
            # بارگذاری تصویر
            image_bytes = image_file.read()
            
            # ترکیب فایل‌ها
            file_bytes = file.read()
            combined_bytes = image_bytes + file_bytes
            
            # ذخیره تصویر ترکیب شده به عنوان فایل
            response = HttpResponse(combined_bytes, content_type='image/jpeg')
            response['Content-Disposition'] = 'attachment; filename="combined_image.jpg"'
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MultiplePDFUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MultiplePDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdfs = request.FILES.getlist('pdfs')
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
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SinglePDFUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SinglePDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = request.FILES['pdf']
            reader = PdfReader(pdf_file)
            for page_num, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                output_path = f'split_page_{page_num + 1}.pdf'
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
            
            return Response({'message': 'PDF split successfully!'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExtractPagesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ExtractPagesSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = request.FILES['pdf']
            start_page = serializer.validated_data['start_page'] - 1
            end_page = serializer.validated_data['end_page']
            reader = PdfReader(pdf_file)
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
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    class EncryptPDFAPIView(APIView):
        def post(self, request, *args, **kwargs):
            serializer = EncryptPDFSerializer(data=request.data)
            if serializer.is_valid():
                pdf_file = request.FILES['pdf']
                password = serializer.validated_data['password']
                reader = PdfReader(pdf_file)
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
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
