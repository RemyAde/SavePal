from django.urls import path
from .views import (HomePageView, SavingsCreateView, 
                   SavingsUpdateView, SavingsListView,
                   SavingsDeleteView, SavingsDetailView)


urlpatterns =  [
    path('', HomePageView.as_view(), name='home'),
    path('piggy/', SavingsListView.as_view(), name='savings_list'),
    path('new/', SavingsCreateView.as_view(), name='savings_new'),
    path('piggy/<int:pk>/', SavingsDetailView.as_view(), name='savings_detail'),
    path('piggy/<int:pk>/edit/', SavingsUpdateView.as_view(), name='savings_edit'),
    path('piggy/<int:pk>/delete/', SavingsDeleteView.as_view(), name='savings_delete')
]