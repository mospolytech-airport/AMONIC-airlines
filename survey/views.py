from rest_framework import viewsets

from survey.models import Survey
from survey.serializers import SurveySerializer


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
