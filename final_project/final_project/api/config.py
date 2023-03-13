import json

from django.views.generic import View
from game.models import Config, Campaign
from final_project.api.load_categories import load_categories
from .helper_functions import ok_status, failed_status, data_status


class ConfigView(View):
    def get(self, request):
        try:
            config = Config.get_solo()
            print(config)
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
            # Campaign.objects.all().delete()
            config = Config.get_solo()
            config.impressions_total = data['impressions_total']
            config.auction_type = data['auction_type']
            config.mode = data['mode']
            config.budget = float(data['budget'])
            config.impression_revenue = data['impression_revenue']
            config.click_revenue = data['click_revenue']
            config.conversion_revenue = data['conversion_revenue']
            config.frequency_capping = data['frequency_capping']
            config.save()
            # for free mode
            for c in Campaign.objects.all():
                c.budget = config.budget // len(Campaign.objects.all())
                c.save()
            # load_categories('static/Content-Taxonomy-1.0.xlsx')
        except KeyError:
            return failed_status("invalid_post_data")
        except TypeError:
            return failed_status("type error happened")
        return ok_status()
