"""yeondaegi_setting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('yeon/',include('yeondaegi_app.urls'))
    # path('',include('yeondaegi_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #↑ 개발모드에서는 미디어파일을 자동으로 서빙해주지 않는다고한다. 그래서 수동으로 할 수 있게끔 위와 같이 static메서드를 이용해서 추가해줘야한다고 한다