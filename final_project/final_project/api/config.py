from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from game.models import Config
from .helper_functions import ok_status, failed_status, data_status
import json


class ConfigView(View):

    def get(self, request):
        try:
            config = Config.objects.all()[0]
            data = []
            data.append(
                {"id": config.id, "impressions_total": config.impressions_total, "auction_type": config.auction_type,
                 "mode": config.mode, "budget": config.budget,
                 "impression_revenue": config.impression_revenue, "click_revenue": config.click_revenue,
                 "conversion_revenue": config.conversion_revenue, "frequency_capping": config.frequency_capping}
            )
            return data_status(data)
        except IndexError:
            return failed_status("no_config")

    def post(self, request):
        data = json.loads(request.body)
        try:
            if data['auction_type'] not in [1, 2]:
                return failed_status("auction type 1 or 2")
            if data['mode'] not in ['script', 'free']:
                return failed_status("mode is script or free")
            config = Config.objects.create(
                impressions_total=data['impressions_total'],
                auction_type=data['auction_type'],
                mode=data['mode'],
                budget=data['budget'],
                impression_revenue=data['impression_revenue'],
                click_revenue=data['click_revenue'],
                conversion_revenue=data['conversion_revenue'],
                frequency_capping=data['conversion_revenue']
            )
        except KeyError:
            return failed_status("invalid_post_data")
        except TypeError:
            return failed_status("type error happened")

        config.save()
        return ok_status()

    @staticmethod
    def delete(request):
        if request.method == "DELETE":
            try:
                config = Config.objects.all()[0]
            except ObjectDoesNotExist:
                return failed_status("object_not_found")
            config.delete()
            return ok_status()
