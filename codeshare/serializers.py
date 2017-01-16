from rest_framework import serializers

from models import CourseAccess


class CourseAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseAccess
        fields = ('access',)
