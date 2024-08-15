from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta

#
class CustomersManager(BaseUserManager):
    def create_user(self, cus_email, password, **extra_fields):
        if not cus_email:
            raise ValueError('The Email field must be set')
        cus_email = self.normalize_email(cus_email)
        user = self.model(cus_email=cus_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cus_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cus_email, password, **extra_fields)


#
class Customers(AbstractUser):
    username = models.CharField(max_length=155, null=True, blank=True)
    cus_code = models.CharField(max_length=15)
    package_id = models.IntegerField(default=1)
    is_user = models.IntegerField(default=0)
    package_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    purchase_package = models.DateTimeField(null=True, blank=True)
    sponsor_id = models.IntegerField(null=True, blank=True)
    sponsor_code = models.CharField(max_length=15)
    level = models.IntegerField(null=True, blank=True)
    m_tree = models.TextField()
    cus_name = models.CharField(max_length=100)
    cus_wallet = models.DecimalField(default=0, max_digits=10, decimal_places=5)
    cus_mobile = models.CharField(max_length=18)
    cus_email = models.CharField(max_length=100, unique=True)
    cus_bank_name = models.CharField(max_length=100, null=True)  # Adjusted max_length
    cus_account_no = models.CharField(max_length=25, null=True)  # Adjusted max_length
    cus_ifsc = models.CharField(max_length=11, null=True)  # Adjusted max_length
    cus_image = models.CharField(max_length=255, null=True)
    cus_address = models.CharField(max_length=255, null=True)
    cus_country = models.CharField(max_length=10, null=True)
    cus_mobile_code = models.CharField(max_length=10, null=True)
    cus_status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    profile=models.FileField(upload_to='profile_pics/', blank=True, null=True)
    USERNAME_FIELD = 'cus_email'
    REQUIRED_FIELDS = []

    objects = CustomersManager()

    def __str__(self):
        return f"{self.id}"

    class Meta:
        db_table = 'customers'


class Payments(models.Model):
    cus_id = models.IntegerField()
    order_id = models.CharField(max_length=155, null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    gateway = models.CharField(max_length=50, default='CRYPTO_GATEWAY', null=True, blank=True)
    status = models.CharField(max_length=25, default='PENDING')
    response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    remark_admin = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.order_id

    class Meta:
        db_table = 'payments'


class Wallet_transactions(models.Model):
    cus_id = models.IntegerField()
    transaction_id = models.IntegerField(null=True, blank=True)
    opening = models.DecimalField(default=0, max_digits=15, decimal_places=5)
    credit = models.DecimalField(default=0, max_digits=15, decimal_places=5)
    debit = models.DecimalField(default=0, max_digits=15, decimal_places=5)
    closing = models.DecimalField(default=0, max_digits=15, decimal_places=5)
    message = models.CharField(max_length=155, null=True, blank=True)
    from_to = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        # return f"{self.cus_id}"

        return self.message

    class Meta:
        db_table = 'wallet_transactions'

class Payouts(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPT', 'Accept'),
        ('CANCEL', 'Cancel'),
    ]

    cus_id = models.IntegerField()
    request_amount = models.FloatField()
    wallet_address = models.CharField(max_length=255)
    service_charge = models.FloatField()
    charge_amount = models.FloatField(editable=False)
    final_amount = models.FloatField(editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    remarks = models.TextField(blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(null=True, blank=True,max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.charge_amount = self.request_amount * (self.service_charge / 100)
        self.final_amount = self.request_amount - self.charge_amount
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'payouts'

class ApplyForFund(models.Model):
    cus_id = models.IntegerField(blank=True)
    full_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, choices=[
        ('', '--Select--'),
        ('+1', 'United States (+1)'),
        ('+91', 'India (+91)'),
        # Add more country codes as needed
    ])
    whatsapp_no = models.CharField(max_length=15)
    email = models.EmailField()
    residential_address = models.TextField()
    investment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    risk_ratio = models.DecimalField(max_digits=5, decimal_places=2)
    id_upload = models.FileField(upload_to='uploads/')
    performance_link = models.URLField()
    terms = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class InvestmentForFund(models.Model):
    cus_id = models.IntegerField(blank=True)
    invested_at=  models.IntegerField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    last_credit_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created_at:
            self.created_at = timezone.now()
        if not self.last_credit_date:
            self.last_credit_date =  now.replace(hour=23, minute=59, second=0, microsecond=0)
        if not self.end_date:
            self.end_date = self.created_at + timedelta(days=101)
        super(InvestmentForFund, self).save(*args, **kwargs)

    class Meta:
        db_table = 'investmentforfund'

