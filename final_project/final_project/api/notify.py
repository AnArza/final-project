from django.views.generic import View
from .helper_functions import *
from game.models import History
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal


class NotifyView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        print(type(data))
        try:
            id = data['id']
            # if type(id) != str:
            #     raise TypeError
            win = data['win']
            # if type(win) != bool:
            #     raise TypeError
            if win:
                price = Decimal(data['price'])
                # if type(price) != float:
                #     raise TypeError
                click = data['click']
                # if type(click) != bool:
                #     raise TypeError
                conversion = data['conversion']
                # if type(conversion) != bool:
                #     raise TypeError
                revenue = data['revenue']
                # if type(revenue) != float:
                #     raise TypeError

        except KeyError:
            # should we return ok status here?
            return failed_status("missed parameter")
        # except TypeError as d:
        #     # should we return ok status here?
        #     print(d, "*******************")
        #     return failed_status("wrong type")
        try:
            history = None
            history = History.objects.get(bid_request_id=data['id'])
            history.win = win
            if win:
                history.campaign.budget -= price
                history.revenue += data['revenue']
                history.campaign.save()
            history.save()
        except ObjectDoesNotExist:
            return ok_status()
        except TypeError:
            if history:
                history.delete()
            return ok_status()
        return notify_status()
