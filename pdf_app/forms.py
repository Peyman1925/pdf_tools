from django import forms
from multiupload.fields import MultiFileField

class SinglePDFUploadForm(forms.Form):
    pdf = forms.FileField(label='Select a PDF file')

class MultiplePDFUploadForm(forms.Form):
    pdfs = MultiFileField(label='Select multiple PDF files', min_num=1, max_num=10, max_file_size=1024*1024*5) 

class ExtractPagesForm(forms.Form):
    pdf = forms.FileField(label='Select a PDF file')
    start_page = forms.IntegerField(label='Start Page')
    end_page = forms.IntegerField(label='End Page')

class EncryptPDFForm(forms.Form):
    pdf = forms.FileField(label='Select a PDF file')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class FileHideForm(forms.Form):
    image = forms.ImageField(label='Select a jpg Image')
    file = forms.FileField(label='Select a zip File')

class ImageUploadForm(forms.Form):
    image = forms.FileField(label="Upload Image")

class ImageExtractForm(forms.Form):
    images = MultiFileField(
        max_num=10,  
        min_num=1,   
        required=True,
        label="Upload Images"
    )