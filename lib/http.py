
import json

from django.conf import settings
from django.http import HttpResponse


def render_json(data,code=0):
    result = {
        "data":data,
        "code":code
    }

    if settings.DEBUG:
        json_str = json.dumps(result,indent=4,ensure_ascii=False,sort_keys=True)
    else:
        json_str = json.dumps(result,separators=[',',':'],ensure_ascii=False)
    return HttpResponse(json_str)

