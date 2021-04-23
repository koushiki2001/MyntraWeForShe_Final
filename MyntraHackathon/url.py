from django.urls import path

from . import views1

urlpatterns = [

    
    path('',views1.open),
    path('index',views1.open),
    path('up', views1.simple_upload, name = 'create'),
    path('results',views1.check_results),
    path('products',views1.view_products),
    path('sketches',views1.showSketches),
    path('findTops',views1.findTops),

    
]