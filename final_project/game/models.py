from django.db import models
from django.core.validators import MinValueValidator
from solo.models import SingletonModel


class Config(SingletonModel):
    impressions_total = models.PositiveIntegerField(null=True)
    auction_type = models.PositiveIntegerField(null=True)
    mode = models.CharField(max_length=10, null=True)
    budget = models.FloatField(null=True)
    impression_revenue = models.PositiveIntegerField(null=True)
    click_revenue = models.PositiveIntegerField(null=True)
    conversion_revenue = models.PositiveIntegerField(null=True)
    frequency_capping = models.IntegerField(validators=[MinValueValidator(1)], null=True)


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    budget = models.FloatField(validators=[MinValueValidator(0)], null=True)


class Bid(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    click_prob = models.FloatField()
    conv_prob = models.FloatField()
    site_domain = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    price = models.FloatField(validators=[MinValueValidator(0)])


class Category(models.Model):
    code = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=100)


class Creative(models.Model):
    id = models.AutoField(primary_key=True)
    external_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    file = models.ImageField()
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    url = models.URLField()
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)


class History(models.Model):
    bid_request_id = models.CharField(max_length=100)
    click_prob = models.FloatField()
    conv_prob = models.FloatField()
    price = models.FloatField(validators=[MinValueValidator(0)])
    win = models.BooleanField(default=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    revenue = models.FloatField(default=0)
    current_round = models.PositiveIntegerField(default=0)
