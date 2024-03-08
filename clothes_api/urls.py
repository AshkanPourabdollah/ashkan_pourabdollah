from django.urls import path,include
from . import views
from rest_framework.authtoken import views as rest_framework_views
urlpatterns = [
    path('products/',views.ProcutsApi.as_view()),
    path('card/<phone>/',views.CartApi.as_view()),
    path('getToken/',rest_framework_views.obtain_auth_token),

]