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
            data.append({'id': bid.id,
                         'click_prob': bid.click_prob,
                         'conv_prob': bid.conv_prob,
                         'site_domain': bid.site_domain,
                         'user_id': bid.user_id,
                         'price': str(bid.price)
                         })
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body.decode())
        try:

            bid = None

            if type(data['imp']['banner']['w']) != int or type(data['imp']['banner']['h']) != int or type(
                    data['ssp']['id']) != str or type(data['click']['prob']) != str or type(
                data['conv']['prob']) != str:
                raise TypeError

            float(data['click']['prob'])
            float(data['conv']['prob'])

            creative = None
            if 'bcat' in data:
                creatives = Creative.objects.filter(~Q(categories__code__in=data['bcat']))
                for bcat in data['bcat']:
                    if len(bcat) <= 5:
                        creatives = creatives.filter(~Q(categories__code__startswith=bcat + '-'))
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
            bid.price = betting_limit(creative.campaign.budget, bid.click_prob)

        except KeyError:
            if bid:
                bid.delete()
            return ok_status()
        except TypeError as t:
            print(t)
            if bid:
                bid.delete()
            return ok_status()
        except ValueError:
            if bid:
                bid.delete()
            return ok_status()

        history = History.objects.create(
            bid_request_id=data['id'],
            click_prob=bid.click_prob,
            conv_prob=bid.conv_prob,
            campaign=creative.campaign,
            price=bid.price
        )
        history.save()

        category = creative.categories.all()
        cats = []
        for c in category:
            cats.append(c.code)
        response = {"external_id": bid.id, "price": str(bid.price),
                    "image_url": f"http://192.168.8.208:8000{creative.url}?width={creative.width}&height={creative.height}",
                    "cat": cats}
        bid.save()
        return data_status(response)
