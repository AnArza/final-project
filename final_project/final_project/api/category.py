from django.views.generic import View
from game.models import Category
from .helper_functions import *


class CategoryView(View):

    def get(self, request):
        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append(
                {"code": category.code, "name": category.name}
            )
        return data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        response = []
        if "code" in data and "name" in data:
            category = Category.objects.create(
                code=data["code"],
                name=data["name"]
            )
        else:
            return failed_status("invalid_post_data")
        category.save()
        response.append({"code": category.code, "name": category.name})
        return data_status(response)
