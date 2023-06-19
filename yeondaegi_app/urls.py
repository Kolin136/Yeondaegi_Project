from django.urls import path
from . import views
from .views import (yeondaegi_List,yeondaegi_Detail,yeondaegi_detail_search_user, yeondaegi_detail_search_genre,Login_View,
                    Sign_up_View,Follow,Follow_detail,Like,User_delete_view
                    )



urlpatterns=[

    path('yeondaegi',yeondaegi_List.as_view()),
    path('yeondaegi/pagenum/<int:pagenum>/pagesize/<int:pagesize>',yeondaegi_List.as_view()),
    path('yeondaegi/<int:pk_id>',yeondaegi_Detail.as_view()),
    # path('yeondaegi/<str:word>',yeondaegi_detail_search.as_view()),
    path('yeondaegi/user/<str:word>',yeondaegi_detail_search_user.as_view()),
    path('yeondaegi/genre/<str:word>',yeondaegi_detail_search_genre.as_view()),
    path('yeondaegi/login',Login_View.as_view()),
    path('yeondaegi/sign_up',Sign_up_View.as_view()),
    path('yeondaegi/follow',Follow.as_view()),
    path('yeondaegi/follow/<str:word>',Follow_detail.as_view()),
    #↓ pk_id는 좋아요를 할 글의 pk , word는 추천,비추천 결정/ 소문자 true,false 
    path('yeondaegi/like/<int:pk_id>/<str:word>',Like.as_view()),
    path('yeondaegi/user_delete',User_delete_view.as_view()),
    
]