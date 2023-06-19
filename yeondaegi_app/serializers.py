from rest_framework import serializers
from yeondaegi_app.models  import Genre,Sign_up,Organize,Follow,DRF_Follow

class Organize_Serializer(serializers.ModelSerializer):
    # 괄호안 required=False 는 빈 파일 허용 여부를 지정 false가 빈파일 허용
    img_file = serializers.ImageField(use_url=True,required=False)
    

    class Meta:
        model = Organize
        fields =['id','year_date','month_date','day_date','organize_id','contents','u_id','img_file','like','like_count']
        read_only_fields = ['like','like_count','like_drf','like_count_drf']

class DRF_Follow_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DRF_Follow
        fields = '__all__'

class Like_Serializer(serializers.Serializer):
    like_count = serializers.IntegerField(read_only=True)
    like_list = serializers.CharField(read_only=True)