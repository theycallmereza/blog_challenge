from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post


@receiver(post_save, sender=Post)
def update_match_ticket_cache(sender, instance, *args, **kwargs):
    if not instance.word_count:
        instance.set_word_count()
