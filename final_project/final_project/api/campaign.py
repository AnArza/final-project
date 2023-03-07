from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json

from app.models import Campaign
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
        if 'name' in data and 'budget' in data:
            campaign = Campaign.objects.create(
                name=data['name'],
                budget=data['budget']
            )
        else:
            return failed_status("invalid_post_data")
        campaign.save()
        return ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return CampaignView.get_by_id(request, id)
        if request.method == "DELETE":
            return CampaignView.delete(request, id)

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