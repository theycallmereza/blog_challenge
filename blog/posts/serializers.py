from rest_framework import serializers

from posts.models import Post, Review


class PostSerializer(serializers.ModelSerializer):
    current_user_rate = serializers.SerializerMethodField()

    def get_current_user_rate(self, obj):
        return obj.current_user_rate if hasattr(obj, "current_user_rate") else None

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "text",
            "avg_rate",
            "avg_user_count",
            "current_user_rate",
        )


class ListPostSerializer(serializers.ModelSerializer):
    current_user_rate = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_current_user_rate(self, obj):
        return obj.current_user_rate if hasattr(obj, "current_user_rate") else None

    def get_text(self, obj):
        return obj.text[:150]

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "text",
            "avg_rate",
            "avg_user_count",
            "current_user_rate",
        )


class AddRateByUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "rate",
        )
