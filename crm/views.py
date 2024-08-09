from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, SalesPipeline
from .forms import ClientForm, SalesPipelineForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def client_list(request):
    clients = Client.objects.filter(owner=request.user)
    return render(request, 'crm/client_list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user
            client.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'crm/client_form.html', {'form': form})

def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'crm/client_form.html', {'form': form})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, owner=request.user)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'crm/client_list.html')

def sales_pipeline(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    pipeline, created = SalesPipeline.objects.get_or_create(client=client)
    if request.method == 'POST':
        form = SalesPipelineForm(request.POST, instance=pipeline)
        if form.is_valid():
            form.save()
    else:
        form = SalesPipelineForm(instance=pipeline)
    
    return render(request, 'crm/sales_pipeline.html', {
        'client': client,
        'form': form,
        'pipeline': pipeline,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('client_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('client_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')