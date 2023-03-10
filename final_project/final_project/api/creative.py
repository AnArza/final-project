from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json

from game.models import Creative, Campaign, Category
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
        response = []
        try:
            creative = Creative.objects.create(
                external_id=data['external_id'],
                name=data['name'],
                campaign=Campaign.objects.get(id=data['campaign']['id']),
                file=data['file']
            )
            for cat in data['categories']:
                creative.categories.add(Category.objects.get(code=cat['code']))

            response.append({
                'id': creative.id,
                'external_id': creative.external_id,
                'name': creative.name,
                'categories': [{"id": c.id, "code": c.code} for c in creative.categories.all()],
                'campaign': {
                    'id': creative.campaign.id,
                    'name': creative.campaign.name
                },
                # this is the image url that we should generate
                'url': ''

            })
        except KeyError:
            return failed_status("missed parameter")
        except TypeError:
            return failed_status("wrong type")
        creative.save()
        return data_status(response)

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
    def delete(request, id):
        try:
            creative = Creative.objects.get(id=id)
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
