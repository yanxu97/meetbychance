from django import forms
from django.contrib.auth.models import User
import re
from .models import travel_Plan

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email',)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 6:
            raise forms.ValidationError("Your username must be at least 6 characters long.")
        elif len(username) > 50:
            raise forms.ValidationError("Your username is too long.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your email already exists.")
        else:
            raise forms.ValidationError("Please enter a valid email.")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password1) > 20:
            raise forms.ValidationError("Your password is too long.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")

        return password2


class LoginForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("This email does not exist.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                        raise forms.ValidationError("This username does not exist. Please register first.")

        return username

class ProfileForm(forms.Form):

   first_name = forms.CharField(label='First Name', max_length=50, required=False)
   last_name = forms.CharField(label='Last Name', max_length=50, required=False)
   org = forms.CharField(label='Organization', max_length=50, required=False)
   telephone = forms.CharField(label='Telephone', max_length=50, required=False)


class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput)

    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password1) > 20:
            raise forms.ValidationError("Your password is too long.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")

        return password2

Country_CHOICES = [('unknown','-------'),('Austria', 'Austria'), ('Belgium', 'Belgium'), ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'), ('Bulgaria', 'Bulgaria'), ('China','China'), ('Croatia','Croatia'),('Czech Republic', ' Czech Republic'), ('Denmark ', 'Denmark '), ('England', 'England'), ('Estonia ', 'Estonia '), ('Finland', 'Finland'), ('France', 'France'), ('Germany', 'Germany'), ('Greece', 'Greece'), ('Hungary', 'Hungary'), ('Iceland', 'Iceland'), ('Ireland', 'Ireland'), ('Italy', 'Italy'), ('Latvia', 'Latvia'), ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'), ('Malta', 'Malta'), ('Netherlands', 'Netherlands'), ('Norway', 'Norway'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('Romania', 'Romania'), ('Russia', 'Russia'), ('Scotland', 'Scotland'), ('Serbia', 'Serbia'), ('Slovakia', 'Slovakia'), ('Slovenia', 'Slovenia'), ('Spain', 'Spain'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('Turkey', 'Turkey'),('United States','United States'), ('Ukraine', 'Ukraine'),]
City_CHOICES = [('unknown','-------'),('Amsterdam','Amsterdam'),
('Athens','Athens'),
('Barcelona','Barcelona'),
('Belgrade','Belgrade'),
('Bergen','Bergen'),
('Berlin','Berlin'),
('Bratislava','Bratislava'),
('Bruges','Bruges'),
('Brussels','Brussels'),
('Bucharest','Bucharest'),
('Budapest','Budapest'),
('Český Krumlov','Český Krumlov'),
('Champaign','Champaign'),
('Chicago','Chicago'),
('Copenhagen','Copenhagen'),
('Dublin','Dublin'),
('Dubrovnik','Dubrovnik'),
('Edinburgh','Edinburgh'),
('Florence','Florence'),
('Hamburg','Hamburg'),
('Helsinki','Helsinki'),
('Ibiza','Ibiza'),
('Interlaken','Interlaken'),
('Istanbul','Istanbul'),
('Kiev','Kiev'),
('Krakow','Krakow'),
('Lisbon','Lisbon'),
	('Ljubljana','Ljubljana'),
('London','London'),
('Luxembourg City','Luxembourg City'),
('Madrid','Madrid'),
('Milan','Milan'),
('Moscow','Moscow'),
('Munich','Munich'),
	('Naples','Naples'),
('Nice','Nice'),
('Oslo','Oslo'),
('Paris','Paris'),
('Prague','Prague'),
('Reykjavik','Reykjavik'),
('Riga','Riga'),
('Rome','Rome'),
('Saint Petersburg','Saint Petersburg'),
('Salzburg','Salzburg'),
('Santorini','Santorini'),
('Sarajevo','Sarajevo'),
('Sofia','Sofia'),
('Split','Split'),
('Stockholm','Stockholm'),
('Tallinn','Tallinn'),
('Tenerife','Tenerife'),
('Urbana','Urbana'), ('Valletta','Valletta'), ('Venice','Venice'),
('Vienna','Vienna'),
('Vilnius','Vilnius'),
('Warsaw','Warsaw'),
('Zagreb','Zagreb'),
('Zurich','Zurich'),
('Beijing','Beijing'),
('Shanghai','Shanghai'),
('Chengdu','Chengdu'),
('HongKong','HongKong'),
('New York','New York'),
('Houston','Houston'),
('Los Angeles','Los Angeles'),
('San Jose','San Jose'),]

State_CHOICES=[('unknown','-------'),
               ('Alabama','Alabama'),
               ('Alaska ','Alaska'),
               ('Arizona','Arizona'),
('Arkansas','Arkansas'),
('California','California'),
('Colorado','Colorado'),
('Connecticut','Connecticut'),
('Delaware','Delaware'),
('Florida','Florida'),
('Georgia','Georgia'),
('Hawaii','Hawaii'),
('Idaho','Idaho'),
('Illinois','Illinois'),
('Indiana','Indiana'),
('Iowa','Iowa'),
('Kansas','Kansas'),
('Kentucky','Kentucky'),
('Louisiana','Louisiana'),
('Maine','Maine'),
('Maryland','Maryland'),
('Massachusetts','Massachusetts'),
('Michigan','Michigan'),
('Minnesota','Minnesota'),
('Mississippi','Mississippi'),
('Missouri','Missouri'),
('Montana','Montana'),
('Nebraska','Nebraska'),
('Nevada','Nevada'),
('New Hampshire','New Hampshire'),
('New Jersey','New Jersey'),
('New Mexico','New Mexico'),
('New York','New York'),
('North Carolina','North Carolina'),
('North Dakota','North Dakota'),
('Ohio','Ohio'),
('Oklahoma','Oklahoma'),
('Oregon','Oregon'),
('Pennsylvania','Pennsylvania'),
('Rhode Island','Rhode Island'),
('South Carolina','South Carolina'),
('South Dakota','South Dakota'),
('Tennessee','Tennessee'),
('Texas','Texas'),
('Utah','Utah'),
('Vermont','Vermont'),
('Virginia','Virginia'),
('Washington','Washington'),
('West Virginia','West Virginia'),
('Wisconsin','Wisconsin'),
('Wyoming','Wyoming'),]

class post_plan_Form(forms.Form):
    #country = forms.ModelChoiceField(label=u'Country', queryset=travel_Plan.objects.all().values_list('country', flat=True).distinct())
    #city = forms.ModelChoiceField(label=u'City', queryset=travel_Plan.objects.all().values_list('city', flat=True).distinct())

    country = forms.CharField(label='Country', max_length=128, widget=forms.Select(choices = Country_CHOICES))
    state = forms.CharField(label='State', max_length=128, widget=forms.Select(choices = State_CHOICES))
    city = forms.CharField(label='City', max_length=128, widget=forms.Select(choices = City_CHOICES))
    budget = forms.IntegerField(label='Budget')
    start_time = forms.DateField(label='Start_time')
    end_time = forms.DateField(label='End_time')



