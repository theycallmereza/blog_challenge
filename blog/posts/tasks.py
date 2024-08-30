from datetime import timedelta

from django.db.models import Avg, Count, Q
from django.utils import timezone

from blog.celery import app
from posts.models import Post


@app.task(name="update_avg_of_posts")
def update_avg_of_posts():
    posts = Post.objects.filter(post_reviews__updated_at__gte=timezone.now() - timedelta(minutes=30)) \
        .annotate(reviews_avg_rate=Avg("post_reviews__rate", filter=Q(post_reviews__is_fake=False))) \
        .annotate(reviews_avg_user_count=Count("post_reviews", filter=Q(post_reviews__is_fake=False)))
    for post in posts:
        post.avg_rate = post.reviews_avg_rate
        post.avg_user_count = post.reviews_avg_user_count
        post.save()
