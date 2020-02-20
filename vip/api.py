from django.shortcuts import render

# Create your views here.
from lib.http import render_json
from vip.models import Vip


def show_vip_permissions(request):
    '''查看vip所有权限详情'''
    vip_permissions = list()    # 所有vip的所有权限列表
    for vip in Vip.objects.filter(level__gte=1):
        vip_info = vip.to_dict()

        perm_list = list()
        for perm in vip.permissions():
            perm_list.append(perm.to_dict())

        vip_info['perm_info'] = perm_list

        vip_permissions.append(vip_info)

    return render_json(vip_permissions)

