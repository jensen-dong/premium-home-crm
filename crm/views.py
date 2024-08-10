from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, SalesPipeline, Campaign, Order, Lead, Product
from .forms import ClientForm, SalesPipelineForm, ProductForm, CampaignForm, OrderForm, ProductFormSet
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def redirect_to_appropriate_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')
    
def client_list(request):
    clients = Client.objects.filter(owner=request.user)
    client_data = []
    for client in clients:
        pipeline, created = SalesPipeline.objects.get_or_create(client=client)
        total_revenue = sum(product.normal_price for product in pipeline.products.all())
        client_data.append({
            'client': client,
            'stage': pipeline.get_current_stage_display(),
            'total_revenue': total_revenue,
        })

    sort_by = request.GET.get('sort_by', 'name')
    if sort_by == 'stage':
        client_data.sort(key=lambda x: x['stage'])
    elif sort_by == 'revenue':
        client_data.sort(key=lambda x: x['total_revenue'], reverse=True)
    else:
        client_data.sort(key=lambda x: x['client'].name)

    return render(request, 'crm/client_list.html', {'client_data': client_data, 'sort_by': sort_by})

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
        return HttpResponseRedirect(reverse('client_list'))
    
    return HttpResponseRedirect(reverse('client_list'))

def sales_pipeline(request, client_id):
    print("Request method:", request.method)
    client = get_object_or_404(Client, id=client_id, owner=request.user)
    pipeline, created = SalesPipeline.objects.get_or_create(client=client)

    products = pipeline.products.all()
    total_revenue = sum(product.normal_price for product in products)

    form = SalesPipelineForm(instance=pipeline)
    product_form = ProductForm()
    order_form = OrderForm()

    if request.method == 'POST':
        print("Handling POST request")
        if 'stage_form' in request.POST:
            form = SalesPipelineForm(request.POST, instance=pipeline)
            if form.is_valid():
                form.save()
                return redirect('sales_pipeline', client_id=client_id)
        elif 'product_form' in request.POST:
            print("Handling product form submission")
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.pipeline = pipeline
                product.save()
                print("Product added successfully:", product.name)
                return redirect('sales_pipeline', client_id=client_id)
            else:
                print("Product form is not valid. Errors:", product_form.errors)
        elif 'order_form' in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.pipeline = pipeline
                order.total_price = total_revenue 
                order.save()
                return redirect('sales_pipeline', client_id=client_id)

    return render(request, 'crm/sales_pipeline.html', {
        'client': client,
        'form': form,
        'product_form': product_form,
        'order_form': order_form,
        'pipeline': pipeline,
        'products': products,
        'total_revenue': total_revenue,
        'orders': pipeline.orders.all(),
    })

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    pipeline_id = product.pipeline.id 
    client_id = product.pipeline.client.id

    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('sales_pipeline', args=[client_id]))

    return redirect('sales_pipeline', client_id=client_id)

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
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
    
def campaign_list(request):
    campaigns = Campaign.objects.filter(owner=request.user)
    return render(request, 'crm/campaign_list.html', {'campaigns': campaigns})

def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        formset = ProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            campaign = form.save(commit=False)
            campaign.owner = request.user
            campaign.save()
            products = formset.save(commit=False)
            for product in products:
                product.campaign = campaign
                product.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm()
        formset = ProductFormSet()

    return render(request, 'crm/campaign_form.html', {'form': form, 'formset': formset})

def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm(instance=campaign)
    
    return render(request, 'crm/campaign_detail.html', {'campaign': campaign, 'form': form})

def send_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    clients = Client.objects.filter(owner=request.user)
    
    for client in clients:
        Lead.objects.create(client=client, campaign=campaign)
    
    return redirect('campaign_list')

def campaign_delete(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if request.method == 'POST':
        campaign.delete()
        return HttpResponseRedirect(reverse('campaign_list'))

    return HttpResponseRedirect(reverse('campaign_detail', args=[campaign_id]))

def lead_list(request):
    leads = Lead.objects.filter(client__owner=request.user)
    return render(request, 'crm/lead_list.html', {'leads': leads})

def dashboard(request):

    pipelines = SalesPipeline.objects.filter(client__owner=request.user)
    
    revenue_order_stage = sum(product.normal_price for pipeline in pipelines if pipeline.current_stage == 'order' for product in pipeline.products.all())
    revenue_other_stages = sum(product.normal_price for pipeline in pipelines if pipeline.current_stage != 'order' for product in pipeline.products.all())
    
    clients = Client.objects.filter(owner=request.user)
    leads = Lead.objects.filter(client__owner=request.user).select_related('client', 'campaign')

    context = {
        'revenue_order_stage': revenue_order_stage,
        'revenue_other_stages': revenue_other_stages,
        'clients': clients,
        'leads': leads,
    }
    return render(request, 'crm/dashboard.html', context)