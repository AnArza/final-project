from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json

from game.models import Bid, Creative, Campaign, History
from game.models import Category
from .helper_functions import *
from .optimize import betting_limit


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
            for cr in Creative.objects.all():
                if cr.width == data['imp']['banner']['w'] and cr.height == data['imp']['banner']['h']:
                    cat = []
                    for c in cr.categories.all():
                        cat.append(c.code)
                    if has_intersection(data['bcat'], cat) is False:
                        creative = cr
                        break
            if creative is None:
                for cr in Creative.objects.all():
                    cat = []
                    for c in cr.categories.all():
                        cat.append(c.code)
                    # print(data['bcat'])
                    if has_intersection(data['bcat'], cat) is False:
                        creative = cr
                        break
            # print(creative.external_id)

            bid = Bid.objects.create(
                id=data['id'],
                click_prob=float(data['click']['prob']),
                conv_prob=float(data['conv']['prob']),
                site_domain=data['site']['domain'],
                user_id=data['user']['id'],
                price=0
            )
        except KeyError:
            return failed_status("key error")
        except TypeError:
            return failed_status("type error")
        except ValueError:
            return failed_status("value error")
        bid.price = betting_limit(creative.campaign.budget, float(bid.click_prob))
        response.append({"external_id": bid.id, "price": bid.price, "image_url": creative.url, "cat": cat})
        bid.save()
        history = History.objects.create(
            click_prob=bid.click_prob,
            conv_prob=bid.conv_prob,
            budget=creative.campaign.budget,
            price=bid.price
        )
        history.save()
        return data_status(response)
