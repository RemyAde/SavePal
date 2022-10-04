from math import ceil
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from .models import Piggy


class HomePageView(TemplateView):
    template_name = "home.html"


## CRUD

# CREATE
class SavingsCreateView(LoginRequiredMixin, CreateView):
    model = Piggy
    template_name = 'savings_new.html'
    fields = ['monthly_income', 'desired_item', 'desired_item_cost', 'daily_expenses',
                'monthly_donations', 'monthly_bills']


    def form_valid(self, form):
        form.instance.saver = self.request.user
        return super(SavingsCreateView, self).form_valid(form)



#RETRIEVE
@login_required
def view_savings(request, piggy_pk):
    piggy = get_object_or_404(Piggy, pk=piggy_pk)

    if request.method == "GET":
        piggy = get_object_or_404(Piggy, pk=piggy_pk, saver=request.user)
        miscellaneous = piggy.monthly_income * 0.02
        spare_cash = piggy.monthly_income - ((piggy.daily_expenses * 30) + piggy.monthly_donations + piggy.monthly_bills + miscellaneous)
        
        if -(spare_cash) == abs(spare_cash):
            error = "Oops. You don't have enough spare cash to save, why not review your expenses and see what you can do without. xx"
            return render(request, "savings_detail.html", {"piggy":piggy, "spare_cash":abs(spare_cash), "error":error})

        elif piggy.desired_item_cost > spare_cash:
            daily_amount = spare_cash/30
            extra_days = (piggy.desired_item_cost-spare_cash)/daily_amount
            num_saving_days = ceil(30 + extra_days)
            daily_amount = round(daily_amount, 2)
            return render(request, 'savings_detail.html', {"piggy":piggy,'spare_cash':daily_amount, 'days':num_saving_days})

        elif piggy.desired_item_cost <= spare_cash:
            daily_amount = piggy.desired_item_cost/30
            daily_amount = round(daily_amount, 2)
            num_saving_days = 30
            return render(request, 'savings_detail.html', {"piggy":piggy, 'spare_cash':daily_amount, 'days':num_saving_days})

        # else:
        #     num_saving_days = piggy.desired_item_cost/spare_cash
        #     num_saving_days = ceil(num_saving_days)
        #     return render(request, "savings_detail.html", {"piggy":piggy, "spare_cash":spare_cash, "days":num_saving_days})
        



# class SavingsDetailView(DetailView):
#     model = Piggy
#     template_name = 'savings_detail.html'


#     def get_queryset(self):
#         qs = Piggy.objects.filter(saver=self.request.user)
#         return qs



#UPDATE
class SavingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Piggy
    template_name = "savings_edit.html"
    fields = ['monthly_income', 'desired_item', 'desired_item_cost', 'daily_expenses', 'monthly_donations', 'monthly_bills']


    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.saver != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)



#DELETE
class SavingsDeleteView(LoginRequiredMixin, DeleteView):
    model = Piggy
    template_name = 'savings_delete.html'
    success_url = reverse_lazy('savings_list')


    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.saver != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)



class SavingsListView(LoginRequiredMixin, ListView):
    model = Piggy
    template_name = "savings_list.html"


    def get_queryset(self):
        qs = Piggy.objects.filter(saver=self.request.user)
        return qs


