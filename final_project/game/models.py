from django.db import models
from django.core.validators import MinValueValidator


class Config(models.Model):
    impressions_total = models.PositiveIntegerField()
    auction_type = models.PositiveIntegerField()
    mode = models.CharField(max_length=10)
    budget = models.IntegerField()
    impression_revenue = models.PositiveIntegerField()
    click_revenue = models.PositiveIntegerField()
    conversion_revenue = models.PositiveIntegerField()
    frequency_capping = models.IntegerField(validators=[MinValueValidator(1)])


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    budget = models.PositiveIntegerField()


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
    click_prob = models.FloatField()
    conv_prob = models.FloatField()
    price = models.FloatField(validators=[MinValueValidator(0)])
    win = models.BooleanField(default=False)
    budget = models.FloatField()
