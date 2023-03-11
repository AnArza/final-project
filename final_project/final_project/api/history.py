from django.views.generic import View
import json

from game.models import Campaign, History
from .helper_functions import data_status, ok_status, failed_status


class HistoryView(View):

    def get(self, request):
        histories = History.objects.all()
        data = []
        for history in histories:
            data.append({'id': history.id, 'click_prob': history.click_prob, 'conv_prob': history.conv_prob,
                         'win': history.win, 'price': history.price, 'budget': history.budget})
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        response = []
        if 'click_prob' in data and 'conv_prob' in data and 'price' in data and 'win' in data and 'budget' in data:
            history = History.objects.create(
                click_prob=data['click_prob'],
                conv_prob=data['conv_prob'],
                price=data['price'],
                win=data['win'],
                budget=data['budget']
            )
        else:
            return failed_status("invalid_post_data")
        history.save()
        return ok_status()
