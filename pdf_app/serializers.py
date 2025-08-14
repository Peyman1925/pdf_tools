# # pdf_app/serializers.py

# from rest_framework import serializers

# class FileHideSerializer(serializers.Serializer):
#     image = serializers.ImageField()
#     file = serializers.FileField()

# class MultiplePDFUploadSerializer(serializers.Serializer):
#     pdfs = serializers.ListField(
#         child=serializers.FileField(),
#         min_length=1,
#         max_length=10
#     )

# class SinglePDFUploadSerializer(serializers.Serializer):
#     pdf = serializers.FileField()

# class ExtractPagesSerializer(serializers.Serializer):
#     pdf = serializers.FileField()
#     start_page = serializers.IntegerField()
#     end_page = serializers.IntegerField()

# class EncryptPDFSerializer(serializers.Serializer):
#     pdf = serializers.FileField()
#     password = serializers.CharField(write_only=True)