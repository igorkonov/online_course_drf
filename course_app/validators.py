from rest_framework import serializers

from course_app.models import Course


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get('video')
        if video_url and 'www.youtube.com' not in video_url:
            raise serializers.ValidationError("Ссылки на сторонние ресурсы, кроме youtube.com, запрещены!")


class CourseIdValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        course = Course.objects.get(id=value)
        if not course:
            raise serializers.ValidationError(f"Курса c ID {value} не существует")
        return value
