from rest_framework import serializers

from rank.models import Client


class RankSerializer(serializers.ModelSerializer):
    client_num = serializers.SerializerMethodField(read_only=True)
    # rank_num = serializers.SerializerMethodField(read_only=True)
    rank_num = serializers.IntegerField(read_only=True)


    class Meta:
        model = Client
        fields = 'rank_num','client_num', 'score'

    def get_client_num(self, obj):
        return '客户端{}'.format(obj.client_num)

    # 优化查询次数，不用他
    # def get_rank_num(self, obj):
    #     clients = self.context.get('clients')
    #     self_score = obj.score
    #     max_count = clients.filter(score__gt=self_score).count()
    #     self_rank = max_count + 1
    #     return self_rank