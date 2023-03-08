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


class Creative(models.Model):
    external_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)


class Bid(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    # imp_banner_w = models.IntegerField(validators=[MinValueValidator(0)])
    # imp_banner_h = models.IntegerField(validators=[MinValueValidator(0)])
    click_prob = models.CharField(max_length=15)
    conv_prob = models.FloatField(max_length=15)
    site_domain = models.CharField(max_length=100)
    ssp_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    # external_id = models.CharField(max_length=100, primary_key=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    # image_url = models.TextField()


class Category(models.Model):
    code = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)
    creative = models.ForeignKey(Creative, on_delete=models.CASCADE)
    # bid = models.ForeignKey(Bid, on_delete=models.CASCADE)  i guess we don't need this one
