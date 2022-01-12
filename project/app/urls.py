from django.urls import path, include
from . import views
from .views import views3, apiview1
from . import views1
from rest_framework import routers

router = routers.DefaultRouter()
router.register('views', views.apiviewset, basename='views')

urlpatterns = [
    path('router/', include(router.urls)),
    path('router/<int:pk>', include(router.urls)),
    path('3', views3),
    path('detail/<int:pk>/', views.view4),
    path('apiview', apiview1.as_view()),
    path('apiview/<int:id>/', views.apiview2.as_view()),
    path('generic/<int:id>', views.genericview1.as_view()),
]


urlpatterns += [
    path('', views1.index),
    path('signup', views1.signup),
    path('signin', views1.signin),
    path('signout', views1.signout),
    path('staffhome', views1.staffhome)
]

from . import views2
router.register('1', views2.v1)
urlpatterns += [
    path('11', views2.fun1),
    path('11/<int:pk>', views2.fun2),
    path('111/', include(router.urls)),

]