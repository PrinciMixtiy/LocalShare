from django.urls import path
from .views import server_file_list, add_file,\
remove_file, show_file, show_folder, download_folder,\
upload_file, user_file_list, shared_file_list,\
switch_sharing_state, remove_user_file

app_name = 'share'
urlpatterns = [
    path("", server_file_list, name="server-file-list"),
    path('my-files/', user_file_list, name='user-file-list'),
    path('shared-files/', shared_file_list, name='shared-file-list'),
    path('add-file/', add_file, name='add-file'),
    path('remove-file/<int:file_id>/', remove_file, name='remove-file'),
    path('dir-content/', show_folder, name='dir-content'),
    path('file-content/', show_file, name='file-content'),
    path('download-folder/', download_folder, name='download-folder'),
    path('upload/', upload_file, name='upload-file'),
    path('switch-sharing-state/<int:user_file_id>/', switch_sharing_state, name='switch-sharing-state'),
    path('remove-my-file/<int:user_file_id>/', remove_user_file, name='remove-user-file')
]
