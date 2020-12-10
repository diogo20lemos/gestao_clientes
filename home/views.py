from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.views.generic.base import View


def home(request):
    return render(request, 'home.html')


def my_logout(request):
    logout(request)
    return redirect('home')


class MyView(View):
    def get(self, request, *args, **kwargs):
        reponse = render_to_response('home3.html')
        reponse.set_cookie('cor', 'blue', max_age=1000)
        # mycookie = request.COOKIES.get('color') valor do cookie
        return reponse

    def post(self, request, *args, **kwargs):
        return HttpResponse('Post')