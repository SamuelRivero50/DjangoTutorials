from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.urls import reverse

# Create your views here.
def homePageView(request): 
    return HttpResponse('Hello World!') 
class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        return context


class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact Information",
            "email": "contacto@tiendaonline.com.co",
            "address": "Carrera 49 #7 Sur-50, El Poblado, Medellín, Antioquia, Colombia",
            "phone": "+57 (4) 261-9500",
            "company": "Tienda Online Colombia S.A.S"
        })
        return context

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 599.99},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 899.99},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 35.99},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 129.99}
    ]


class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'
    
    def get(self, request, id):
        try:
            # Check if id is a valid integer
            product_id = int(id)
            
            # Check if the product exists (valid range: 1 to len(products))
            if product_id < 1 or product_id > len(Product.products):
                return HttpResponseRedirect(reverse('home'))
            
            # Get the product (subtract 1 because list is 0-indexed but IDs start at 1)
            product = Product.products[product_id - 1]
            
            viewData = {}
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] = product["name"] + " - Product information"
            viewData["product"] = product
            return render(request, self.template_name, viewData)
            
        except (ValueError, IndexError):
            # If id is not a valid integer or any other error occurs, redirect to home
            return HttpResponseRedirect(reverse('home'))

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return redirect(form)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)