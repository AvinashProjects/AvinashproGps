from django.shortcuts import render
from .models import *
from geopy.geocoders import Nominatim
from .utils import get_center_coordinates
from geopy import distance

# Importing the geodesic module from the library
from geopy.distance import geodesic

import folium
from datetime import datetime


# Create your views here.

dict = {}
l_lat = ''
l_lon = ''
def indexview(request):
    return render(request,'testapp/index.html')

def deliverylctn(request):
    #locating delivery boy location
    geolocator = Nominatim(user_agent="testapp")

    obj = Deliveryboylctn.objects.get(id=1)

    l_lat = obj.l_lat
    l_lon = obj.l_lon

    location = geolocator.reverse("{}, {}".format(l_lat, l_lon))


    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=11)

    # location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup='Your location',
                  icon=folium.Icon(color='blue')).add_to(m)

    # 15 kms circle around the delivery boy locaktion
    folium.Circle([l_lat, l_lon], radius=15000).add_to(m)


    #obj for orders
    orders = Orders.objects.all()
    y=0

    for ord in orders:
        # Loading the lat-long data for Kolkata & Delhi
        current_location = (l_lat, l_lon)
        d_lat = ord.order_lat
        d_lon = ord.order_lon
        destination_location = (d_lat, d_lon)

        # Print the distance calculated in km
        radius = 15
        dist = geodesic(current_location, destination_location).km



        if dist < radius:
            y += 1
            if y == 6:
                break
            folium.Marker([d_lat, d_lon], tooltip='click here for more', popup='Delivery loation',icon=folium.Icon(color='purple')).add_to(m)
            # line = folium.PolyLine(locations=[current_location, destination_location], weight=5, color='blue')
            # m.add_child(line)
            global dict
            dict[ord.id] = dist


    # print(dict)

    map = m._repr_html_()
    context = {'map':map}
    return render(request,'testapp/deliverylctn.html',context)



def Deistinatinonebyone(request):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # print('executing')

    if len(dict)==0:
        orders = Orders.objects.all()
        return render(request,'testapp/endoflist.html',{'orders':orders})

    geolocator = Nominatim(user_agent="testapp")

    obj = Deliveryboylctn.objects.get(id=1)
    obj.start_time = current_time
    obj.save()

    l_lat = obj.l_lat
    l_lon = obj.l_lon

    location = geolocator.reverse("{}, {}".format(l_lat, l_lon))

    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=11)

    # location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup='Your location',icon=folium.Icon(color='blue')).add_to(m)

    # 15 kms circle around the delivery boy locaktion
    folium.Circle([l_lat, l_lon], radius=15000).add_to(m)

    # print(dict)


    #finding shortest location
    key_min = min(dict.keys(), key=(lambda k: dict[k]))
    speed = 40
    time_reach = (key_min / speed)*60

    #finding corresponding id
    order_id = list(dict.keys())[list(dict.values()).index(dict[key_min])]
    orders = Orders.objects.get(id=order_id)


    current_location = (l_lat, l_lon)
    d_lat = orders.order_lat
    d_lon = orders.order_lon
    destination_location = (d_lat, d_lon)

    folium.Marker([d_lat, d_lon], tooltip='click here for more', popup='Delivery loation',icon=folium.Icon(color='purple')).add_to(m)
    line = folium.PolyLine(locations=[current_location, destination_location], weight=5, color='blue')
    m.add_child(line)

    l_lat = d_lat
    l_lon = d_lon

    map = m._repr_html_()
    context = {'map': map,'time_reach':time_reach}

    if request.method == "POST":

        # print(len(dict))

        # print('post executing')
        key_min = min(dict.keys(), key=(lambda k: dict[k]))
        order_id = list(dict.keys())[list(dict.values()).index(dict[key_min])]
        orders = Orders.objects.get(id=order_id)
        t = request.POST['t']
        orders.deliverd_time = t
        orders.save()
        del dict[key_min]


        location = geolocator.reverse("{}, {}".format(l_lat, l_lon))
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=11)
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup='Your location',icon=folium.Icon(color='blue')).add_to(m)

        if len(dict)>=1:
            key_min = min(dict.keys(), key=(lambda k: dict[k]))
            order_id = list(dict.keys())[list(dict.values()).index(dict[key_min])]
            orders = Orders.objects.get(id=order_id)

            current_location = (l_lat, l_lon)
            d_lat = orders.order_lat
            d_lon = orders.order_lon
            destination_location = (d_lat, d_lon)

            folium.Marker([d_lat, d_lon], tooltip='click here for more', popup='Delivery loation',icon=folium.Icon(color='purple')).add_to(m)
            line = folium.PolyLine(locations=[current_location, destination_location], weight=5, color='blue')
            m.add_child(line)

            speed = 40
            time_reach = (key_min / speed)*60


        l_lat = d_lat
        l_lon = d_lon


        map = m._repr_html_()
        context = {'map': map,'time_reach':time_reach}
        return render(request, 'testapp/destination.html', context)


    return render(request, 'testapp/destination.html',context)