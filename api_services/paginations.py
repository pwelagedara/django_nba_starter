from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """Use pagination for responses with lists to prevent performance issues in the backend"""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100