from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name

class PipelineStage(models.TextChoices):
    CONTACT = 'contact', 'Contact'
    CONSULTATION = 'consultation', 'Consultation'
    DESIGN = 'design', 'Design'
    PROPOSAL = 'proposal', 'Proposal'
    ORDER = 'order', 'Order'

class SalesPipeline(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    current_stage = models.CharField(
        max_length=20,
        choices=PipelineStage.choices,
        default=PipelineStage.CONTACT,
    )

    def __str__(self):
        return f"{self.client.name} - {self.get_current_stage_display()}"

class RoomChoices(models.TextChoices):
    LIVING_ROOM = 'living_room', 'Living Room'
    KITCHEN = 'kitchen', 'Kitchen'
    MASTER_BEDROOM = 'master_bedroom', 'Master Bedroom'
    GUEST_BEDROOM = 'guest_bedroom', 'Guest Bedroom'
    BATHROOM = 'bathroom', 'Bathroom'
    DINING_ROOM = 'dining_room', 'Dining Room'
    OFFICE = 'office', 'Office'
    GARAGE = 'garage', 'Garage'
    OTHER = 'other', 'Other'
 
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    pipeline = models.ForeignKey(SalesPipeline, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Lead(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('contacted', 'Contacted')], default='new')

    def __str__(self):
        return f"Lead from {self.campaign.name} for {self.client.name}"
    
class Product(models.Model):
    pipeline = models.ForeignKey(SalesPipeline, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    campaign = models.ForeignKey(Campaign, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=500, default="https://placeholder.url")
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    room = models.CharField(max_length=50, choices=RoomChoices.choices, default=RoomChoices.OTHER)

    def __str__(self):
        return self.name