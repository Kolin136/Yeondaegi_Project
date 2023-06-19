from django.shortcuts import render   
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.core import serializers
from yeondaegi_app.forms import Organize_Form,Search_Form,Sign_Form,Login_Form,UpdateOrganize_Form,UpdateGenre_Form
from yeondaegi_app.models import Genre,Organize,Sign_up,Follow
from django.core.paginator import Paginator

# Create your views here.

# render ,redirect 차이점===> render 는 템플릿을 불러오고, redirect 는 URL로 이동합니다

def create(request):       
   if request.session.get('user'):
      if request.method == 'POST':
         form_data = Organize_Form(request.POST,request.FILES)
         
         
         Genre_received= request.POST.get('organize_id')
         year= request.POST.get('year_date')
         month = request.POST.get('month_date')
         if month == '':
            month = None
         day = request.POST.get('day_date')
         if day == '':
            day = None
         content = request.POST.get('contents')
         try:  
            file=request.FILES['img_file']
         except:
            file =''
            
         hide = request.POST.get('hide_check')
         if hide == None:
            print('hide값:none')
            hide='0'


         if Genre.objects.filter(genre_name=Genre_received).exists():   # exists()는 장고 모델 데이터 존재여부 확인
            print('있음')
            genre =Genre.objects.get(genre_name=Genre_received)
            c=Organize(year_date=year,month_date= month,day_date= day, organize_id=genre, contents=content,u_id=request.session.get('user'),
                       img_file=file, hide_data=hide)
            c.save()
         else:
            print('없음')
            #장르를 새로 저장
            genre =Genre(genre_name=Genre_received)
            genre.save()
            print(genre.id)
            c=Organize(year_date=year,month_date=month,day_date=day,organize_id=genre,contents=content,u_id=request.session.get('user'),
                       img_file=file, hide_data=hide)
            c.save()
            
         return redirect('home')
      else:
         form_data = Organize_Form(use_required_attribute=False)   # use_required_attribute=False 는 폼입력을 필수로 안하게 하고싶을때
         return render(request,'yeon/create.html',{'form':form_data})
   else:
      print('로그인부터')
      return redirect('login')

def search(request):
   if request.session.get('user'):
      if request.method == 'POST':
         search_data=request.POST.get('search_form')
         
         Genre_result = Genre.objects.filter(genre_name__contains = search_data)
         
         print('분야 리스트:',Genre_result)
      
         result_list=[]
         
         for i in Genre_result:
            organize_search=Organize.objects.select_related().filter(organize_id = i)
            
            print('join리스트',organize_search)
            for i in organize_search:
               try:
                  user = Sign_up.objects.get(id=i.u_id)
                  user_name = user.user_id
               except:
                  user_name ="none"
               result_list.append(
               {
                  "year_date" : i.year_date,
                  "month_date" : i.month_date,
                  "day_date" : i.day_date,
                  "genre" : i.organize_id.genre_name,
                  "contents" : i.contents,
                  "img_file":i.img_file,
                  "uid" : user_name,
                  "hide_data":i.hide_data  
               }
            )
         print('result리스트타입',type(result_list))
         print('result리스트결과',result_list)
         
         return render(request,'yeon/search_result.html',{'result_list':result_list})
         # return JsonResponse(result_list,safe=False)
      else:
         form_data = Search_Form()
         return render(request,'yeon/search.html',{'form_data':form_data})
   else:
      print('로그인부터')
      return redirect('login')
      
# def old(): 수정전 방식
      id_list=[]
      
      if Genre_result.exists():
         for i in Genre_result:
            id_list.append(i.id)
            
         print('아이디_리스트:',id_list)   
         
         organize_result_list=[]
         organize_result_list2=[{'name':'aaaa'},{'name':'vvvvvvv'}]
         organize_result_list3={'name':'aaaa'}
         
         organize_result_list4=['aaaa','vvvvv']
         organize_result_list5 = "aaaa"
         
         
         for i in id_list:
            organize_id_search = Organize.objects.filter(organize_id = i)
            print('쿼리셋',organize_id_search)
            tmpJsonStr = serializers.serialize("json",organize_id_search)
            print('제이슨전',type(tmpJsonStr))
            tmpJsomObj = json.loads(tmpJsonStr)
            print('제이슨후',type(tmpJsomObj))
            organize_result_list.extend(tmpJsomObj)
            
         print('검색 결과 리스트:',organize_result_list)
            
         
         return JsonResponse(organize_result_list,safe=False)
         return HttpResponse(json.dumps(organize_result_list5), content_type = "application/json")
      
