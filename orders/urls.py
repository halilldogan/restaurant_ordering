from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders import views
from .views import ProcessOrderView
from django.views.generic.base import RedirectView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'dishes', views.DishViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('order/process_order/', ProcessOrderView.as_view(), name='process_order'),
    path('', RedirectView.as_view(url='/api/', permanent=True))
]



