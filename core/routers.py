from rest_framework.routers import DefaultRouter

from authentication.views import UserViewSet
from office.views import OfficeViewSet
from role.views import RoleViewSet
from country.views import CountryViewSet
from schedules.views import ScheduleViewSet
from survey.views import SurveyViewSet
from airports.views import AirportViewSet
from tickets.views import TicketViewSet
from amenities.views import AmenityViewSet
from cabintypes.views import CabinTypeViewSet
from amenitiesCabinType.views import CabinTypeAmenityViewSet
from amenitiesTickets.views import AmenityTicketViewSet

router = DefaultRouter()

router.register('auth', UserViewSet)
router.register('office', OfficeViewSet)
router.register('role', RoleViewSet)
router.register('country', CountryViewSet)
router.register('schedules', ScheduleViewSet)
router.register('survey', SurveyViewSet)
router.register('airport', AirportViewSet)
router.register('tickets', TicketViewSet)
router.register('amenity', AmenityViewSet)
router.register('cabintype', CabinTypeViewSet)
router.register('amenity-cabin', CabinTypeAmenityViewSet)
router.register('amenity-ticket', AmenityTicketViewSet)
