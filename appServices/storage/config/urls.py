from django.contrib import admin
from django.urls import path
from app.controllers.storageDataController import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('storages', GetStorageData.as_view(), name='get_storage_data'),
    path('storage/create', CreateStorageData.as_view(), name='create_storage_data'),
    path('storage/update', UpdateStorageData.as_view(), name='update_storage_data'),
    path('storage/delete', DeleteStorageData.as_view(), name='delete_storage_data'),
    path('storage/upload', UploadFile.as_view(), name='upload_file'),
    path('storage/public-url', GenPublicUrl.as_view(), name='gen_public_url'),
    path('storage/<str:id>', GetStorageData.as_view(), name='get_storage_data_by_id'),
]
