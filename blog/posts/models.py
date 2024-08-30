from django.db import models
from django.contrib.auth.models import User


class ExcludeFakesModelManager(models.Manager):
    """
    This Manager Use to override default manager of rate model.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_fake=False)


class BaseTimeAbstractModel(models.Model):
    """
    Time abstract model to let other models inherit and avoid code duplicate
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseTimeAbstractModel):
    title = models.CharField(max_length=127)
    text = models.TextField()
    avg_rate = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    avg_user_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.title


class Review(BaseTimeAbstractModel):
    RATE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_reviews")
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="post_reviews")
    rate = models.SmallIntegerField(choices=RATE_CHOICES)
    is_fake = models.BooleanField(default=False)

    # you can use this manager if you need all objects in this model
    all_objects = models.Manager()
    # Exclude fake rates by default
    objects = ExcludeFakesModelManager()

    class Meta:
        unique_together = ["user", "post"]
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.post.title} - {str(self.rate)}"