def all_list(request):
   # result_list = Organize.objects.extra(tables=['yeondaegi_app_Genre'],
   #                        where=['yeondaegi_app_Genre.id = yeondaegi_app_organize.organize_id'])
   login_user=request.session.get('user')

   if login_user:
      join_list = Organize.objects.select_related('organize_id')
      # print('결과',join_list)
      
      connecting_id = request.session.get('user')
      
      connecting_str = str(connecting_id)
      # connecting_str = Sign_up.objects.values('user_id').get(id=connecting_id)['user_id']
      
      try:
         following_user = Follow.objects.values('following').get(follower = connecting_str)['following']
         following_u_list = following_user.split(',')
      except:
         following_u_list = None
      

      # test=Organize.objects.get(pk=6)
      # a=test.like.all()
      # print('결과',a)
      # print('테스트',a.values('id').get(pk=login_user)['id'])
      
      

     
      result_list=[]
      
      for i in join_list:
         try:
            user = Sign_up.objects.get(id=i.u_id)
            user_name = user.user_id
         except:
            user_name ="none"

         
         post_like = i.like.all()    # i번째 글의 ManyToManyField의 테이블에 i번째글에 해당하는 sign_up 테이블 정보 가져온다
         try:
            like_check = post_like.values('id').get(pk=login_user)['id']
         except:
            like_check = None


         result_list.append(
            {
               "id":i.id,
               "year_date" : i.year_date,
               "month_date" : i.month_date,
               "day_date" : i.day_date,
               "genre" : i.organize_id.genre_name,
               "contents" : i.contents,
               "uid" : user_name,
               "img_file":i.img_file,
               "hide_data":i.hide_data,
               "int_uid":i.u_id,
               "str_uid":str(i.u_id),
               "like_check":like_check,
               
               
            }
         )
      #= print('result리스트',type(result_list))
      #    print('전체',res)
      #    print('분야',res.organize_id.genre_name)
      # tmpJsonStr = serializers.serialize("json",result_list)
      # tmpJsomObj = json.loads(tmpJsonStr)
      # return JsonResponse(result_list,safe=False)
      # return JsonResponse({"ok":"anta"},safe=False)
      
      return render(request,'yeon/all_list.html',{
         'result_list':result_list , 
         'connecting_id':connecting_id, 
         'following_u_list':following_u_list,
         
         }
         )
   else:
      print('로그인부터')
      return redirect('login')


def sign_up(request):
   if request.method == 'POST':
      print('포스트')
      sign_id = request.POST.get('user_id')
      sign_password =request.POST.get('password')
      sign_password_again =request.POST.get('password_again')
      print('아이디:',sign_id,'비번:',sign_password,'비번확인:',sign_password_again)
      res_data = {} 
      form_data = Sign_Form(request.POST)
            
      if Sign_up.objects.filter(user_id =sign_id).exists():
            messages.warning(request, "이미 존재하는 아이디 입니다.")
            # # res_data['message'] = '이미 존재하는 아이디 입니다'
            # # return render(request,'yeon/sign.html',{'form_data':form_data},res_data)
            
            return redirect('sign')
      elif sign_password == sign_password_again:
         form_data.save()
         print('가입완2')
         return redirect('login')
      else:
         print('비밀번호 다시 입력')
         return redirect('sign')
   
   
   form_data = Sign_Form()
   print('겟')
   return render(request,'yeon/sign.html',{'form_data':form_data})

def login(request):
   if request.method == 'POST':
      login_id = request.POST.get('user_id')
      login_password =request.POST.get('password')
      try:
         user_data =Sign_up.objects.get(user_id=login_id)
         if login_id == user_data.user_id:
            print('아이디 존재')
            if login_password == user_data.password:
               print('로그인 성공')
               request.session['user'] = user_data.id
               return redirect('my_list')
               # return JsonResponse({"ok":"anta"},safe=False)
               
            else:
               print('패스워드 틀림')
      except:
         print('아이디 존재X')
   
   form_data = Sign_Form(use_required_attribute=False)
   return render(request,'yeon/login.html',{'form_data':form_data})

def logout(request):
    request.session.pop('user')
    print('로그아웃 완료')
    return redirect('login')   
 
