from django.db import models
from django.core.validators import MinValueValidator


class Config(models.Model):
    impressions_total = models.IntegerField(validators=[MinValueValidator(0)])
    auction_type = models.IntegerField(validators=[MinValueValidator(0)])
    mode = models.CharField(max_length=10)
    budget = models.IntegerField()
    impression_revenue = models.IntegerField(validators=[MinValueValidator(0)])
    click_revenue = models.IntegerField(validators=[MinValueValidator(0)])
    conversion_revenue = models.IntegerField(validators=[MinValueValidator(0)])
    frequency_capping = models.IntegerField(validators=[MinValueValidator(1)])


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    budget = models.IntegerField()


class Bid(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    click_prob = models.CharField(max_length=15)
    conv_prob = models.FloatField(max_length=15)
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
    click_prob = models.CharField(max_length=15)
    conv_prob = models.FloatField(max_length=15)
    price = models.FloatField(validators=[MinValueValidator(0)])
    win = models.BooleanField(default=False)
    # clicked
    budget = models.FloatField()
