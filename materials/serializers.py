from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('owner', None)  # убрать owner, если он передан, но нет в модели
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @extend_schema_field(int)
    def get_lessons_count(self, obj):
        return obj.lessons.count()

    @extend_schema_field(bool)
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.subscriptions.filter(user=user).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'created_at']
        read_only_fields = ['user', 'created_at']
