from django.urls import path
from .views import *

urlpatterns = [
    path('', home , name='home'),
    path('signup/', sign__up , name='signup'),
    path('login/', log__in , name='login'),
    path('logout/', log__out , name='logout'),
    path('home/<str:pk>/' , product_detail , name='product_detail' ),  # Sproduct details
    path('my_account/' , my_account , name='my_account' ),  # My account
    # path('edit my account' , edit_my_account , name='edit_my_account' ),  # Edit My account
    path('search result/', search_product, name='search_product'),
    
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('view_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('view_cart/', view_cart, name='view_cart'), 
    path('my_orders/', my_order, name='my_order'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
    path('download_bill/<int:id>/', generate_pdf_bill, name='generate_pdf_bill'),
]


 


    