from django.db.models import Avg
from django.db.models.functions import TruncHour

from blog.celery import app
from posts.models import Post, Review


@app.task(name="update_avg_of_posts")
def update_avg_of_post(post_pk):
    post = Post.objects.get(pk=post_pk)
    avg_rate = Review.objects.filter(post=post, is_fake=False) \
        .annotate().annotate(hour=TruncHour("created_at")).values('hour') \
        .annotate(avg_per_hour=Avg("rate")).order_by("hour").aggregate(avg_rate=Avg("avg_per_hour"))["avg_rate"]
    post.avg_rate = avg_rate
    post.avg_user_count = Review.objects.filter(post=post, is_fake=False).count()
    post.save()
