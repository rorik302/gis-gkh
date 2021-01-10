import json

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from wkhtmltopdf.views import PDFTemplateView

from home_management.forms import AddressForm
from home_management.models import House
from home_management.tasks import get_and_save_passport_url_and_info, get_and_save_passport_info


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
            get_and_save_passport_url_and_info(fias_id, suggestion)

        if house.passport_url and not house.passport_info:
            get_and_save_passport_info(fias_id, house.passport_url)

        if house.passport_info:
            return redirect('passport-pdf-view', house.fias_id)
        else:
            print('Письмо будет отправлено на указанный e-mail после формирования отчета')


class PassportPDFView(PDFTemplateView):
    template_name = 'home_management/passport_template.html'
    show_content_in_browser = True

    def get_context_data(self, **kwargs):
        fias_id = kwargs['fias_id']
        context = super(PassportPDFView, self).get_context_data(**kwargs)
        context['passport'] = json.loads(House.objects.get(fias_id=fias_id).passport_info)
        return context

