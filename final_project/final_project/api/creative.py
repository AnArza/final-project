from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json

from game.models import Creative, Campaign
from .helper_functions import data_status, ok_status, failed_status


class CreativeView(View):

    def get(self, request):
        creatives = Creative.objects.all()
        data = []
        for creative in creatives:
            data.append({
                'external_id': creative.external_id,
                'name': creative.name,
                'campaign': {
                    'name': creative.campaign.name,
                    'budget': creative.campaign.budget
                }
            })
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        # if 'external_id' in data and 'name' in data and 'compaign_id' in data:
        #     creative = Creative.objects.create(
        #         external_id=data['external_id'],
        #         name=data['name'],
        #     )
        # else:
        #     return failed_status("invalid_post_data")
        try:
            creative = Creative.objects.create(
                external_id=data['external_id'],
                name=data['name'],
                campaign=Campaign.objects.get(id=data['campaign_id'])
            )
        except KeyError:
            return failed_status("missed parameter")
        except TypeError:
            return failed_status("wrong type")
        creative.save()
        return ok_status()

    @staticmethod
    def check_view(request, external_id):
        if request.method == "GET":
            return CreativeView.get_by_id(request, external_id)
        if request.method == "DELETE":
            return CreativeView.delete(request, external_id)
        if request.method == "PATCH":
            return CreativeView.edit(request, external_id)

    @staticmethod
    def get_by_id(request, external_id):
        try:
            creative = Creative.objects.get(external_id=external_id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        return data_status(
            {'external_id': creative.external_id, 'name': creative.name})

    @staticmethod
    def delete(request, external_id):
        try:
            creative = Creative.objects.get(external_id=external_id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        creative.delete()
        return ok_status()

    @staticmethod
    def edit(request, external_id):
        data = json.loads(request.body)
        try:
            creative = Creative.objects.get(external_id=external_id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        if 'name' in data:
            creative.name = data['name']
        if 'campaign_id' in data:
            creative.campaign = Campaign.objects.get(id=data['campaign_id'])
        creative.save()
        return ok_status()
