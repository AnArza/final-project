from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json

from game.models import Bid, Creative, Campaign, History, Config
from game.models import Category
from .helper_functions import *
from .optimize import betting_limit
from django.db.models import Q


class BidView(View):

    def get(self, request):
        bids = Bid.objects.all()
        data = []
        for bid in bids:
            # categories = Category.objects.filter(bid_id=bid.id)
            data.append({'id': bid.id,
                         # 'external_id': bid.external_id,
                         'click_prob': bid.click_prob,
                         'conv_prob': bid.conv_prob,
                         'site_domain': bid.site_domain,
                         'user_id': bid.user_id,
                         'price': bid.price
                         })
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        response = []
        try:
            categories = Category.objects.all()

            if type(data['imp']['banner']['w']) != int or type(data['imp']['banner']['h']) != int or type(
                    data['ssp']['id']) != str or type(data['click']['prob']) != str or type(
                data['conv']['prob']) != str:
                raise TypeError("wrong type")

            float(data['click']['prob'])
            float(data['conv']['prob'])

            creative = None
            if 'bcat' in data:
                creatives = Creative.objects.filter(~Q(categories__code__in=data['bcat']))
            else:
                creatives = Creative.objects.all()
            for cr in creatives:
                if cr.width == data['imp']['banner']['w'] and cr.height == data['imp']['banner']['h']:
                    creative = cr
                    break
            if not creative:
                creative = creatives.first()

            bid = Bid.objects.create(
                id=data['id'],
                click_prob=float(data['click']['prob']),
                conv_prob=float(data['conv']['prob']),
                site_domain=data['site']['domain'],
                user_id=data['user']['id'],
                price=0
            )
        except KeyError:
            if bid:
                bid.delete()
            return failed_status("key error")
        except TypeError:
            if bid:
                bid.delete()
            return failed_status("type error")
        except ValueError:
            if bid:
                bid.delete()
            return failed_status("value error")
        history = History.objects.create(
            bid_request_id=data['id'],
            click_prob=bid.click_prob,
            conv_prob=bid.conv_prob,
            campaign=creative.campaign,
            price=bid.price
        )
        history.save()
        bid.price = betting_limit(creative.campaign.budget, bid.click_prob)
        category = creative.categories.all()
        cats = []
        for c in category:
            cats.append(c.code)
        response.append(
            {"external_id": bid.id, "price": bid.price,
             "image_url": f"http://127.0.0.1:8000{creative.url}?width={creative.width}&height={creative.height}",
             "cat": cats})
        bid.save()
        return data_status(response)
