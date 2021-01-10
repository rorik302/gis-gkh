import json

from django.conf import settings
from django.shortcuts import render
from django.views import View

from home_management.forms import AddressForm
from home_management.models import House
from home_management.tasks import get_passport_url, get_passport_info


class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, "home_management/address.html",
                      {"form": form, "dadata_api_key": settings.DADATA_API_KEY})

    def post(self, request):
        suggestion = json.loads(request.POST['suggestion'])
        fias_id = suggestion['house_fias_id']
        house = House.objects.get_or_create(fias_id=fias_id)[0]

        if not house.passport_url:
            house.passport_url = get_passport_url(suggestion)
            house.save()

        if not house.passport_info and house.passport_url:
            house.passport_info = get_passport_info(house.passport_url)
            house.save()

        form = AddressForm()
        return render(request, "home_management/address.html",
                      {"form": form, "dadata_api_key": settings.DADATA_API_KEY})
