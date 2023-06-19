from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm
from yeondaegi_app.models import Sign_up,Organize,Genre

class Organize_Form(forms.Form):
    year_date = forms.IntegerField(label='년도')
    month_date = forms.IntegerField(label='월')
    day_date = forms.IntegerField(label='일')
    organize_id = forms.CharField(label='분야',max_length=20)
    contents = forms.CharField(label='내용',max_length=500)
    img_file = forms.ImageField(label='파일 올리기')
    
    
class Search_Form(forms.Form):
    search_form = forms.CharField(label='분야 검색',max_length=30)
    

class Sign_Form(ModelForm):
    class Meta:
        model = Sign_up
        fields =['user_id','password','password_again']
        labels={
            'user_id':_('아이디'),
            'password':_('비밀번호'),
            'password_again':_('비밀번호 확인')
        }
        help_texts ={
            'user_id':_('아이디를 입력하세요' ),
            'password':_('비밀번호를 입력하세요'),
            'password_again':_('비밀번호 다시 입력하세요')
        }
        widgets={
             'password': forms.PasswordInput()
        
         }
        error_messages = {
            'user_id': {
                'max_length':_('아이디가 너무 깁니다.20자 이하로')
            },
            'password': {
                'max_length':_('비밀번호가 너무 깁니다.20자 이하로')
            },
            'password_again': {
                'max_length':_('비밀번호가 너무 깁니다.20자 이하로')
            }
            
            }

class Login_Form(Sign_Form):
    class Meta:
        model = Sign_up
        exclude=['password']
        


class UpdateOrganize_Form(ModelForm):
    class Meta:
        model = Organize
        fields = ['year_date','month_date','day_date','organize_id','contents','u_id','img_file']
        labels = {
            'year_date':_('년도'),
            'month_date':_('월'),
            'day_date':_('일'),
            # 'organize_id':_('분야'),
            'contents':_('내용'),
            'img_file':_('이미지 업로드')
        }
        widgets = {
            'u_id':forms.HiddenInput(),
            'organize_id':forms.HiddenInput(),
        }
        
        help_texts ={
            'year_date':_('년도를 입력하세요'),
            'month_date':_('월을 입력하세요'),
            'day_date':_('일을 입력하세요'),
            # 'organize_id':_('분야를 입력하세요'),
            'contents':_('내용을 입력하세요'),
            
        } 
        
class UpdateGenre_Form(forms.Form):
    genre_name = forms.CharField(label='분야',max_length=20)

        