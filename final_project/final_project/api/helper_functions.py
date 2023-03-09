import json

from django.http import JsonResponse


def data_status(data):
    return JsonResponse(
        json.dumps({"data": data, "status": "ok"}),
        status=200,
        content_type="application/json", safe=False
    )


def ok_status():
    return JsonResponse(
        json.dumps({"status": "ok"}), status=200, content_type="application/json", safe=False
    )


def failed_status(status):
    return JsonResponse(
        json.dumps({"status": status}), status=404, content_type="application/json", safe=False
    )
