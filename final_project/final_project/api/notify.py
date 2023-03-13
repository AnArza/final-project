from django.views.generic import View
from .helper_functions import *
from game.models import History
from django.core.exceptions import ObjectDoesNotExist


class NotifyView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            id = data['id']
            if type(id) != str:
                raise TypeError
            win = data['win']
            if type(win) != bool:
                raise TypeError
            price = data['price']
            if type(price) != float:
                raise TypeError
            click = data['click']
            if type(click) != bool:
                raise TypeError
            conversion = data['conversion']
            if type(conversion) != bool:
                raise TypeError
            revenue = data['revenue']
            if type(revenue) != float:
                raise TypeError

        except KeyError:
            return failed_status("missed parameter")
        except TypeError:
            return failed_status("wrong type")
        try:
            history = History.objects.get(bid_request_id=data['id'])
            history.win = win
            if win:
                history.campaign.budget -= price
                history.revenue += data['revenue']
                history.campaign.save()
            history.save()
        except ObjectDoesNotExist:
            return failed_status("does not exist")
        return notify_status()
