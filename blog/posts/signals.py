from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post, Review
from posts.tasks import update_avg_of_post


@receiver(post_save, sender=Post)
def update_match_ticket_cache(sender, instance, *args, **kwargs):
    if not instance.word_count:
        instance.set_word_count()


@receiver(post_save, sender=Review)
def update_post_avg(sender, instance, *args, **kwargs):
    post = instance.post
    update_avg_of_post.s(post.pk).apply_async()
