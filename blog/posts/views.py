from django.db.models import OuterRef, Subquery
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from posts.models import Post, Review
from posts.serializers import ListPostSerializer, PostSerializer


class PostViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Post.objects.none()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.request.user.is_authenticated:
            current_user_reviews = Review.objects.filter(post=OuterRef("pk"), user=self.request.user)
            queryset = Post.objects.annotate(current_user_rate=Subquery(current_user_reviews.values("rate")))
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ListPostSerializer
        return PostSerializer
