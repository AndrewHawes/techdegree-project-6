from random import choice

from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect

from .models import Mineral


def index(request):
    mineral_list = Mineral.objects.all()
    return render(request, 'minerals/index.html', {'mineral_list': mineral_list})


def detail(request, mineral_id):
    mineral = get_object_or_404(Mineral, pk=mineral_id)
    return render(request, 'minerals/detail.html', {'mineral': mineral})


def random_mineral(request):
    mineral_list = Mineral.objects.all()
    mineral = choice(mineral_list)
    return HttpResponseRedirect(reverse('minerals:detail', args=(mineral.id,)))
