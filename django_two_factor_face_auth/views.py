from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import UserCreationForm, AuthenticationForm, UploadFileForm, Searchform
from .authenticate import FaceIdAuthBackend
from .utils import prepare_image
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .utils import base64_file
from .models import UserFile
from io import BytesIO
import json

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
            return redirect('/accounts/files/')
    else:
        form = UploadFileForm()
    
    context = {'form': form}
    return render(request, 'django_two_factor_face_auth/upload.html', context )

@login_required()
def viewfiles(request):
    if request.method == 'GET':
        flist = UserFile.objects.filter(user = request.user)
        form = Searchform()
        context = {'filelist': flist , 'form' : form} 
        return render(request, 'django_two_factor_face_auth/flist.html', context)

@login_required()
def fdelete(request):
    if request.method == 'POST':
        unic = request.body.decode('utf-8')
        body = json.loads(unic)
        content = body['fnames']
        files = content.split()
        print(files)
        sf = (UserFile.objects.filter(user = request.user))
        for f in sf:
            if f.ufilename() in files:
                f.delete()
        return HttpResponse(content)

@login_required()
def fsearch(request):
    if request.method == 'POST':
        form = Searchform(request.POST)
        nflist = []
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            flist = UserFile.objects.filter(user = request.user)
            for f in flist:
                if keyword in f.ufilename():
                    nflist.append(f)
        else:
            print("invalid")
        form = Searchform()
        context = {'filelist': nflist, 'form' : form}
        return render(request, 'django_two_factor_face_auth/flist.html', context)
    
@login_required()
def fdownload(request, dfile, user):
    if request.user.username == user:
        f = get_object_or_404(UserFile, ufile = "content/"+user+'/'+dfile)
        return FileResponse(f.ufile)

def index(request):
    if request.method == 'GET':
        return render(request, 'django_two_factor_face_auth/index.html')

def about(request):
    if request.method == 'GET':
        return render(request, 'django_two_factor_face_auth/about.html')