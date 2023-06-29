from django.urls import path
from rest_framework.routers import DefaultRouter

from course_app.apps import CourseAppConfig
from course_app.views import CourseViewSet, LessonListView, LessonCreateView, LessonDeleteView, LessonDetailView, LessonUpdateView

app_name = CourseAppConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/detail/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
] + router.urls
