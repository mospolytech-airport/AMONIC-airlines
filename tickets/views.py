from django.forms import model_to_dict
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from aircrafts.models import Aircraft
from airoutes.models import Route
from schedules.models import Schedule
from airports.models import Airport
from tickets.models import Ticket
from tickets.serializers import TicketSerializer


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    outbound_schedules: list[Schedule] = []
    return_schedules: list[Schedule] = []

    def get_value(self, model, key):
        try:
            obj = model_to_dict(model)

            return obj.get(key)
        except Exception as e:
            print('error', e)

    def search_schedule(self, from_airport: str, to_airport: str, date: str, schedules: list[Schedule]):
        from_airport_model = Airport.objects.get(IATACode=from_airport)
        to_airport_model = Airport.objects.get(IATACode=to_airport)

        try:
            route = Route.objects.get(DepartureAirport=from_airport_model, ArrivalAirport=to_airport_model)
            schedule = Schedule.objects.get(Date=date, Route=route)

            if schedule:
                schedules.append(schedule)
        except ObjectDoesNotExist:
            middle_routes = Route.objects.filter(DepartureAirport=from_airport_model)

            for middle_route in middle_routes:
                middle_route_from_airport_id = self.get_value(middle_route, 'ArrivalAirport')
                middle_route_from = Airport.objects.get(id=middle_route_from_airport_id)

                try:
                    first_part_route = Route.objects.get(DepartureAirport=from_airport_model, ArrivalAirport=middle_route_from)
                    second_part_route = Route.objects.get(DepartureAirport=middle_route_from, ArrivalAirport=to_airport_model)

                    first_part_schedule = Schedule.objects.get(Date=date, Route=first_part_route)
                    second_part_schedule = Schedule.objects.get(Date=date, Route=second_part_route)

                    if first_part_schedule:
                        schedules.append(first_part_schedule)

                    if second_part_schedule:
                        schedules.append(second_part_schedule)
                except ObjectDoesNotExist:
                    return

    @action(methods=['POST'], detail=False, url_path='search')
    def search_flights(self, request):
        # user = User.objects.get(id=request.user.id)
        from_airport = request.data.get('from_airport')
        to_airport = request.data.get('to_airport')
        cabin_type = request.data.get('cabin_type')
        outbound_date = request.data.get('outbound_date')
        return_date = request.data.get('return_date')

        is_economy = cabin_type == 'economy'

        self.outbound_schedules = []

        try:
            self.search_schedule(from_airport, to_airport, outbound_date, self.outbound_schedules)
        except Exception as e:
            return Response({"error": e})

        if return_date:
            self.return_schedules = []

            try:
                self.search_schedule(to_airport, from_airport, return_date, self.return_schedules)
            except Exception as e:
                return Response({"error": e})

        def filter_schedule_by_class(schedule: Schedule) -> bool:
            aircraft_id = self.get_value(schedule, 'Aircraft')
            aircraft = Aircraft.objects.get(id=aircraft_id)
            economy_seats = self.get_value(aircraft, 'EconomySeats')
            business_seats = self.get_value(aircraft, 'BusinessSeats')

            if is_economy and economy_seats:
                return True

            if not is_economy and business_seats:
                return True

            return False

        def schedule_adapter(schedules: list[Schedule]):
            dates = []
            times = []
            flight_numbers = []
            price = 0
            ids = []
            routes = []

            for schedule in schedules:
                date = self.get_value(schedule, 'Date')
                time = self.get_value(schedule, 'Time')
                route_id = self.get_value(schedule, 'Route')
                route = Route.objects.get(id=route_id)
                departure_airport_id = self.get_value(route, 'DepartureAirport')
                arrival_airport_id = self.get_value(route, 'ArrivalAirport')
                departure_airport_code = self.get_value(Airport.objects.get(id=departure_airport_id), 'IATACode')
                arrival_airport_code = self.get_value(Airport.objects.get(id=arrival_airport_id), 'IATACode')

                ids.append(self.get_value(schedule, 'id'))
                dates.append(date)
                times.append(time)
                routes.append({
                    'from': departure_airport_code,
                    'to': arrival_airport_code
                })
                flight_numbers.append(self.get_value(schedule, 'FlightNumber'))
                price += float(self.get_value(schedule, 'EconomyPrice'))

            return {
                'ids': ids,
                'routes': routes,
                'date': dates,
                'time': times,
                'flight_number': flight_numbers,
                'price': price,
                'number_of_stops': len(flight_numbers)
            }

        filter(filter_schedule_by_class, self.outbound_schedules)
        outbound_response = schedule_adapter(self.outbound_schedules)

        return_response = None

        if return_date:
            filter(filter_schedule_by_class, self.return_schedules)
            return_response = schedule_adapter(self.return_schedules)

        return Response({
            'outbound': outbound_response,
            'return': return_response
        })
