from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10  # 每页现实的数据条数
    page_size_query_param = 'size'  # 设置了每页大小的参数名为size即  ?page=xx&size=??
    max_page_size = 10  # 每页可以展示的最大数据条数


