import requests
from django.shortcuts import redirect, render,HttpResponse, redirect
from .models import City
from .form import CityForm
# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid= put your api key'

    msg = ''
    msg_for_user = ''
    msg_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            new_city_count = City.objects.filter(name = new_city).count()

            if new_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                
                if r['cod'] == 200:
                    form.save()
                else:
                    msg = 'City Not Found!'
            else:
                msg = 'City is already Exist!'
    
        if msg:
            msg_for_user = msg
            msg_class = 'alert alert-danger'
        else:
            msg_for_user = 'City Added Successfully!'
            msg_class = 'alert alert-success'
    form = CityForm()
    
    cities = City.objects.all()

    weather_data = []
    for city in cities:

        r = requests.get(url.format(city)).json()
        
        city_weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
        'form': form,
        'msg' : msg_for_user,
        'msg_class' : msg_class 
        }
    return render(request, 'i.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
