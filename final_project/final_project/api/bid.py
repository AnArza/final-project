from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json

from game.models import Bid, Creative
from game.models import Category
from .helper_functions import data_status, ok_status, failed_status


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
        image_url = 'temporary_eshutyun.jpg'  # creative serving zibil service
        try:
            float(data['click']['prob'])
            float(data['conv']['prob'])
            if type(data['id']) != str or type(data['click']['prob']) != str or type(
                    data['conv']['prob']) != str or type(data['imp']['banner']['w']) != int or type(
                data['imp']['banner']['h']) != int or type(data['site']['domain']) != str or type(
                data['ssp']['id']) != str or type(
                data['user']['id']) != str:
                raise TypeError
            # we gotta generate these categories of creatives
            # by making sure that they are not in the blocked categories
            cat = []
            for creative in Creative.objects.all():
                pass
            bid = Bid.objects.create(
                id=data['id'],
                click_prob=data['click']['prob'],
                conv_prob=data['conv']['prob'],
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
        # also not sure about external id
        # optimize price
        bid.price = 5
        response.append({"external_id": bid.id, "price": bid.price, "image_url": image_url, "cat": cat})
        bid.save()
        return data_status(response)
