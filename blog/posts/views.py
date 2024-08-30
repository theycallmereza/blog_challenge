from datetime import timedelta
from django.core.cache import cache
from django.db.models import OuterRef, Subquery
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from posts.models import Post, Review
from posts.serializers import ListPostSerializer, PostSerializer, AddRateByUserSerializer
from posts.const import POST_DETAIL_TIME_CACHE_KEY


class PostViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Post.objects.none()
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        response = super(PostViewSet, self).retrieve(request, *args, **kwargs)
        cache_key = POST_DETAIL_TIME_CACHE_KEY.format(user_id=request.user.pk, post_id=kwargs.get("pk"))
        cache.set(cache_key, timezone.now(), 600)
        return response

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
        is_fake = False
        post = self.get_object()
        user = request.user
        try:
            review = Review.objects.get(post=post, user=user)
        except Review.DoesNotExist:
            review = None
        if not review:
            cache_key = POST_DETAIL_TIME_CACHE_KEY.format(user_id=user.pk, post_id=post.pk)
            start_read_time = cache.get(cache_key)
            if start_read_time + timedelta(minutes=post.get_fastest_read_time()) > timezone.now():
                is_fake = True
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, instance=review)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, post=post, is_fake=is_fake)
        return Response({"status": "success"})
