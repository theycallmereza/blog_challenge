from django.db.models import OuterRef, Subquery
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from posts.models import Post, Review
from posts.serializers import ListPostSerializer, PostSerializer, AddRateByUserSerializer


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
        if self.action == "rate":
            return AddRateByUserSerializer
        return PostSerializer

    @action(methods=["POST"], detail=True)
    def rate(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        try:
            review = Review.objects.get(post=post, user=user)
        except Review.DoesNotExist:
            review = None
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, instance=review)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, post=post)
        return Response({"status": "success"})
