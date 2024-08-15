from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render, redirect
from datetime import datetime
from neurovart.forms import RegistrationForm, LoginForm, RequestForm, ActivationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from neurovart.models import Customers, Payments, Wallet_transactions, Payouts
from django.db.models import Sum
from neurovart.context_processors import setting
import requests
from django.urls import reverse
from django.utils.http import urlencode
from django.shortcuts import render
from neurovart.models import Payouts
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect

# Create your views here.


def loginAdmin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admindashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            admin = authenticate(request, cus_email=email, password=password)
            if admin is not None and admin.is_staff:
                login(request, admin)
                return redirect('admindashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'All inputs required!')
    else:
        form = LoginForm()
    return render(request, 'backend/login.html', {form: form})

def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'backend/index.html')
    return redirect('loginAdmin')


def logoutAdmin(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('loginAdmin')

def userList(request):
    if request.user.is_authenticated and request.user.is_staff:
        payouts = Customers.objects.all()
        return render(request, 'backend/user/userlist.html',{'payout': payouts})
    return redirect('loginAdmin')



def payout_list(request):
    payouts = Payouts.objects.all()
    # Extract customer IDs from Payouts
   # Fetch all payouts from the database
    return render(request, 'backend/user/payout_list.html', {'payouts': payouts})


def activate_payout(request, payout_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    payout = get_object_or_404(Payouts, id=payout_id)
    payout.status = 'ACCEPTED'
    payout.save()
    return redirect('payout_list')  # Redirect to the payout list or appropriate page

def deactivate_payout(request, payout_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    payout = get_object_or_404(Payouts, id=payout_id)
    payout.status = 'CANCELLED'
    payout.save()
    return redirect('payout_list')  # Redirect to the payout list or appropriate page

def pending_payout(request, payout_id):
    if not request.user.is_staff:
        return redirect('backend/login')
    payout = get_object_or_404(Payouts, id=payout_id)
    payout.status = 'PENDING'
    payout.save()
    return redirect('payout_list')  # Redirect to the payout list or appropriate page


def edit_transaction(request, payout_id):
    transaction = get_object_or_404(Payouts, pk=payout_id)
    customer = get_object_or_404(Customers, pk=transaction.cus_id)

    if request.method == 'POST':
        # Ensure only `status`, `admin_remarks`, and `transaction_id` are updated
        status = request.POST.get('status')
        admin_remarks = request.POST.get('admin_remarks')
        transaction_id = request.POST.get('transaction_id')

        # Update only the fields that are allowed to be changed
        if status:
            transaction.status = status
        if admin_remarks:
            transaction.admin_remarks = admin_remarks
        if transaction_id:
            transaction.transaction_id = transaction_id

        # Save changes
        transaction.save()

        return redirect('payout_list')  # Redirect to a detail view or another appropriate view
    else:
        # Display current values for the editable fields
        context = {
            'payout': transaction,
            'customer':customer,
        'status_choices': Payouts.STATUS_CHOICES,
            'editable_fields': {
                'status': transaction.status,
                'admin_remarks': transaction.admin_remarks,
            }
        }
        return render(request, 'backend/user/edit_payout_list.html', context)