def home(request):
   print('홈페이지')
   user_id = request.session.get('user')
   print('세션',user_id)
   if user_id:
      return redirect('my_list')
   else:
      print('로그인부터')
      return redirect('login')
   
def my_list(request):
   user_id= request.session.get('user')
   s = request.POST.get('sort')
   print("sort=",s)
   if user_id:
      print('유저아이디',user_id)
      if s == "1":
         print("과거순")
         mylists = Organize.objects.select_related().filter(u_id__contains = user_id).order_by('year_date','month_date','day_date')
      else:
         mylists = Organize.objects.select_related().filter(u_id__contains = user_id).order_by('-year_date','-month_date','-day_date')
      print(mylists)
      return render(request,'yeon/mylist.html',{'mylists':mylists, 'sort':s})

   else:
      print('로그인부터')
      return redirect('login')
   
def my_delete(request,delete_id):
   user_id= request.session.get('user')
   if user_id:
      delete_data= Organize.objects.get(pk=delete_id)
      
      if delete_data.u_id == user_id:
         print('유저=삭제할 데이터')
         delete_data.delete()
         print('삭제완료')
         
         return redirect('my_list')
   else:
      print('로그인부터')
      return redirect('login')
   
def my_update(request,update_id):
   user_id= request.session.get('user')
   hide = request.POST.get('hide_check')
   if user_id:
      if request.method == "POST":
         print('하하',update_id)
         print('데이터',request)
         print('포스트')
         edit_data = Organize.objects.get(pk=update_id)
         print('request아이디',request.POST.get('u_id'))
         form_data= UpdateOrganize_Form(request.POST,request.FILES,instance=edit_data)
         genre_data=request.POST.get('genre_name')
         
         
         if user_id == int(request.POST.get('u_id')):
            print('유저동일')
            form_data.save()
            
            if hide == '1':
               print('hide값1')
               edit_data.hide_data= hide
               edit_data.save()
            else:
               print('hide값0')
               hide='0'
               edit_data.hide_data = hide
               edit_data.save()
            
            try:
               print('분야 이미 존재')
               genre = Genre.objects.get(genre_name =genre_data)
            except:
               print('분야 없음')
               genre = Genre(genre_name=genre_data)
               genre.save()
               
               
            edit_data.organize_id = genre
            edit_data.save()
            print('수정완')
         else:
            print('다른유저') 
         return redirect('my_list')
      
      else:
         print('겟')
         edit_data= Organize.objects.get(pk=update_id)
         print('수정데이터',edit_data)
         form_data= UpdateOrganize_Form(instance=edit_data)
         genre_form=UpdateGenre_Form()
         return  render(request,'yeon/update.html',{'form_data':form_data ,'genre_form':genre_form , 'edit_data':edit_data})
      
      
   else:
      print('로그인부터')
      return redirect('login')
   
def follow(request):
   login_user= request.session.get('user')
   
   if login_user:
      following_user = request.POST.get('following_id')
      print('팔로윙 유저', following_user)
      # follower_user = Sign_up.objects.values('user_id').get(id = login_user)['user_id']
      follower_u_int = Sign_up.objects.values('id').get(id=login_user)['id']
      follower_user = str(follower_u_int)
      print('팔로워 유저',type(follower_u_int))
      
      if following_user: 
         
         if Follow.objects.filter(follower = follower_user).exists():
            print('팔로워 유저 이미 존재')
            already_following = Follow.objects.values('following').get(follower = follower_user)['following']
            print('하하',already_following)
               
            select_follow = Follow.objects.get(follower=follower_user)
            select_follow.following = already_following + "," + following_user
            select_follow.save()
            print('팔로윙 저장완')
               
               
         else:
            print('팔로워 유저 존재x')
            Follow( follower = follower_user, following = following_user ).save()
            print('팔로워 저장완')
            
         return redirect('all_list')
      
      else:
         print('팔로윙값 없음')
         return redirect('all_list')
      
   
   else:
      print('로그인부터')
      return redirect('login')
   
