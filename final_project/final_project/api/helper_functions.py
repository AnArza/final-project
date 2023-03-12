import json

from django.http.response import HttpResponse, JsonResponse


def data_status(data):
    return HttpResponse(
        json.dumps(data),
        status=200,
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
        json.dumps({"status": "ok"}), status=200, content_type="application/json"
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