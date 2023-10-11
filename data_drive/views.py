from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from . import forms #LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from .forms import FolderForm, FileForm
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import FolderForm, FileForm
from .models import Folder

def home(request):
    try:
        login_form = forms.LoginForm()
        register_form = forms.RegistrationForm()

        if request.method == 'POST':
            if 'login_submit' in request.POST:
                login_form = forms.LoginForm(request.POST)
                if login_form.is_valid():
                    username = login_form.cleaned_data['username']
                    password = login_form.cleaned_data['password']
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect(dashboard)
                    
            elif 'register_submit' in request.POST:
                register_form = forms.RegistrationForm(request.POST)
                if register_form.is_valid():
                    username = register_form.cleaned_data['username']
                    email = register_form.cleaned_data['email']
                    password = register_form.cleaned_data['password']
                    new_user = User(username=username, email=email)
                    new_user.set_password(password)
                    new_user.save()

        context = {'login_form': login_form, 'register_form': register_form}
        return render(request, 'authentication.html', context)
    except Http404:
        return render(request, '404.html', status=404)

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"user":request.user})




class CreateFolderView(View):
    template_name = 'folder.html'

    def get(self, request):
        folder_form = FolderForm()
        file_form = FileForm()
        folders = Folder.objects.filter(owner=request.user, no_parent_folder=True)
        subfile = File.objects.filter(owner=request.user, folder_id=None)
        context = {'folders': folders, 'files': subfile, 'form': folder_form, 'form2': file_form, 'back_id': None}
        return render(request, self.template_name, context)

    def post(self, request):
        if 'create_folder' in request.POST:
            form = FolderForm(request.POST)
        elif 'upload_file' in request.POST:
            form = FileForm(request.POST, request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            if 'create_folder' in request.POST:
                obj.no_parent_folder = True
            elif 'upload_file' in request.POST:
                obj.folder = None  # You can set the folder here if needed
            obj.save()
            return redirect('create_folder')

        folder_form = FolderForm()
        file_form = FileForm()
        folders = Folder.objects.filter(owner=request.user, no_parent_folder=True)
        subfile = File.objects.filter(owner=request.user, folder_id=None)
        context = {'folders': folders, 'files': subfile, 'form': folder_form, 'form2': file_form, 'back_id': None}
        return render(request, self.template_name, context)

class ShowFolderView(View):
    template_name = 'folder.html'

    def get(self, request, folder_id):
        if folder_id == 0:
            return redirect('create_folder')
        subfolders = Folder.objects.filter(parent_folder_id=folder_id, owner=request.user)
        subfile = File.objects.filter(owner=request.user, folder_id=folder_id)
        parent_id = Folder.objects.filter(id = folder_id).values("parent_folder")[0]['parent_folder']
        print(parent_id)
        if parent_id == None:
            parent_id = 0
        else:
            parent_id = int(parent_id)
        folder_form = FolderForm()
        file_form = FileForm()
        context = {'folders': subfolders, 'files': subfile, 'form': folder_form, 'form2': file_form, 'back_id': parent_id}
        return render(request, self.template_name, context)

    def post(self, request, folder_id):
        if 'create_folder' in request.POST:
            form = FolderForm(request.POST)
        elif 'upload_file' in request.POST:
            form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            if 'create_folder' in request.POST:
                obj.parent_folder_id = folder_id
            elif 'upload_file' in request.POST:
                obj.folder_id = folder_id
            obj.save()
            folder_url = reverse('show_folder', args=[folder_id])
            return redirect(folder_url)

        subfolders = Folder.objects.filter(parent_folder_id=folder_id, owner=request.user)
        subfile = File.objects.filter(owner=request.user, folder_id=folder_id)
        parent_id = Folder.objects.filter(id = folder_id).values("parent_folder")[0]['parent_folder']
        folder_form = FolderForm()
        file_form = FileForm()
        context = {'folders': subfolders, 'files': subfile, 'form': folder_form, 'form2': file_form, 'back_id': int(parent_id)}
        return render(request, self.template_name, context)



def previous_page(request, previous_id):
    folder_id = previous_id
    folder_url = reverse('show_folder', args=[folder_id])
    return redirect(folder_url)



