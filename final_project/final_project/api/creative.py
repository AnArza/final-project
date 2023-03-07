from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
import json

from game.models import Creative
from .helper_functions import data_status, ok_status, failed_status


class CreativeView(View):

    def get(self, request):
        creatives = Creative.objects.all()
        data = []
        for creative in creatives:
            data.append(
                {"id": creative.id, "external_id": creative.external_id, "name": creative.name}
            )
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if "external_id" in data and "name" in data:
            creative = Creative.objects.create(
                external_id=data["external_id"],
                name=data["name"],
            )
        else:
            return failed_status("invalid_post_data")
        creative.save()
        return ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return CreativeView.get_by_id(request, id)
        if request.method == "DELETE":
            return CreativeView.delete(request, id)

    @staticmethod
    def get_by_id(request, id):
        try:
            creative = Creative.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        return data_status(
            {"id": creative.id, "external_id": creative.external_id, "name": creative.name}
        )

    @staticmethod
    def delete(request, id):
        try:
            creative = Creative.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        creative.delete()
        return ok_status()