def follow_clear(request):
   
   login_user= request.session.get('user')
   
   if login_user:
      following_user = request.POST.get('following_id')
      print('팔로윙 유저', following_user)
      
      login_u_str=str(login_user)
      follow_u_str=Follow.objects.values('following').get(follower = login_u_str)['following']
      print('리스트전',follow_u_str)
      
      following_u_list = follow_u_str.split(',')
      print('팔로윙리스트후',following_u_list)
      
      while following_user in following_u_list:
         following_u_list.remove(following_user)
      print('리스트결과',following_u_list)
      
      str_f =",".join(following_u_list)
      
      
      select_follow = Follow.objects.get(follower= login_u_str)
      select_follow.following = str_f
      select_follow.save()
      
      
      return redirect('all_list')
      
      
   else:
      print('로그인부터')
      return redirect('login')
      
def get_followers(login_u_str):
         follow_u_str=Follow.objects.values('following').get(follower = login_u_str)['following']
         print('리스트전',follow_u_str)
         
         following_u_list = follow_u_str.split(',')
         print('팔로윙리스트후',following_u_list)
     
      
         for i in following_u_list:
            if i =="":
               following_u_list.remove(i)
               
         print('공백 제거후',following_u_list)
      

         following_name=[]
         
         for i in following_u_list:
            a=int(i)
            try:
               data = Sign_up.objects.values('user_id').get(id = a)['user_id']
               following_name.append(data)
            except:
               pass
               
         print('팔로윙 이름',following_name)   
         
         following_dic = [{"id":0,"name":"전체"}]
         
         # x=0
         for i in range(len(following_u_list)):
            following_dic.append(
               {
                  "id":following_u_list[i],
                  "name":following_name[i]
               }
            )
            # x += 1
            
         print('팔로윙 최종 딕셔너리',following_dic)
         return following_dic
         
def follow_search(request):
   login_user= request.session.get('user')
   
   if login_user:
      
      login_u_str=str(login_user)
      try:         
         following_dic = get_followers(login_u_str)
         return render(request,'yeon/follow_result.html',{'following_dic':following_dic})
      
      except:
         return redirect('my_list')
   else:
      print('로그인부터')
      return redirect('login')
     
def get_posts(following_id):
   
      following_data = Organize.objects.select_related().filter(u_id = int(following_id))
      print('팔로윙데이터',following_data)
      
      result_list=[]
      for i in following_data:
               try:
                  user = Sign_up.objects.get(id=i.u_id)
                  user_name = user.user_id
               except:
                  user_name ="none"
               result_list.append(
                  {
                     "year_date" : i.year_date,
                     "month_date" : i.month_date,
                     "day_date" : i.day_date,
                     "genre" : i.organize_id.genre_name,
                     "contents" : i.contents,
                     "img_file":i.img_file,
                     "uid" : user_name,
                     "hide_data":i.hide_data  
                  }
               )
      return result_list
               
def following_search_result(request):
   login_user= request.session.get('user')
   
   if login_user:

      login_u_str=str(login_user)
      following_dic = get_followers(login_u_str)
      print('팔로윙딕',following_dic)

      following_id=request.POST.get('following_select')
      print('데이터',following_id)
      
      
      if following_id != '0':
         result_list=get_posts(following_id)
      else: 
         #x=1
         result_list=[]
         for i in range(len(following_dic)-1):
            a=get_posts(following_dic[i+1]['id'])
            result_list += a
            #x += 1
      
      return render(request,'yeon/follow_result.html',{'result_list':result_list,'following_dic':following_dic })
   
   else:
      print('로그인부터')
      return redirect('login')
   
def like(request,post_id):
   login_user= request.session.get('user')
   if login_user:
      sign_data = Sign_up.objects.get(pk=login_user)
      like_post = Organize.objects.get(pk=post_id)
      like_value = int(request.POST.get('html_like'))
      # 'html_like'==> all_list.html의 인풋값을 가져오기위한 name 값
      
      if like_value == 1:
         like_post.like.add(sign_data)
         like_post.like_count += like_value
         like_post.save()
         

      if like_value == -1:
         like_post.like.remove(sign_data)
         like_post.like_count -= like_value
         like_post.save()
         

      return redirect('all_list')
      
   else:
      print('로그인부터')
      return redirect('login')

def like_list(request,post2_id):
   login_user= request.session.get('user')
   if login_user:
      like_post = Organize.objects.get(pk=post2_id)
      like_object = like_post.like.all()

      l_list=[]
      for i in like_object:
         l_list.append(i.user_id)
      print('좋아요 리스트',l_list)

      return render(request,'yeon/like_list.html',{'like_list':l_list})

   else:
      print('로그인부터')
      return redirect('login')