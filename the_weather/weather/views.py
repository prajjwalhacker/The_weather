import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
# Create your views here.

def index(request):
    city = City.objects.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=77dfe7903bd21efbc773dad1b2f1b521'
    
    if request.method == 'POST':
        cc = False
        for i in city:
            if i.name == request.POST['name']:
                cc = True 
        if cc==0:
            form = CityForm(request.POST)
            form.save()
            return redirect('index')

    
    form = CityForm()
        

    list = []
    for cty in city:
         
         r = requests.get(url.format(cty.name)).json()
         weather = {
         'city' : cty.name,
         'temperature' : r['main']['temp'],
         'description':  r['weather'][0]['description'],
         'icon' : r['weather'][0]['icon'], 
         }
         list.append(weather)

    context = {
        'list' : list,
        'form' : form,
    }
    return render(request,'weather/weather.html',context)

