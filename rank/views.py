from django.db.models import Q, Count, F, Window
from django.db.models.functions import Rank
from django.shortcuts import render

# Create your views here.
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rank.GetUserJWTAuthentication import GetUserJWTAuthentication
from rank.models import Client, User
from rank.paginations import MyPageNumberPagination
from rank.serializers import RankSerializer


class RankView(GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = RankSerializer
    authentication_classes = GetUserJWTAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, request):  # 传入客户端号和分数
        client_num = request.data.get('client_num')
        score = request.data.get('score')
        if self.get_queryset().filter(client_num=client_num).exists():
            client = self.get_queryset().filter(client_num=client_num).first()
            client.score = score
            client.save()
        else:
            client = Client(client_num=client_num, score=score)
            client.save()
        return Response({'code': 200, 'msg': '添加成功'})

    def get(self, request):
        user = request.user
        client = user.client
        queryset = self.get_queryset().annotate(
            rank_num=Window(
                expression=Rank(),
                order_by=F('score').desc()
            ),
        ).order_by('-score')
        my_client_num = client.client_num
        my_client = self.get_queryset().filter(client_num=my_client_num).first()
        my_score = my_client.score
        max_count = self.get_queryset().filter(score__gt=my_score).count()
        my_rank = max_count + 1
        paginator = MyPageNumberPagination()
        page_list = paginator.paginate_queryset(queryset, request, self)
        serializer = self.get_serializer(page_list, many=True, context={'clients': queryset})
        return Response({
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'code': status.HTTP_200_OK,
            'data': serializer.data,
            'my_data': {'rank_num': my_rank,
                        'client_num': '客户端{}'.format(my_client_num),
                        'score': my_score}
        })


class UserLoginView(TokenObtainPairView):
    """
    提供：username     password
    返回：refresh:刷新用     access：登陆用
    """
    permission_classes = AllowAny,
    serializer_class = TokenObtainPairSerializer
    authentication_classes = JWTAuthentication,

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            username = request.data.get('username')
            user = User.objects.filter(username=username).first()
            data = {
                'user_id': user.id,
                'msg': '登陆成功',
                'token': serializer.validated_data,
                'status': status.HTTP_200_OK,
            }
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(data)
