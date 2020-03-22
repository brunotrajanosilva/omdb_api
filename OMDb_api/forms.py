from django import forms
import datetime


def year_choices():
    year_choices = [(r,r) for r in range(1900, datetime.date.today().year+1)]
    year_choices.append( ('', '----' ) )
    year_choices.reverse()
    return year_choices


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100,
    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'size': 15}) )

    year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial="'----'",
    empty_value=None, required=False,
    widget=forms.Select(attrs={'class': 'custom-select mb-3'}) )