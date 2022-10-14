from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from math import ceil


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
    miscellaneous = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.miscellaneous = self.monthly_income * 0.02
        return super(Piggy, self).save(*args, **kwargs)

    
    def spare_cash(self):
        self.extra_cash = self.monthly_income - ((self.daily_expenses * 30) + self.monthly_donations
                        + self.monthly_bills + self.miscellaneous)
        if -(self.extra_cash) == abs(self.extra_cash) or self.extra_cash == 0:
            return self.extra_cash
            # I assume the person is going to have miscellaneous expense
            # which can still be put in the amount of debt that will be owed month end

        elif self.desired_item_cost > self.extra_cash:
            daily_amount = self.extra_cash/30
            self.extra_days = (self.desired_item_cost-self.extra_cash)/daily_amount
            daily_amount = round(daily_amount, 2)
            print(f"cost: {self.desired_item_cost}, extra cash: {self.extra_cash}")
            return daily_amount

        elif self.desired_item_cost <= self.extra_cash:
            daily_amount = self.desired_item_cost/30
            daily_amount = round(daily_amount, 2)
            print(f"cost: {self.desired_item_cost}, extra cash: {self.extra_cash}")
            return daily_amount
            # the person has enough money to purchase the desired item on pay check day, after he will meet all monthly needs,
            # the whole goal of the app is to ensure you save. LOL

    def num_days(self):
        if self.desired_item_cost > self.extra_cash:
            days = ceil(30 + self.extra_days)

        elif self.desired_item_cost <= self.extra_cash:
            days = 30

        return days

    

    def __str__(self):
        return self.saver.username

    
    def get_absolute_url(self):
        return reverse('savings_detail', args=[str(self.id)])