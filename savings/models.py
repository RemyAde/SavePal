from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your models here.
class Piggy(models.Model):
    saver = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)
    monthly_income = models.FloatField(null=True, blank=True)
    desired_item = models.CharField(max_length=200, blank=True)
    desired_item_cost = models.FloatField(null=True, blank=True)
    daily_expenses = models.FloatField(null=True, blank=True)
    monthly_donations = models.FloatField(null=True, blank=True) 
    monthly_bills = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.saver.username

    
    def get_absolute_url(self):
        return reverse('savings_detail', args=[str(self.id)])