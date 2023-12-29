from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=255,unique=True,null=False)
    address = models.CharField(max_length=255,unique=True,null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    tokens = models.ManyToManyField('Token', related_name='wallets')
    time_created = models.DateTimeField(default=timezone.now)
    
    # Add other fields as needed

    def __str__(self):
        return f"{self.name}'s Wallet"

class Token(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    token_name = models.CharField(max_length=255,unique=False,null=False)
    token_address = models.CharField(max_length=255,unique=False,null=False)
    token_initial_price = models.DecimalField(max_digits=40,default=0,null=True, decimal_places=10)
    quantity = models.DecimalField(max_digits=64, decimal_places=6)
    currency = models.CharField(max_length=255 ,null=True)
    time_created = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['wallet', 'token_address'], name='unique_token')
        ]


    def __str__(self):
        return f"{self.token_name} in {self.wallet.name}'s Wallet"


# ethereum_webhook/models.py
from django.db import models

class EthereumTransaction(models.Model):
    transaction_hash = models.CharField(max_length=66, unique=True)
    from_address = models.CharField(max_length=42)
    to_address = models.CharField(max_length=42)
    value = models.DecimalField(max_digits=30, decimal_places=18)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_hash
