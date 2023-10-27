from rest_framework.routers import DefaultRouter

from authentication.views import UserViewSet
from office.views import OfficeViewSet
from role.views import RoleViewSet
from country.views import CountryViewSet
from survey.views import SurveyViewSet

router = DefaultRouter()

router.register('auth', UserViewSet)
router.register('office', OfficeViewSet)
router.register('role', RoleViewSet)
router.register('country', CountryViewSet)
router.register('survey', SurveyViewSet)
