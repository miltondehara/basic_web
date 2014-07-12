from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from .models import Category, Page
from rango.forms import CategoryForm, PageForm


def encode_url(str):
	return str.replace(' ','_')
def decode_url(str):
	return str.replace('_',' ')

def index(request):
	context = RequestContext(request)
	page_list = Page.objects.order_by('-views')[:5]

	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list,'pages': page_list}
	#context_dict['pages'] = page_list

	for category in category_list:
		category.url = category.name.replace(' ', '_')

	return render_to_response('rango/index.html', context_dict, context)

	#context_dict = {'boldmessage': "I am bold front from the context"}
	#return render_to_response('rango/index.html', context_dict,context)

	#return HttpResponse("Rango says hello world! <a href='/rango/about'>About</a>")

def category(request,category_name_url):
	
	context = RequestContext(request)
	category_name = category_name_url.replace('_',' ')
	context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

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

def add_category(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()

	return render_to_response('rango/add_category.html', {'form': form}, context)		

def add_page(request, category_name_url):
	context = RequestContext(request)

	category_name = decode_url(category_name_url)
	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():

			page = form.save(commit=False)

			try:
				cat = Category.objects.get(name=category_name)
				page.category = cat
			except Category.DoesNotExist:

				return render_to_response('rango/add_category.html', {}, context)

			page.views = 0
			page.save()

			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm()

	return render_to_response('rango/add_page.html',
	 {'category_name_url': category_name_url,
	 'category_name': category_name, 'form': form}, 
	 context)





