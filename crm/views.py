from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, SalesPipeline
from .forms import ClientForm, SalesPipelineForm

# Create your views here.
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'crm/client_list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'crm/client_form.html', {'form': form})

def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'crm/client_form.html', {'form': form})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
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