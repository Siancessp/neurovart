from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render, redirect
from decimal import Decimal
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from .forms import RegistrationForm, LoginForm,  RequestForm, ActivationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customers, Payments, Wallet_transactions, Payouts,ApplyForFund ,InvestmentForFund
from django.db.models import Sum
from .context_processors import setting
import requests
from .forms import ProfileUpdateForm, ProfilePictureForm, PasswordUpdateForm ,PasswordNewForm
from django.urls import reverse
from django.utils.http import urlencode
from django.shortcuts import render, redirect
from .forms import InvestmentForm
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

#schedulling
from decimal import Decimal
from django.utils import timezone
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.core.mail import send_mail, BadHeaderError
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import threading
from django.conf import settings
from threading import Thread
import schedule
import time
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import InvestmentForFund, Wallet_transactions, Customers
# Create your views here.
import schedule
import time
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from datetime import datetime, timedelta

def home(request):
    return render(request, 'frontend/index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('userDashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['fullname']
            email = form.cleaned_data['email'].lower()
            mobile = form.cleaned_data['mobile']
            sponsor = form.cleaned_data['sponsor'].upper()
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirmPassword']
            country_code = form.cleaned_data['country']
            dial_code = form.cleaned_data['dialCode']
            now = datetime.now()

            exist_email = Customers.objects.filter(cus_email=email).count()
            if exist_email == 0:
                exist_sponsor = Customers.objects.filter(cus_code=sponsor).count()
                if exist_sponsor == 1:
                    if password == confirm_password:
                        user = Customers.objects.create_user(cus_email=email, username=email, cus_name=name, cus_mobile=mobile,
                                                             sponsor_code=sponsor, cus_country=country_code,
                                                             cus_mobile_code=dial_code, created_at=now,
                                                             password=password,is_user=1)
                        if user:
                            # Call the stored procedure using Django's connection
                            with connection.cursor() as cursor:
                                cursor.callproc('UPDATE_MEMBER', [user.id, sponsor, sponsor, now])
                            messages.success(request, 'Customer registered successfully!')
                            return redirect('login')
                        else:
                            messages.error(request, 'Something went wrong with registration!')
                    else:
                        messages.error(request, 'Password mismatch with confirm password!')
                else:
                    messages.error(request, 'Invalid sponsor code!')
            else:
                messages.error(request, 'Email id already taken!')

            # Call the stored procedure using Django's connection
            # with connection.cursor() as cursor:
            #     cursor.callproc('ADD_MEMBER', [sponsor, sponsor, name, password, mobile, email, country_code, dial_code, now])
            #     result = cursor.fetchone()
            #     if result:
            #         if len(result) >= 3:
            #             return_id, var_message, var_member_id = result[:3]
            #             if return_id == 1:
            #                 messages.success(request, 'Customer registered successfully!')
            #                 # return redirect('/login')
            #                 return HttpResponse('User Login successfully')
            #             else:
            #                 messages.error(request, var_message)
            #         else:
            #             messages.error(request,'Unexpected response from the server!')
            #     else:
            #         messages.error(request,'Something went wrong with registration!')
        else:
            messages.error(request, 'All inputs required!')
    else:
        form = RegistrationForm()
    return render(request, 'frontend/register.html', {form: form, 'ref': request.GET.get('ref', '') })


def loginUser(request):
    if request.user.is_authenticated and  user.is_user == 1:
        return redirect('userDashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, cus_email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('userDashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'All inputs required!')
    else:
        form = LoginForm()
    return render(request, 'frontend/login.html', {form: form})


def dashboardUser(request):
    total_sponsor = Customers.objects.filter(sponsor_code=request.user.cus_code).count()
    total_active = Customers.objects.filter(sponsor_code=request.user.cus_code, package_id__gt=1).count()
    total_inactive = Customers.objects.filter(sponsor_code=request.user.cus_code, package_id=1).count()
    total_earn = Wallet_transactions.objects.filter(cus_id=request.user.id).exclude(message='ADD_FUND').aggregate(total=Sum('credit'))['total']
    total_earn = total_earn if total_earn is not None else 0.00000

    base_url = setting(request).get('BASE_URL')
    register_url = reverse('register')
    referral_params = urlencode({'ref': request.user.cus_code})
    referral_link = f"{base_url}{register_url}?{referral_params}"

    context = {
        'total_sponsor': total_sponsor,
        'total_active': total_active,
        'total_inactive': total_inactive,
        'total_earn': total_earn,
        'referral_link': referral_link
    }

    return render(request, 'frontend/user/dashboard.html', context)

def walletUser(request):
    wallets = Wallet_transactions.objects.filter(cus_id=request.user.id)
    return render(request, 'frontend/user/wallet.html', {'wallets': wallets})

def activeSponsorList(request):
    userList =  Customers.objects.filter(sponsor_code=request.user.cus_code, package_id__gt=1)
    return render(request, 'frontend/user/active-sponsor-list.html', {'userList': userList})

def inactiveSponsorList(request):
    userList =  Customers.objects.filter(sponsor_code=request.user.cus_code, package_id=1)
    return render(request, 'frontend/user/inactive-sponsor-list.html', {'userList': userList})

def activationUser(request):
    if request.method == 'POST':
        form = ActivationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
                payment = Payments.objects.create(cus_id=request.user.id, amount=amount, gateway='CRYPTO_GATEWAY',
                                                  status='PENDING')
                payment.save()
                if payment.id:
                    order_id = f"CRYPTO{payment.id}"
                    payment.order_id = order_id
                    payment.save()

                    postdata = {
                        'Username': request.user.username,
                        'userId': request.user.id,
                        'Amount': amount,
                        'Api_key': setting(request).get('APP_KEY'),
                        'order_id': order_id,
                        'redirect_url': request.build_absolute_uri(reverse('verifyUserActivation')),
                    }
                    # return redirect(reverse('verifyUserActivation') + '?' + urlencode({'clientId': order_id}))
                    url = "https://sspmitra.in/base/encrypt-decrypt/"
                    response = requests.post(url, headers={}, json=postdata)
                    if response.status_code == 201:
                        client_id = response.json().get('clientId')
                        return redirect('https://sspmitra.in/main?clientId=' + client_id)
                    else:
                        messages.error(request, 'Failed! try after some time.')
                else:
                    messages.error(request, 'Failed! try after some time.')
            except Exception as e:
                messages.error(request, f'Insert failed: {str(e)}')
        else:
            messages.error(request, 'All inputs required!')
    else:
        form = ActivationForm()
    return render(request, 'frontend/user/activation.html', {form: form})


# def verifyActivationUser(request):
#     client_id = request.GET.get('clientId')
#     if client_id:
#         url = "https://sspmitra.in/base/encrypt-decrypt/?clientId=" + client_id
#         response = requests.get(url, headers={})
#         data = response.json()
#         # if response.status_code == 200:
#         exist_payment = Payments.objects.filter(order_id=data.get('order_id'), cus_id=request.user.id, status='PENDING').count()
#         # exist_payment = Payments.objects.filter(order_id=client_id, cus_id=request.user.id, status='PENDING').count()
#         if exist_payment == 1:
#             payment = Payments.objects.filter(order_id=data.get('order_id'), cus_id=request.user.id, status='PENDING')[0]
#             # payment = Payments.objects.filter(order_id=client_id, cus_id=request.user.id, status='PENDING')[0]
#             payment.response = data
#             payment.status = 'FAILED'
#             payment.save()
#
#             if data.get('status') == True: # if 1 == 1:
#                 payment.status = 'SUCCESS'
#                 payment.save()
#
#                 amount = payment.amount
#                 Wallet_transactions.objects.create(cus_id=request.user.id, transaction_id=payment.id, opening=request.user.cus_wallet, credit=amount, debit=0, closing=request.user.cus_wallet+amount, message='ADD_FUND')
#                 Wallet_transactions.objects.create(cus_id=request.user.id, transaction_id=payment.id, opening=request.user.cus_wallet+amount, credit=0, debit=amount, closing=(request.user.cus_wallet+amount)-amount, message='ACTIVATION_ID')
#
#                 customer = Customers.objects.get(id=request.user.id)
#                 customer.package_id = 2
#                 customer.package_amount = amount
#                 customer.purchase_package = datetime.now()
#                 customer.save()
#
#                 messages.success(request, 'Id activated successfully.')
#             else:
#                 messages.error(request, 'Your last transaction was failed!')
#         else:
#             messages.error(request, 'Invalid payment!')
#     else:
#         messages.error(request, 'Something went wrong with activation!')
#     return redirect('userActivation')
def verifyActivationUser(request):
    client_id = request.GET.get('clientId')
    if client_id:
        url = "https://sspmitra.in/base/encrypt-decrypt/?clientId=" + client_id
        response = requests.get(url, headers={})
        data = response.json()
        # if response.status_code == 200:
        exist_payment = Payments.objects.filter(order_id=data.get('order_id'), cus_id=request.user.id, status='PENDING').count()
        # exist_payment = Payments.objects.filter(order_id=client_id, cus_id=request.user.id, status='PENDING').count()
        if exist_payment == 1:
            payment = Payments.objects.filter(order_id=data.get('order_id'), cus_id=request.user.id, status='PENDING')[0]
            # payment = Payments.objects.filter(order_id=client_id, cus_id=request.user.id, status='PENDING')[0]
            payment.response = data
            payment.status = 'FAILED'
            payment.save()

            if data.get('status') == True: # if 1 == 1:
                payment.status = 'SUCCESS'
                payment.save()

                amount = payment.amount
                distribute_referral_payment(request.user, amount)

                Wallet_transactions.objects.create(cus_id=request.user.id, transaction_id=payment.id, opening=request.user.cus_wallet, credit=amount, debit=0, closing=request.user.cus_wallet+amount, message='ADD_FUND')
                Wallet_transactions.objects.create(cus_id=request.user.id, transaction_id=payment.id, opening=request.user.cus_wallet+amount, credit=0, debit=amount, closing=(request.user.cus_wallet+amount)-amount, message='ACTIVATION_ID')

                customer = Customers.objects.get(id=request.user.id)
                customer.package_id = 2
                customer.package_amount = amount
                customer.purchase_package = datetime.now()
                customer.save()

                messages.success(request, 'Id activated successfully.')
            else:
                messages.error(request, 'Your last transaction was failed!')
        else:
            messages.error(request, 'Invalid payment!')
    else:
        messages.error(request, 'Something went wrong with activation!')
    return redirect('userActivation')

def distribute_referral_payment(user, total_amount):
	# Distribution percentages
	first_level_percentage = Decimal(0.50)
	referral_percentage = Decimal(0.10)  # 10% for all levels
	current_level = 1
	max_level = 100
	current_user = user

	# Distribute to the first level (50%)
	if current_user:
		referral_amount = Decimal(total_amount) * first_level_percentage
		Wallet_transactions.objects.create(
			cus_id=current_user.id,
			transaction_id=None,  # or some transaction id if applicable
			opening=current_user.cus_wallet,
			credit=referral_amount,
			debit=0,
			closing=current_user.cus_wallet + referral_amount,
			message='REFERRAL_PAYMENT_LEVEL_1'
		)
		current_user = Customers.objects.filter(cus_code=current_user.sponsor_code).first()

		current_level += 1

	# Distribute to subsequent levels (10%)
	while current_user and current_level <= max_level:
		referral_amount = Decimal(total_amount) * referral_percentage /100

		if referral_amount > 0:
			Wallet_transactions.objects.create(
				cus_id=current_user.id,
				transaction_id=None,  # or some transaction id if applicable
				opening=current_user.cus_wallet,
				credit=referral_amount,
				debit=0,
				closing=current_user.cus_wallet + referral_amount,
				message=f'REFERRAL_PAYMENT_LEVEL_{current_level}'
			)

			# Find the next referrer
			try:
				sponsor = Customers.objects.get(cus_code=current_user.sponsor_code)
				current_user = sponsor
			except Customers.DoesNotExist:
				current_user = None

			current_level += 1
		else:
			break

def logoutUser(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('login')


def create_payout(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.cus_id = request.user.id  # Set the customer ID to the current user's ID
            request_instance.service_charge = setting(request).get('SERVICE_CHARGE', 15)  # Default to 15 if not found
            request_instance.status = 'PENDING'
            request_instance.admin_remarks = None
            request_instance.charge_amount = request_instance.request_amount * (request_instance.service_charge / 100)
            request_instance.final_amount = request_instance.request_amount - request_instance.charge_amount

            # Fetch the customer's wallet
            try:
                customer = Customers.objects.get(id=request.user.id)
            except Customers.DoesNotExist:
                messages.error(request, 'Customer does not exist.')
                return render(request, 'frontend/user/create_request.html', {'form': form})

            # Check if request_amount exceeds cus_wallet
            if request_instance.request_amount > float(customer.cus_wallet):
                messages.error(request, 'Request amount cannot exceed your wallet balance.')
                return render(request, 'frontend/user/create_request.html', {'form': form})

            # Save the payout request
            request_instance.save()

            # Create a new wallet transaction
            Wallet_transactions.objects.create(
                cus_id=request.user.id,
                transaction_id=request_instance.id,  # Assuming transaction_id is the ID of the payout request
                opening=float(customer.cus_wallet),
                credit=0,
                debit=request_instance.request_amount,
                closing=float(customer.cus_wallet) - request_instance.request_amount,
                message='PAYOUT',
                from_to=request_instance.id,  # Assuming from_to is the payout request ID
            )

            # Update the customer's wallet balance
            customer.cus_wallet =float(customer.cus_wallet) - request_instance.request_amount
            customer.save()

            messages.success(request, 'Request created successfully.')
            return redirect('userDashboard')  # Replace 'userDashboard' with your actual success redirect URL
        else:
            messages.error(request, 'All inputs required and must be valid!')
    else:
        form = RequestForm()
    return render(request, 'frontend/user/create_request.html', {'form': form})

def payoutUser(request):
    payouts = Payouts.objects.filter(cus_id=request.user.id)
    return render(request, 'frontend/user/payout.html', {'payout': payouts})
# def myInvestment(request):
#     payouts = InvestmentForFund.objects.filter(cus_id=request.user.id).order_by('-id')
#     apply_for_fund = ApplyForFund.objects.filter(cus_id=request.user.id).first()
#     return render(request, 'frontend/user/myinvestment.html', {'payout': payouts, 'apply_for_fund': apply_for_fund})
def myInvestment(request):
    user_id = request.user.id

    # Fetch investments for the current user
    investments = InvestmentForFund.objects.filter(cus_id=user_id).order_by('-id')

    # Debug: Log the investments
    print(f'Investments: {[inv.id for inv in investments]}')

    # Create a dictionary to hold full names for matching invested_at
    invested_at_ids = [inv.invested_at for inv in investments]
    apply_for_fund_dict = {
        af.id: af.full_name
        for af in ApplyForFund.objects.filter(id__in=invested_at_ids)
    }

    # Debug: Log the dictionary
    print(f'apply_for_fund_dict: {apply_for_fund_dict}')

    # Attach the full name to each investment based on invested_at
    for investment in investments:
        # Use invested_at to get the full name from the dictionary
        investment.full_name = apply_for_fund_dict.get(investment.invested_at, "N/A")

        # Debug: Log each investment with its full name
        print(f'Investment ID: {investment.id}, Invested At: {investment.invested_at}, Full Name: {investment.full_name}')

    return render(request, 'frontend/user/myinvestment.html', {'payouts': investments})
# def create_investment(request):
#     if request.method == 'POST':
#         form = InvestmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     else:
#         form = InvestmentForm()
#     return render(request, 'frontend/user/applyforfund.html', {'form': form})
@login_required
def create_investment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST, request.FILES)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.cus_id = request.user.id  # Set the cus_id to the logged-in user
            investment.save()
            return redirect('/')
    else:
        form = InvestmentForm()
    return render(request, 'frontend/user/applyforfund.html', {'form': form})

def apply_fund_list(request):
    fund_applications = ApplyForFund.objects.all()
    return render(request, 'frontend/user/fund_list.html', {'fund_applications': fund_applications})


def set_investment_session(request, cus_id):
    if request.user.is_authenticated:
        request.session['investment_id'] = cus_id
    return redirect('request_investment')

# def request_investment(request):
#     if request.method == 'POST':
#         investment_amount = request.POST.get('investment_amount')
#         invested_at = request.session.get('investment_id')  # Get the ID from the session
#
#         # Server-side validation
#         try:
#             investment_amount = float(investment_amount)
#             if investment_amount < 50:
#                 raise ValidationError("The minimum investment amount is 50 rupees.")
#
#             # Check if the user is authenticated
#             if not request.user.is_authenticated:
#                 raise ValidationError("User is not authenticated.")
#
#             # Fetch or create ApplyForFund instance for the provided ID
#             apply_for_fund, created = ApplyForFund.objects.get_or_create(cus_id=invested_at)
#
#             # Save the valid investment to the database
#             investment = InvestmentForFund.objects.create(
#                 cus_id=request.user.id,  # Assign User instance to ForeignKey field
#                 invested_at=apply_for_fund.id,
#                 amount=investment_amount
#             )
#
#             # Redirect to the user dashboard
#             return redirect('userDashboard')
#         except (ValueError, ValidationError) as e:
#             error_message = str(e)
#             return render(request, 'frontend/request_investment.html',
#                           {'error_message': error_message, 'id': invested_at})
#     else:
#         invested_at = request.GET.get('id')  # Get the ID from the query parameters
#         return render(request, 'frontend/request_investment.html', {'id': invested_at})


#schedulling
# Define the task function


def distribute_sponsor_bonus(investment_amount: Decimal, cus_code: str, level=1):
    if level > 5 or not cus_code:
        return

    try:
        sponsor = Customers.objects.get(cus_code=cus_code)
        percentage = Decimal('6.00') if level == 1 else Decimal('1.00')

        bonus_amount = (investment_amount * percentage) / Decimal('100')

        opening_balance = Decimal(sponsor.cus_wallet)
        closing_balance = opening_balance + bonus_amount

        Wallet_transactions.objects.create(
            cus_id=sponsor.id,
            opening=opening_balance,
            credit=bonus_amount,
            debit=0,
            closing=closing_balance,
            message="SPONSOR INVESTMENT",
            level=level,
            from_to=sponsor.id
        )

        sponsor.cus_wallet = closing_balance
        sponsor.save()

        # Recursive call for the next level sponsor
        distribute_sponsor_bonus(investment_amount, sponsor.sponsor_code, level + 1)
    except ObjectDoesNotExist:
        print(f"Customer with cus_code {cus_code} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
#

# def distribute_sponsor_bonus(request):
#     return 0
def run_process_investments():
    now = timezone.now()
    logger.info(f"Running process_investments at {now}")
    investments = InvestmentForFund.objects.all()

    for investment in investments:
        try:
            process_investment_credit(investment, now)
        except Exception as e:
            logger.error(f"Error processing investment {investment.id}: {e}")


def process_investment_credit(investment, now):
    try:
        customer = Customers.objects.get(id=investment.cus_id)
        logger.info(f"Processing investment_id {investment.id} for customer_id {customer.id}.")

        # Check if today's date is before the end_date
        if investment.end_date and now > investment.end_date:
            logger.info(f"End date has passed for investment_id {investment.id}. No further credits.")
            return

        # Check if last_credit_date is not today
        if investment.last_credit_date is None or investment.last_credit_date.date() != now.date():
            opening_balance = Decimal(customer.cus_wallet)
            credit_amount = (investment.amount * Decimal('2.00')) / Decimal('100')
            closing_balance = opening_balance + Decimal(credit_amount)

            # Create a Wallet_transactions record
            Wallet_transactions.objects.create(
                cus_id=customer.id,
                transaction_id=investment.id,
                opening=opening_balance,
                credit=Decimal(credit_amount),
                closing=closing_balance,
                message="RETURN INVESTMENT",
                from_to=investment.invested_at
            )

            # Update last_credit_date
            investment.last_credit_date = now
            investment.save()
            logger.info(f"Processed credit for investment_id {investment.id}. New balance: {closing_balance}.")
        else:
            logger.info(f"Credit already processed for today for investment_id {investment.id}.")
    except Customers.DoesNotExist:
        logger.error(f"Customer with id {investment.cus_id} does not exist.")
    except Exception as e:
        logger.error(f"Error processing credit for investment_id {investment.id}: {e}")


def schedule_tasks():
    logger.info("Starting scheduler...")
    schedule.every().minute.do(run_process_investments)

    while True:
        schedule.run_pending()
        time.sleep(1)




# Start scheduling tasks in a separate thread
scheduler_thread = threading.Thread(target=schedule_tasks)
scheduler_thread.daemon = True
scheduler_thread.start()
logger.info("Scheduler thread started.")

def request_investment(request):
    if request.method == 'POST':
        investment_amount_str = request.POST.get('investment_amount')
        invested_at = request.session.get('investment_id')

        try:
            # Convert investment_amount to Decimal
            investment_amount = Decimal(investment_amount_str)
            if investment_amount < Decimal('5.00'):
                raise ValidationError("The minimum investment amount is 5 USDT.")

            if not request.user.is_authenticated:
                raise ValidationError("User is not authenticated.")

            # Ensure ApplyForFund exists or is created
            apply_for_fund, created = ApplyForFund.objects.get_or_create(cus_id=invested_at)

            # Create investment record
            investment = InvestmentForFund.objects.create(
                cus_id=request.user.id,
                invested_at=apply_for_fund.id,
                amount=investment_amount
            )
            print(f"Investment created: {investment.id}")

            # Calculate credit amount and schedule tasks
            credit_amount = (investment_amount * Decimal('2.00')) / Decimal('100')
            # schedule_credit_tasks(investment.id, request.user.id, credit_amount)

            # Distribute sponsor bonuses
            sponsor_code = request.user.sponsor_code
            if sponsor_code:
                distribute_sponsor_bonus(investment_amount, sponsor_code)

            return redirect('userDashboard')
        except (ValueError, ValidationError) as e:
            error_message = str(e)
            return render(request, 'frontend/request_investment.html',
                          {'error_message': error_message, 'id': invested_at})
    else:
        invested_at = request.session.get('investment_id')
        if not invested_at:
            invested_at = request.GET.get('id')
            request.session['investment_id'] = invested_at
        return render(request, 'frontend/request_investment.html', {'id': invested_at})
@login_required
def set_investment_session(request, cus_id):
    request.session['investment_id'] = cus_id
    return redirect('request_investment')


# Schedule process_investments to run every day
# schedule.every().day.at("22:32").do(process_investments)
# execution_count = {}
#
# def credit_wallet(investment_id, customer_id, credit_amount):
#     print(f"credit_wallet called for investment_id: {investment_id}, customer_id: {customer_id} with amount: {credit_amount}")
#     if investment_id not in execution_count:
#         execution_count[investment_id] = 0
#
#     if execution_count[investment_id] < 5:
#         try:
#             customer = Customers.objects.get(id=customer_id)
#             opening_balance = Decimal(customer.cus_wallet)
#             closing_balance = opening_balance + Decimal(credit_amount)
#
#             # Create a Wallet_transactions record
#             Wallet_transactions.objects.create(
#                 cus_id=customer.id,
#                 opening=opening_balance,
#                 transaction_id=investment_id,
#                 credit=Decimal(credit_amount),
#                 closing=closing_balance,
#                 message="RETURN INVESTMENT",
#                 from_to=customer.id
#             )
#             print(f"Wallet transaction created: Opening balance: {opening_balance}, Credit: {credit_amount}, Closing balance: {closing_balance}")
#
#
#             # Update the customer's wallet balance
#             customer.cus_wallet = closing_balance
#             customer.save()
#             print(f"Customer wallet updated: {customer.cus_wallet}")
#
#             # Increment the execution count
#             execution_count[investment_id] += 1
#
#         except Customers.DoesNotExist:
#             print(f"Customer with id {customer_id} does not exist.")
#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#
#     # Stop scheduling after 5 executions
#     if execution_count[investment_id] >= 5:
#         schedule.clear(f"task_{investment_id}")
#         print(f"Task for investment_id {investment_id} completed and cleared from schedule.")
#
#
# def schedule_credit_tasks(investment_id, customer_id, credit_amount):
#     print(
#         f"Scheduling credit_wallet tasks for investment_id: {investment_id}, customer_id: {customer_id} with amount: {credit_amount}")
#
#     # Initialize execution count
#     execution_count[investment_id] = 0
#
#     # Schedule the task to run daily at 9:30 PM
#     schedule.every(1).minute.do(credit_wallet, investment_id=investment_id, customer_id=customer_id,
#                                         credit_amount=credit_amount).tag(f"task_{investment_id}")
#     print(f"Task scheduled to run daily at 21:30 for investment_id: {investment_id}, customer_id: {customer_id}")
#
#
# def process_investments():
#     now = make_aware(datetime.now())
#     investments = InvestmentForFund.objects.filter(created_at__date=now.date())
#
#     print(f"Processing investments for {now.date()}. Found {len(investments)} investments.")
#     for investment in investments:
#         investment_id = investment.id
#         customer_id = investment.cus_id
#         amount = Decimal(investment.amount)
#         credit_amount = (amount * Decimal('2')) / Decimal('100')
#
#         # Schedule credit wallet tasks for the investment
#         schedule_credit_tasks(investment_id, customer_id, credit_amount)
#
# def run_scheduler():
#     print("Scheduler is running.")
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
# def start_scheduling():
#     scheduler_thread = Thread(target=run_scheduler)
#     scheduler_thread.daemon = True
#     scheduler_thread.start()
#     print("Scheduler thread started.")
#
# # Start the scheduler
# start_scheduling()
#
# @login_required
# def request_investment(request):
#     if request.method == 'POST':
#         investment_amount = request.POST.get('investment_amount')
#         invested_at = request.session.get('investment_id')
#
#         try:
#             investment_amount = float(investment_amount)
#             if investment_amount < 50:
#                 raise ValidationError("The minimum investment amount is 50 rupees.")
#
#             apply_for_fund, created = ApplyForFund.objects.get_or_create(cus_id=invested_at)
#             if not request.user.is_authenticated:
#                 raise ValidationError("User is not authenticated.")
#
#             investment = InvestmentForFund.objects.create(
#                 cus_id=request.user.id,
#                 invested_at=apply_for_fund.id,
#                 amount=investment_amount
#             )
#             print(f"Investment created: {investment.id}")
#
#             # Schedule investments
#             credit_amount = (Decimal(investment_amount) * Decimal('2')) / Decimal('100')
#             schedule_credit_tasks(investment.id, request.user.id, credit_amount)
#
#             return redirect('userDashboard')
#         except (ValueError, ValidationError) as e:
#             error_message = str(e)
#             return render(request, 'frontend/request_investment.html',
#                           {'error_message': error_message, 'id': invested_at})
#     else:
#         invested_at = request.session.get('investment_id')
#         if not invested_at:
#             invested_at = request.GET.get('id')
#             request.session['investment_id'] = invested_at
#         return render(request, 'frontend/request_investment.html', {'id': invested_at})
#
# @login_required
# def set_investment_session(request, cus_id):
#     request.session['investment_id'] = cus_id
#     return redirect('request_investment')
#
# # # Schedule process_investments to run every day
# schedule.every().day.at("00:00").do(process_investments)
@login_required
def profile(request):
    profile_form = ProfileUpdateForm(instance=request.user)
    picture_form = ProfilePictureForm(instance=request.user)
    password_form = PasswordUpdateForm(request.user)

    return render(request, 'frontend/user/profile.html', {
        'profile_form': profile_form,
        'picture_form': picture_form,
        'password_form': password_form
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
        else:
            messages.error(request, 'Error updating your profile')
    return redirect('profile')

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if picture_form.is_valid():
            picture_form.save()
            messages.success(request, 'Your profile picture has been updated!')
        else:
            messages.error(request, 'Error updating your profile picture')
    return redirect('profile')


@login_required
def update_password(request):
    if request.method == 'POST':
        password_form = PasswordUpdateForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated!')
            return redirect('profile')
        else:
            for field, errors in password_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        password_form = PasswordUpdateForm(request.user)

    return render(request, 'frontend/user/profile.html', {'password_form': password_form})


def enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the email exists in the CustomUser model
        user = Customers.objects.filter(cus_email=email).first()
        if user:
            otp = get_random_string(length=6, allowed_chars='0123456789')
            request.session['otp'] = otp
            request.session['email'] = email

            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    settings.EMAIL_HOST_USER,  # Use EMAIL_HOST_USER from settings
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent to your email.')
                return redirect('enter_otp')
            except BadHeaderError:
                messages.error(request, 'Invalid header found.')
            except ConnectionRefusedError:
                messages.error(request, 'Failed to connect to the email server.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
        else:
            messages.error(request, 'Email does not exist.')

    return render(request, 'frontend/enteremail.html')
def enter_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')
        if otp == request.session.get('otp'):
            request.session['verified_email'] = email
            return redirect('change_password')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'frontend/enterotp.html')


def change_password(request):
    # Fetch the email from the session
    email = request.session.get('verified_email')

    if not email:
        messages.error(request, 'Email is not verified. Please request an OTP.')
        return redirect('enter_email')

    user = Customers.objects.filter(cus_email=email).first()

    if not user:
        messages.error(request, 'User not found.')
        return redirect('enter_email')

    if request.method == 'POST':
        form = PasswordNewForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordNewForm(user)

    return render(request, 'frontend/change_password.html', {'form': form})
def my_fund_applications_view(request):
    cus_id = request.user.id  # Assuming `request.user` is the logged-in customer
    my_fund_applications = ApplyForFund.objects.filter(cus_id=cus_id)

    context = {
        'my_fund_applications': my_fund_applications,
    }

    return render(request, 'frontend/user/my_fund_applications.html', context)

# View for investments made in you
def investments_in_me_view(request):
    cus_id = request.user.id  # The logged-in customer's ID
    # Get the ApplyForFund instances where the logged-in user is the cus_id
    my_funds = ApplyForFund.objects.filter(cus_id=cus_id)
    # Get the investments where the invested_at matches any of the ApplyForFund IDs
    investments_in_me = InvestmentForFund.objects.filter(invested_at__in=my_funds.values_list('id', flat=True))

    context = {
        'investments_in_me': investments_in_me,
    }

    return render(request, 'frontend/user/investments_in_me.html', context)