from django import forms


class AddressForm(forms.Form):
    raw_address = forms.CharField(label=False, required=False)
    suggestion = forms.CharField(label=False, widget=forms.Textarea(attrs={"hidden": True}))
