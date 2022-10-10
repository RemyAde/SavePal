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
class SavingsDetailView(DetailView):
    model = Piggy
    template_name = 'savings_detail.html'
    context_object_name ="piggy"


    def get_queryset(self):
        qs = Piggy.objects.filter(saver=self.request.user)
        return qs



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


