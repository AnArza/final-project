import json
from email.mime import image
import io
import re
from PIL import Image
from django.http.response import HttpResponse, JsonResponse


# used
def data_status(data):
    return HttpResponse(
        json.dumps(data),
        status=200,
        content_type="application/json"
    )


# used
def notify_status():
    response_text = ""
    response = HttpResponse(response_text, content_type="text/plain;charset=UTF-8", status=200)
    return response


# def creative_status(url):
#     image = Image.open(request.url)
#     index = re.findall('url', request)
#     extension = request[index + 6:3]
#     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", extension)
#
#     print(extension)
#     response = HttpResponse(status=200, content_type='image/jpg')
#     image.save(response, 'JPG')
#     return response


# used
def data_status_creative_campaign(data):
    return HttpResponse(
        json.dumps(data),
        status=201,
        content_type="application/json"
    )


def data_status_post(data):
    return HttpResponse(
        json.dumps({"data": data, "status": "ok"}),
        status=201,
        content_type="application/json"
    )


def ok_status():
    return HttpResponse(
        status=200, content_type="application/json"
    )


def success_status_post():
    return HttpResponse(
        json.dumps({"status": "ok"}), status=201, content_type="application/json"
    )


def success_status_delete():
    return HttpResponse(
        json.dumps({"status": "ok"}), status=204, content_type="application/json"
    )


def failed_status(status):
    return HttpResponse(
        json.dumps({"status": status}), status=404, content_type="application/json"
    )


def has_intersection(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    return bool(set1 & set2)  # returns True if the intersection is non-empty, False otherwise


def no_bid_status(data):
    return HttpResponse(
        json.dumps({"status": "ok"}),
        status=204,
        content_type="text/plain;charset=UTF-8"
    )
