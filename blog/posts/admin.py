from django.contrib import admin
from posts.models import Post, Review


class PostAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    raw_id_fields = ("post", "user")


admin.site.register(Post, PostAdmin)
admin.site.register(Review, ReviewAdmin)
