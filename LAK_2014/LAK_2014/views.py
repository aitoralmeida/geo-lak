# coding: utf-8

from django.shortcuts import render_to_response


# Create your views here.


#########################
# View: index
#########################

def index(request):
    return render_to_response('LAK_2014/index_2.html')


#########################
# View: view404
#########################

def view404(request):
    return render_to_response('LAK_2014/404.html')
