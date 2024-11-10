from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, FileResponse

from io import BytesIO

import os
import mimetypes
import zipfile

from .models import File, UserFile


def get_content_type(file_name):
    content_type, _ = mimetypes.guess_type(file_name)

    if content_type is None:
        return 'application/octet-stream'

    return content_type


@login_required
def download_folder(request):
    path = request.GET['path']
    archive_name = 'folder.zip'
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        for folder_root, folders, files in os.walk(path):
            for file in files:
                full_path = os.path.join(folder_root, file)
                archive.write(full_path, os.path.relpath(full_path, path))

    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachement; filename={archive_name}'

    return response


@login_required
def show_file(request):
    path = request.GET['path']
    file = open(path, 'rb')
    content_type = get_content_type(os.path.split(path)[-1])
    return FileResponse(file, content_type=content_type)


@login_required
def show_folder(request):
    path = request.GET['path']    
    content_list = os.listdir(path)
    files = []
    for file in content_list:
        type = 'D' if os.path.isdir(os.path.join(path, file)) else 'N'
        files.append(
            {
                'name': file,
                'path': os.path.join(path, file),
                'type': type,
                'exists': True
            }
        )

    return render(request, 'share/server-file-list.html', {'files': files})


@login_required
def server_file_list(request):
    files = File.objects.all()
    context = {'files': files}
    return render(request, "share/server-file-list.html", context)


@login_required
def user_file_list(request):
    user_files = UserFile.objects.filter(user=request.user)
    context = {'user_files': user_files}
    return render(request, "share/user-file-list.html", context)


@login_required
def shared_file_list(request):
    shared_files = UserFile.objects.filter(shared=True).exclude(user=request.user)
    context = {'shared_files': shared_files}
    return render(request, "share/shared-file-list.html", context)


@login_required
def add_file(request):
    if request.user.is_superuser:
        path = request.GET.get('path')

        path = path[:-2] if path[-1] == '/' or path[-1] == '\\' else path

        if os.path.exists(path):
            if not File.objects.filter(path=path).exists():
                name = os.path.split(path)[-1]

                if os.path.isdir(path):
                    file_type = 'D'
                else:
                    file_type = 'N'

                file = File.objects.create(name=name, path=path, type=file_type, user=request.user)

        else:
            messages.error(request, "The path doesn't exists.")

    return redirect(reverse('share:server-file-list'))


@login_required
def remove_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if file.user == request.user:
        file.delete()

    return redirect(reverse('share:server-file-list'))


@login_required
def upload_file(request):
    file = request.FILES['file']
    UserFile.objects.create(file=file, user=request.user)
    return redirect(reverse('share:user-file-list'))


@login_required
def switch_sharing_state(request, user_file_id):
    user_file = get_object_or_404(UserFile, pk=user_file_id)
    user_file.switch_shared()
    return redirect(reverse('share:user-file-list'))


@login_required
def remove_user_file(request, user_file_id):
    user_file = get_object_or_404(UserFile, pk=user_file_id)
    if request.user == user_file.user:
        user_file.delete()
        
    return redirect(reverse('share:user-file-list'))
