from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json
from decimal import Decimal

from game.models import Campaign
from .helper_functions import *


class CampaignView(View):

    def get(self, request):
        campaigns = Campaign.objects.all()
        data = []
        for campaign in campaigns:
            data.append({'id': campaign.id, 'name': campaign.name, 'budget': str(campaign.budget)})
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        response = []
        if 'name' in data and 'budget' in data:
            campaign = Campaign.objects.create(
                name=data['name'],
                budget=Decimal(data['budget'])
            )
        else:
            # makes no sense
            return ok_status()
        campaign.save()
        response.append({'id': campaign.id, 'name': campaign.name, 'budget': str(campaign.budget)})
        return data_status_creative_campaign(response)

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
        return data_status({'id': campaign.id, 'name': campaign.name, 'budget': str(campaign.budget)})

    @staticmethod
    def delete(request, id):
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        campaign.delete()
        return success_status_delete()

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
