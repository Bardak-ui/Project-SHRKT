from django.shortcuts import render
from .models import Monument, Panorama, HotSpot
import json

def map_view(request):
    monuments = Monument.objects.all()
    return render(request, 'map.html', {'monuments':monuments})

def monument_detail(request, monument_id):
    monument = Monument.objects.get(id=monument_id)
    panoramas = Panorama.objects.filter(monument=monument)
    return render(request, 'monument_detail.html', {'monument': monument, 'panoramas': panoramas})

def panorama_view(request, panorama_id):
    panorama = Panorama.objects.get(id=panorama_id)
    return render(request, 'panorama.html', {'panorama': panorama, 'hotspots': panorama.hotspots.all()})
