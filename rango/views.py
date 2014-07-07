from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from .models import Category
from .models import Page

def index(request):
	context = RequestContext(request)
	
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}

	return render_to_response('rango/index.html', context_dict, context)

	#context_dict = {'boldmessage': "I am bold front from the context"}
	#return render_to_response('rango/index.html', context_dict,context)

	#return HttpResponse("Rango says hello world! <a href='/rango/about'>About</a>")

def category(request,category_name_url):
	
	context = RequestContext(request)
	category_name = category_name_url.replace('_',' ')
	context_dict = {'category_name': category_name}

	try:
		category = Category.objects.get(name=category_name)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except:
		pass

	return render_to_response('rango/category.html', context_dict, context)

def about(request):
	context = RequestContext(request)

	return render_to_response('rango/about.html', request)
	#return HttpResponse("Rango says: Here is the about page <a href='/rango'>Index</a>")
