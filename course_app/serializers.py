from rest_framework import serializers

from course_app.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "name",
            "description",
            "preview",
            "video",
        )


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True)

    def get_lessons_count(self, instance):
        lessons = Lesson.objects.filter(course=instance).all()
        if lessons:
            return lessons.count()
        return 0

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
        )
