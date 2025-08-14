from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('merge/', merge_pdfs, name='merge_pdfs'),
    path('split/', split_pdf, name='split_pdf'),
    path('extract/', extract_pages, name='extract_pages'),
    path('encrypt/', encrypt_pdf, name='encrypt_pdf'),
    path('hide/', hide_file_in_image, name='hide'),
    path('extract_img/', extract_file_from_images, name='efi'),

]