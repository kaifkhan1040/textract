from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser,Country,DocumentSetModel, \
    CustomerDocumentModel
from django.forms import EmailInput
from django.forms import ModelForm, TextInput, EmailInput, CharField, PasswordInput, ChoiceField, BooleanField, \
    NumberInput, DateInput
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit


signup_as_choices = (
    ('T', 'tenat'),
    ('L', 'Landload')
)

country_choices =(
("","Select Country"),
("Australia","Australia"),
("Bangladesh","Bangladesh"),
("Belarus","Belarus"),
("Brazil","Brazil"),
("Canada","Canada"),
("China","China"),
("France","France"),
("Germany","Germany"),
("India","India"),
("Indonesia","Indonesia"),
("Israel","Israel"),
("Italy","Italy"),
("Japan","Japan"),
("Korea","Korea, Republic of"),
("Mexico","Mexico"),
("Philippines","Philippines"),
("Russia","Russian Federation"),
("South Africa","South Africa"),
("Thailand","Thailand"),
("Turkey","Turkey"),
("Ukraine","Ukraine"),
("United Arab Emirates","United Arab Emirates"),
("United Kingdom","United Kingdom"),
("United States","United States"),
)

class CustomUserCreationForm(UserCreationForm):
    # country = forms.ChoiceField(choices=[(i.name,i.name) for i in Country.objects.all()])
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','email','country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control valid'})


class UserProfileForm(ModelForm):
    country = forms.ChoiceField(choices=country_choices,)
    def __init__(self, *args, **kwargs):
        # super(UserProfileForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.add_input(Submit('submit', 'Submit'))
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control','maxlength':10,'minlength':10})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'form-control'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'hidden': False,"id":'account-upload-form'})
        self.fields['country'].widget.attrs.update({'class': 'select2 form-select ','maxlength':8})

    class Meta:
            model = CustomUser
            fields = ('first_name', 'last_name','email','phone_number','address',
            'state','zipcode','country','image')

    # widgets = {
    #         'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'accountFirstName'}),
    #         'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'accountLastName'}),
    #         'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'accountEmail'}),
    #         'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'accountPhoneNumber'}),
    #         'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'accountAddress'}),
    #         'state': forms.TextInput(attrs={'class': 'form-control', 'id': 'accountState'}),
    #         'zipcode': forms.TextInput(attrs={'class': 'form-control', 'id': 'accountZipcode'}),
    #         'country': forms.Select(attrs={'class': 'form-control', 'id': 'accountCountry'}),
    #     }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=200)

    class Meta:
        fields = '__all__'
        widgets = {
            'email': EmailInput(attrs={
                'class': "form-control",
            })
        }


class CustomerDocumentForm(forms.ModelForm):
        docname=forms.ChoiceField(choices=[])
        class Meta:
            model = CustomerDocumentModel
            fields = ('attached_file','docname')

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            self.fields['attached_file'].widget.attrs.update({'class': 'form-control valid'})
            self.fields['docname'].widget.attrs.update({'class': 'form-control'})
            self.fields['docname'].choices = [(i.id, i.name) for i in DocumentSetModel.objects.filter(country=user.country)]

        def save(self, commit=True, customer=None):
            instance = super(CustomerDocumentForm, self).save(commit=False)
            if customer:
                instance.customer = customer
            if commit:
                instance.save()
            return instance