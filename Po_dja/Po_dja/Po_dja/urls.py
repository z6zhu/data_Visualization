"""Po_dja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from app2 import views
from topo import topo_views
from user_shop import US_views
#from app2.urls import router as app2_router
#from app2.views import do_te
urlpatterns = [
    url(r'^admin/', admin.site.urls),
   # url(r'^api/', include(app2_router.urls)),
   # url(r'^test/', views.do_te),
   # url(r'^map_char1/', views.map_char1),
    url(r'^map_char1/',views.map_char1),
    url(r'^topo/', topo_views.topo),
    url(r'^user_shop/', US_views.user_shop),
   
    
]
