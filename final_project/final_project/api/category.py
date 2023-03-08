import json

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from game.models import Category, Creative
from .helper_functions import *


class CategoryView(View):

    def get(self, request):
        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append(
                (
                    {"code": category.code, "name": category.name, "creative": category.creative.name}
                )
            )
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if "code" in data and "name" in data and "creative" in data:
            category = Category.objects.create(
                code=data["code"],
                name=data["name"],
                creative=Creative.objects.get(id=data["creative"])
            )
        else:
            return failed_status("invalid_post_data")
        category.save()
        return ok_status()

    @staticmethod
    def check_view(request, code):
        if request.method == "GET":
            return CategoryView.get_single(request, code)
        if request.method == "DELETE":
            return CategoryView.delete(request, code)
        # if request.method == "PATCH":
        #     return edit(request, id)

    @staticmethod
    def get_single(request, code):
        try:
            category = Category.objects.get(code=code)
        except ObjectDoesNotExist:
            return failed_status("object_not_found")
        return data_status(
            {"code": category.code, "name": category.name, 'creative': category.creative.name}
        )

    @staticmethod
    def delete(request, code):
        try:
            category = Category.objects.get(code=code)
        except ObjectDoesNotExist:
            return failed_status("object_not_found")
        category.delete()
        return ok_status()