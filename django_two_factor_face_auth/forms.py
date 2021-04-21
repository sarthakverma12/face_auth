from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserFaceImage, UserFile
from .utils import base64_file
from .encrypt import encrypti
from io import BytesIO

class UserCreationForm(UserCreationForm):
    image = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserFaceImage without database save")
        user = super(UserCreationForm, self).save(commit=True)
        image = base64_file(self.data['image'])
        image = encrypti(image)
        face_image = UserFaceImage(user=user, image=image)
        face_image.save()
        return user

class AuthenticationForm(AuthenticationForm):
    image = forms.CharField(widget=forms.HiddenInput())

class UploadFileForm(forms.Form):
    upfile = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class Searchform(forms.Form):
    keyword = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Search..'}))

    