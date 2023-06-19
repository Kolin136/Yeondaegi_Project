from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.create,name='create'),
    path('search/',views.search,name='search'),
    path('list/',views.all_list,name='all_list'),
    path('sign/',views.sign_up,name='sign'),
    # 로그인 처리를 위해서 추가
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('home/',views.home,name='home'),
    path('mylist/',views.my_list,name='my_list'),
    path('mydelete/<int:delete_id>',views.my_delete,name='my_delete'),
    path('myupdate/<int:update_id>',views.my_update,name='my_update'),
    path('follow/',views.follow,name='follow'),
    path('followclear/',views.follow_clear,name='follow_clear'),
    path('followsearch/',views.follow_search,name='follow_search'),
    path('follow_s_result',views.following_search_result,name='following_search_result'),
    path('like/<int:post_id>',views.like,name='like'),
    path('likelist/<int:post2_id>',views.like_list,name='like_list'),
]