import json

from django.http.response import HttpResponse, JsonResponse


def data_status(data):
    return JsonResponse(
        json.dumps({"data": data, "status": "ok"}),
        status=200,
        content_type="application/json", safe=False
    )

def data_status_post(data):
    return JsonResponse(
        json.dumps({"data": data, "status": "ok"}),
        status=201,
        content_type="application/json", safe=False
    )

def ok_status():
    return JsonResponse(
        json.dumps({"status": "ok"}), status=200, content_type="application/json", safe=False
    )

def success_status_post():
    return JsonResponse(
        json.dumps({"status": "ok"}), status=201, content_type="application/json", safe=False
    )

def success_status_delete():
    return JsonResponse(
        json.dumps({"status": "ok"}), status=204, content_type="application/json", safe=False
    )

def failed_status(status):
    return JsonResponse(
        json.dumps({"status": status}), status=404, content_type="application/json", safe=False
    )


def has_intersection(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    return bool(set1 & set2)  # returns True if the intersection is non-empty, False otherwise
