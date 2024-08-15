from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
        path('login', views.loginAdmin, name='loginAdmin'),
        path('logout', login_required(views.logoutAdmin, login_url='loginAdmin'), name='adminLogout'),
        path('userList', login_required(views.userList, login_url='loginAdmin'), name='userList'),
        path('dashboard', login_required(views.home, login_url='loginAdmin'), name='admindashboard'),
        path('payout_list', login_required(views.payout_list, login_url='loginAdmin'), name='payout_list'),
        path('activate-payout/<int:payout_id>/', login_required(views.activate_payout), name='activate_payout'),
        path('deactivate-payout/<int:payout_id>/', login_required(views.deactivate_payout), name='deactivate_payout'),
        path('pending-payout/<int:payout_id>/',login_required(views. pending_payout), name='pending_payout'),
        path('edit-payout/<int:payout_id>/', login_required(views.edit_transaction), name='edit_payout'),

]