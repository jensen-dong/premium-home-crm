from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
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