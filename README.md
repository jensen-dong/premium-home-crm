# Premium Home CRM

## Description
Premium Home CRM is a robust customer relationship management application tailored for businesses dealing with high-end audio and appliance packages. The app helps manage sales pipelines, leads, and marketing campaigns. It streamlines workflows, improves customer satisfaction, and boosts sales efficiency.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript, Bootstrap, Chart.js
- **Backend:** Python, Django, PostgreSQL

## Features
- Client management (CRUD)
- Sales pipeline tracking
- Lead management system
- Marketing campaign management
- Responsive frontend templates

## DEMO
[Render Site](https://premium-home-crm.onrender.com/)
- Demo username: testuser
- Demo password: Password123

- Use demo account for preset data in the database. Or you can create your own account and create your own data!
- Please do not modify data in demo account!

![Screenshot 2024-08-10 at 4 30 06 PM](https://github.com/user-attachments/assets/7f7a48d9-a77a-4895-8307-acde89bca955)


## Setup and Installation
1. Clone the repository
   ```zsh
   git clone https://github.com/jensen-dong/premium-home-crm.git
   ```
2. Set up virtual environment
   ```zsh
   cd premium-home-crm
   brew install pipenv
   pipenv shell
   ```
3. Set up PostgreSQL
   - Create new PostgreSQL database
   - Update DATABASES config in settings.py
4. Run migrations
   ```zsh
   python manage.py migrate
   ```
5. Create superuser
   ```zsh
   python manage.py createsuperuser
   ```
6. Start dev server
   ```zsh
   python manage.py runserver
   ```
## Usage
1. Navigate to http://127.0.0.1:8000/ in your browser.
2. Log in with your superuser account.
3. Start managing clients, interactions, leads, pipelines, and marketing campaigns.

## ERD
![Screenshot 2024-08-06 at 7 33 34 PM](https://github.com/user-attachments/assets/e6525f11-9995-4a4d-ae4d-9f00053b2879)

## Wireframes

- Dashboard (MVP)
  
![Screenshot 2024-08-06 at 8 02 51 PM](https://github.com/user-attachments/assets/b50f1523-dbbe-4ad2-8623-d1d9395ac815)

- Book of Business

![Screenshot 2024-08-06 at 8 02 57 PM](https://github.com/user-attachments/assets/94272471-1efc-4a39-8e55-41fb4e27070d)

- Leads

![Screenshot 2024-08-06 at 8 03 12 PM](https://github.com/user-attachments/assets/207fb209-99ec-4964-bf65-26ca8c241928)

- Pipeline (MVP)
  
![Screenshot 2024-08-06 at 8 03 07 PM](https://github.com/user-attachments/assets/6fe969b3-76f2-4281-930f-7309149221a5)

- Marketing Campaign

![Screenshot 2024-08-06 at 8 03 01 PM](https://github.com/user-attachments/assets/706b6fd4-bd07-432a-b65e-5b013577ac80)

## Code Snippet
### sales_pipeline view function
```python
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
```

### Graphing logic
```Python
# views.py
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
```

```HTML
<script>
    // eslint-disable-next-line no-undef
    const revenueOrderStage = {{ revenue_order_stage|default:0 }};
    const revenueOtherStages = {{ revenue_other_stages|default:0 }};
    
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Order Stage', 'Other Stages'],
            datasets: [{
                label: 'Total Revenue',
                data: [revenueOrderStage, revenueOtherStages],
                backgroundColor: ['rgba(54, 162, 235, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
</script>
```

### Auth
```Python
# views.py
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
```
```Python
# urls.py
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
```

