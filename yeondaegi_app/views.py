# from django.shortcuts import render   
# from django.shortcuts import render,get_object_or_404,redirect
# from django.http import HttpResponse, HttpResponseRedirect
# import json
# from django.core.serializers.json import DjangoJSONEncoder
# from django.http import JsonResponse
# from django.core import serializers
# from yeondaegi_app.forms import Organize_Form,Search_Form,Sign_Form,Login_Form,UpdateOrganize_Form,UpdateGenre_Form
from yeondaegi_app.models import Genre,Organize,Sign_up,Follow,Profile,DRF_Follow
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from yeondaegi_app.serializers import Organize_Serializer,DRF_Follow_Serializer,Like_Serializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


# Create your views here.

class YourPaginationClass(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

#↓ 페이지네이션 데이터 갯수 계산하고 데이터 인덱스 리턴해주는 클래스
class Pagenation:
   def calculate(page_num,page_size):
      if page_num == 1:
         start = 0
         end = page_size
         return start,end
      else:
         start = (page_num-1)*page_size
         end = start + page_size
         return start,end

class yeondaegi_List(APIView):
   pagination_class = YourPaginationClass

   def get(self,request):
      #↓ 장고에서 제공해주는 페이지네이션
      # -----------------------------------------------------------------
      # paginator = self.pagination_class()
      # yeon = Organize.objects.all()
      # paginated_yeon = paginator.paginate_queryset(yeon, request)
      # serializer = Organize_Serializer(paginated_yeon, many=True)
      # return paginator.get_paginated_response(serializer.data)
      #-----------------------------------------------------------------

      # #↓ GET.get()에서 괄호안 두번째값은 page의 키가 존재하지 않으면 그 두번째값을 기본으로 한다는거다
      idx_value=Pagenation.calculate( int(request.GET.get('page',1)) , int(request.GET.get('page_size',3)) )
      
      yeon =Organize.objects.all()[idx_value[0]:idx_value[1]]
      serializer = Organize_Serializer(yeon,many=True)
      return Response(serializer.data)
   
   def post(self,request):

      if (Genre.objects.filter( genre_name = request.data['organize_id'] ).exists() and
          User.objects.filter( username = request.user ).exists() ):   # exists()는 장고 모델 데이터 존재여부 확인
         
         genre = Genre.objects.get( genre_name = request.data['organize_id'] ) # 장르가 존재하니 그 장르 객체 가져오기
         user_name = User.objects.get( username = request.user ) # 유저 id(이름)이 존재하니 유저 정보 객체 가져오기
         request.data['u_id'] = user_name.pk   # u_id 시리얼 라이저에는 int형 보내야하니 pk값으로 설정

         # ↓ genre변수에 장르 담았고 organize_id는 ForeignKey키 이기때문에 현재 post로 받은 organize_id는 문자형이니 딕셔너리에서 삭제
         del request.data['organize_id']  

         # ↓ 시리얼라이저 작업
         serializer= Organize_Serializer(data= request.data)
         if serializer.is_valid(raise_exception=True):
            serializer.save(organize_id=genre) #ForeignKey 같은거나 데이터 객체 자체는 따로 괄호안에 적어야하는듯? 
            return Response(serializer.data,status=status.HTTP_201_CREATED)    
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      # ↓ 유저는 존재하고 장르가 없으니 장르 새로 생성후 저장
      elif (not Genre.objects.filter( genre_name = request.data['organize_id'] ).exists() and
            User.objects.filter( username = request.user ).exists() ):
         
         genre = Genre( genre_name = request.data['organize_id'] ) 
         genre.save()

         # ↓ 밑에 시리얼 라이저 작업까지는 post함수 if문 안에 있는거랑 같으니 그쪽 주석 참고
         user_name = User.objects.get( username = request.user )
         request.data['u_id'] = user_name.pk  
         del request.data['organize_id'] 

         serializer= Organize_Serializer(data= request.data)
         if serializer.is_valid(raise_exception=True):
            serializer.save(organize_id=genre) 
            return Response(serializer.data,status=status.HTTP_201_CREATED)    
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      # ↓ 유저가 존재하지 않는 경우 
      else:
         return Response({"message": "존재하지 않는 유저"}, status=status.HTTP_404_NOT_FOUND)
            
            
class yeondaegi_Detail(APIView):
   # ↓ 특정 데이터 조회,수정,삭제하기위해 그 특정 데이터를 pk로 검색후 가져오는 역활 함수
   def get_object(self,pk_id):
      yeon_data = get_object_or_404(Organize,pk= pk_id)
      return yeon_data
   
   def get(self,request,pk_id):
      pk_search_data =self.get_object(pk_id) 
      #pk_search_data.['full_url']="/media/aaaa"
      serializer = Organize_Serializer(pk_search_data)
      # serializer.data["full_url"]="/media/aaaa"
      print("check2", serializer.data)
      return Response(serializer.data)
   
   def patch(self,request,pk_id):
      pk_search_data =self.get_object(pk_id) 
      serializer = Organize_Serializer(pk_search_data, data=request.data, partial=True) #  partial은 부분수정 일때,전체 수정 put일땐 안적어도 된다

      
      if serializer.is_valid(raise_exception=True): # raise_exception=True는 유효성 검사 false일시  400 response를 반환
            serializer.save()
            return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def delete(self,request,pk_id):
      pk_search_data = self.get_object(pk_id)
      pk_search_data.delete()
      return Response(status = status.HTTP_204_NO_CONTENT)


class yeondaegi_detail_search_genre(APIView):

   # ↓ 장르 검색으로 데이터 가져오고 싶을때 사용하는 함수
   def genre_object(slef,request,word):

      idx_value=Pagenation.calculate( int(request.GET.get('page',1)) , int(request.GET.get('page_size',3)) )
      
      genre = get_object_or_404(Genre,genre_name= word)
      search_data = Organize.objects.filter( organize_id = genre.id )[idx_value[0]:idx_value[1]]
      return search_data

   # ↓ 이 함수안에서 위에 장르,유저 함수로 데이터 가져오고 그 데이터를 출력하게 하는 함수
   def get(self,request,word):
      result_data = self.genre_object(request,word)
      serializer = Organize_Serializer(result_data,many=True)
      print('데이터 체크',serializer.data)
      return Response(serializer.data)


class yeondaegi_detail_search_user(APIView):

  
   # ↓ 유저 검색으로 데이터 가져오고 싶을때 사용하는 함수
   def user_object(self,request,word):
      idx_value=Pagenation.calculate( int(request.GET.get('page',1)) , int(request.GET.get('page_size',3)) )
      user = get_object_or_404(User,username= word)
      search_data = Organize.objects.filter( u_id = user.id)[idx_value[0]:idx_value[1]]
      return search_data

   # ↓ 이 함수안에서 위에 유저 함수로 데이터 가져오고 그 데이터를 출력하게 하는 함수
   def get(self,request,word):
      result_data = self.user_object(request,word)    
      serializer = Organize_Serializer(result_data,many=True)
      print('데이터 체크',serializer.data)
      return Response(serializer.data)


class Sign_up_View(APIView): 
   #↓ 로그인 필요 없이 접근 가능하게 해주는것
   permission_classes = [AllowAny]

   def post(self,request):
      if User.objects.filter(username=request.data['id']).exists():
         return Response({"message": "이미 존재하는 아이디"})

      else: 
         try:
            if request.data['nickname'] and request.data['password']:
               user = User.objects.create_user(username = request.data['id'], password = request.data['password'])
               profile = Profile(user_info=user, user_nick=request.data['nickname'])
               profile.save()
               return Response({"message": "회원가입 완료"})
         except:
            return Response({"message": "닉네임 or비밀번호 입력해주세요"})
     

class Login_View(APIView):
   #↓ 로그인 필요 없이 접근 가능하게 해주는것
   permission_classes = [AllowAny]
   
   def post(self,request):
      #↓ authenticate()는 사용자 인증을 하고 인증이 성공하면 해당 사용자 객체를 반환합니다. 인증에 실패하거나 해당하는 사용자가 없는 경우에는 None을 반환합니다.
      user_data = authenticate(username = request.data['id'], password = request.data['password'])
      print('체크',user_data)

      if user_data:
               #↓ 토큰 생성하는거라 create 해야하는데 _ 로해도 상관없는듯한?? 
         token, _= Token.objects.get_or_create(user=user_data)
         
         return Response({"message": "로그인 성공","Token": token.key},status=status.HTTP_200_OK)
      else:
            return Response({"message": "로그인 실패"},status=status.HTTP_401_UNAUTHORIZED)

class User_delete_view(APIView):
   def post(self,request):
      user_password_check = authenticate(username = request.user ,password = request.data['password'])
      print('유저체크',type(user_password_check))

      if user_password_check:
         #---------------팔로우 모델을 ForeignKey로 안해서 직접 필터링후 삭제 작업을 해야한다--------------

         #↓ Follow_detail 클래스안 닉네임 리턴함수 호출
         nick = Follow_detail.user_object(self,request.user)

         #↓Django의 ORM에서는 논리 연산자 or를 직접 사용하지 않고 Q 객체를 이용하여 OR 연산을 구현합니다.
         # 즉, or 대신 | 연산자를 사용하여 Q 객체를 결합하는 것이 Django의 권장 방식입니다. (Q를 임포트 해야한다)
         # 이렇게 하는 이유는 현재 탈퇴하려는 유저가 팔로우한 목록이랑 다른 유저가 탈퇴하려는 유저를 팔로우했던 목록 둘다 가져와서 삭제해야하기떄문
         follow_data = DRF_Follow.objects.filter(Q( user = nick) | Q(friend = nick))
         # follow_data.delete()
        
         #-----------------------------------------------------------------------------------------

         #↓ Organize의 u_id를 ForeignKey로 안해서 회원 탈퇴하려는 유저의 글을 위에 팔로우 처럼 직접 필터링해서 삭제한다
         user = get_object_or_404(User,username= request.user)
         user_search_data = Organize.objects.filter( u_id = user.id )
         # user_search_data.delete()

         #↓ user변수에는 탈퇴하려는 유저 User모델의 객체가 담겨있으니 그대로 삭제하면 된다.
         #↓ 프로필 모델에 User모델 참조하는거에 on_delete=models.CASCADE 했으니,
         #↓ User모델객체 삭제하면 프로필 모델에 탈퇴하려는 유저 데이터도 자동으로 삭제하고 토큰도 자동으로 삭제한다. 토큰도 자동 삭제는
         #↓ 장고 자체에서 on_delete=models.CASCADE기능 넣은듯 
         # user.delete()
         
         



      else:
         return Response({"message":"비밀번호 틀림"})


class Follow(APIView):
   def user_object(self,login_user):
      #↓ 다른 함수에서 이 함수 호출할때 이 함수는 매개변수 login_user에는 계정 id명을 받는다
      user = get_object_or_404(User,username = login_user) 
      #↓ nick 변수에서는 Profile 테이블에서 user 변수에 담긴 데이터 검색후 nick.user_nick으로 닉네임 리턴하면 된다
      nick=get_object_or_404(Profile,user_info = user)
      return nick.user_nick

   def get(self,request):
      user_nick= self.user_object(request.user)
      user_friend= DRF_Follow.objects.filter(user = user_nick) 
      serializer = DRF_Follow_Serializer(user_friend,many=True)
      return Response(serializer.data)
  
   def post(self,request):
      user_nick= self.user_object(request.user)
      #↓ url에 팔로우할 친구 보내는게 아니고 friend라는 폼이나 필드로 보내야한다  
      friend_nick = request.data['friend']

      #↓ 이미 친구인지 아닌지 확인
      if DRF_Follow.objects.filter(user = user_nick , friend = friend_nick):
         return Response({"message": f"{friend_nick}는 이미 친구인 상태"})
      
      #↓ 친구가 아니면 이제 친구로 설정
      else:
         #↓ 현재 request.data는 친구 신청 하려는 friend 만 담겨있고 user정보는 없으니 시리얼라이저에 보낼수 없다. 그러므로 직접 user 정보 추가해준다
         request.data['user'] = user_nick
         serializer = DRF_Follow_Serializer(data = request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Follow_detail(APIView):
   def user_object(self,login_user):
      #↓ 다른 함수에서 이 함수 호출할때  매개변수 login_user에는 계정 id명을 받는다
      user = get_object_or_404(User,username = login_user) 
      #↓ nick 변수에서는 Profile 테이블에서 user 변수에 담긴 데이터 검색후 nick.user_nick으로 닉네임 리턴하면 된다
      nick=get_object_or_404(Profile,user_info = user)
      return nick.user_nick


   def delete(self,request,word):
      user_nick= self.user_object(request.user)
      user_data = DRF_Follow.objects.filter(user = user_nick , friend = word)
      user_data.delete()
      return Response({"message": f"{word} 삭제완료"},status = status.HTTP_204_NO_CONTENT)
   
class Like(APIView):

   #↓ Follow_detail 클래스안 함수랑 리턴값만 다르고 나머진 같은거
   def user_object(self,login_user):
      user = get_object_or_404(User,username = login_user) 
      nick=get_object_or_404(Profile,user_info = user)
      return nick
   
   def post(self,request,pk_id,word):
      profile_data = self.user_object(request.user)
      like_organize = Organize.objects.get(pk = pk_id)

      #예를 들어 A유저가 1번글 이미 좋아요 했는데 클라에서 1번글에 A유저가 또 좋아요 하면 중복 좋아요를 할수도 있다. 좋아요 취소도 마찬가지
      # 하지만 이건 프론트엔드쪽에서 인풋버튼인가 폼으로 중복 안되게 할수도 있으니 지금은 그냥 백엔드쪽은 중복 좋아요 안되게 하는 기능 패스했다
        
      #↓ url true로 받으면 글추천 
      if word == 'true':
         #↓ ManyToManyField 관계 데이터 추가하는법, like_drf는 Organize의 manytomany해당 변수이고 추가할때 
         #↓ add 함수를 사용하고 괄호안에는 Organize와 관계를 맺으려는 Profile 모델에서 한개의 데이터 넣고 save한다
         like_organize.like_drf.add(profile_data)
         like_organize.like_count_drf += 1
         like_organize.save()

      #↓ url false로 받으면 글추천 취소
      elif word == 'false':
         like_organize.like_drf.remove(profile_data)
         like_organize.like_count_drf -= 1
         like_organize.save()

      #↓ 이 밑에부분들은 이제 클라한테 좋아요의수,좋아요 유저 목록을 보내주는 작업

      #↓ 해당글 좋아요한 유저들 ManyToMany 관계로 전부 가져오기
      like_object = like_organize.like_drf.all()
      like_nick_list=[i.user_nick for i in like_object]
      print('체크',like_nick_list)

      #↓ 시리얼 라이저에 해당글의 좋아요수,좋아요 유저 리스트 보내려면 request 데이터에 직접 넣어줘야한다.직접 넣기전엔 좋아요수,
      #↓ 좋아요 유저 리스트 정보가 request에 없는 상태니
      request.data['like_count'] = like_organize.like_count_drf
      request.data['like_list'] = like_nick_list

      serializer = Like_Serializer(request.data)
      return Response(serializer.data)
         


# render ,redirect 차이점===> render 는 템플릿을 불러오고, redirect 는 URL로 이동합니다

