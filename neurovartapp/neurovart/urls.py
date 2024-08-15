from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('login', views.loginUser, name='login'),
    path('register', views.register, name='register'),
    path('set_investment_session/<int:cus_id>/', login_required(views.set_investment_session), name='set_investment_session'),
    path('dashboard', login_required(views.dashboardUser, login_url='login'), name='userDashboard'),
    path('activation', login_required(views.activationUser, login_url='login'), name='userActivation'),
    path('wallet', login_required(views.walletUser, login_url='login'), name='userWallet'),
    path('active-sponsor-list', login_required(views.activeSponsorList, login_url='login'), name='activeSponsorList'),
    path('inactive-sponsor-list', login_required(views.inactiveSponsorList, login_url='login'), name='inactiveSponsorList'),
    path('verify-activation', login_required(views.verifyActivationUser, login_url='login'), name='verifyUserActivation'),
    path('logout', login_required(views.logoutUser, login_url='login'), name='userLogout'),
    path('create_payout', login_required(views.create_payout, login_url='login'), name='create_payout'),
    path('payoutlist', login_required(views.payoutUser, login_url='login'), name='payoutlist'),
    path('investments', login_required(views.myInvestment, login_url='login'), name='myInvestment'),
    path('create-investment', login_required(views.create_investment, login_url='login'), name='create_investment'),
    path('apply_fund_list', login_required(views.apply_fund_list, login_url='login'), name='apply_fund_list'),
    path('request_investment', login_required(views.request_investment, login_url='login'), name='request_investment'),
    path('profile/', login_required(views.profile, login_url='login'), name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/update_password/', views.update_password, name='update_password'),
    path('enter-email/', views.enter_email, name='enter_email'),
    path('enter-otp/', views.enter_otp, name='enter_otp'),
    path('change-password/', views.change_password, name='change_password'),
    path('my-fund-applications/', login_required(views.my_fund_applications_view, login_url='login'), name='my_fund_applications'),
    path('investments-in-me/', login_required(views.investments_in_me_view, login_url='login'), name='investments_in_me'),

]