from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import UserCreationForm, AuthenticationForm, UploadFileForm
from .authenticate import FaceIdAuthBackend
from .utils import prepare_image
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .utils import base64_file
from .models import UserFile
from io import BytesIO

def register(request):
    if  request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'django_two_factor_face_auth/register.html', context)

def face_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            face_image = prepare_image(form.cleaned_data['image'])

            face_id = FaceIdAuthBackend()
            user = face_id.authenticate(username=username, password=password, face_id=face_image)
            if user is not None:
                login(request, user)
                return redirect('/accounts/menu/')
            else:
                form.add_error(None, "Username, password or face id didn't match.")
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'django_two_factor_face_auth/login.html', context)

@login_required()
def menu(request):
    if request.method == 'GET':
        context = {'username': request.user.username}
        return render(request, 'django_two_factor_face_auth/menu.html', context)

@login_required()
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            flist = request.FILES.getlist('upfile')
            for ufc in flist:
               uf = UserFile(user = request.user, ufile = ufc)
               uf.save()
            return HttpResponse('Files uploaded successfully')
    else:
        form = UploadFileForm()
    
    context = {'form': form}
    return render(request, 'django_two_factor_face_auth/upload.html', context )

@login_required()
def viewfiles(request):
    if request.method == 'GET':
        flist = UserFile.objects.filter(user = request.user)
        context = {'filelist': flist}
        return render(request, 'django_two_factor_face_auth/flist.html', context)

# @login_required()
# def fdelete(request):
#     if request.method == 'POST':
        