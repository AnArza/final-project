from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json

from game.models import Campaign
from .helper_functions import data_status, ok_status, failed_status


class CampaignView(View):

    def get(self, request):
        campaigns = Campaign.objects.all()
        data = []
        for campaign in campaigns:
            data.append({'id': campaign.id, 'name': campaign.name, 'budget': campaign.budget})
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        response = []
        if 'name' in data and 'budget' in data:
            campaign = Campaign.objects.create(
                name=data['name'],
                budget=data['budget']
            )
        else:
            return failed_status("invalid_post_data")
        campaign.save()
        response.append({'id': campaign.id, 'name': campaign.name, 'budget': campaign.budget})
        return data_status(response)

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return CampaignView.get_by_id(request, id)
        if request.method == "DELETE":
            return CampaignView.delete(request, id)
        if request.method == "PATCH":
            return CampaignView.edit(request, id)

    @staticmethod
    def get_by_id(request, id):
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        return data_status({'id': campaign.id, 'name': campaign.name, 'budget': campaign.budget})

    @staticmethod
    def delete(request, id):
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        campaign.delete()
        return ok_status()

    @staticmethod
    def edit(request, id):
        data = json.loads(request.body)
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        if 'name' in data:
            campaign.name = data['name']
        if 'budget' in data:
            campaign.budget = data['budget']
        campaign.save()
        return ok_status()
