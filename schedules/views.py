import logging
import pandas as pd
import math
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from aircrafts.models import Aircraft
from aircrafts.serializers import AircraftSerializer
from airoutes.models import Route
from airoutes.serializers import RouteSerializer
from schedules.models import Schedule
from schedules.admin import ScheduleResource
from schedules.serializers import ScheduleSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    @action(methods=['post'], detail=False, permission_classes=[IsAdminUser], url_path='import')
    def import_excel(self, request):

        if request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']

            success_count = 0
            duplicate_count = 0
            missing_fields_count = 0

            try:
                df = pd.read_excel(excel_file)

                for index, row in df.iterrows():
                    # Проверка
                    is_empty = row.isnull().any()

                    if is_empty.any():
                        missing_fields_count += 1
                        continue
                    
                    row['Date'] = pd.to_datetime(row['Date']).date()
                    row['Time'] = pd.to_datetime(row['Time']).time()
                    aircraft = int(row['Aircraft'])
                    route = row['Route']

                    try:
                        
                        aircraft = Aircraft.objects.get(id=aircraft)
                        route = Route.objects.get(id=route)
                    except Aircraft.DoesNotExist:
                        missing_fields_count += 1
                        continue
                    except Route.DoesNotExist:
                        missing_fields_count += 1
                        continue

                    # Создание объекта для сериализации
                    schedule_data = {
                        'Aircraft': {'id': aircraft.id, 'Name': aircraft.Name, 'MakeModel': aircraft.MakeModel, 'TotalSeats': aircraft.TotalSeats, 'EconomySeats': aircraft.EconomySeats, 'BusinessSeats': aircraft.BusinessSeats},
                        'Route': {'id': route.id, 'DepartureAirport': {'id': route.DepartureAirport.id, 'IATACode': route.DepartureAirport.IATACode, 'Name': route.DepartureAirport.Name, 'CountryID': route.DepartureAirport.CountryID.id}, 'ArrivalAirport': {'id': route.ArrivalAirport.id, 'IATACode': route.ArrivalAirport.IATACode, 'Name': route.ArrivalAirport.Name, 'CountryID': route.ArrivalAirport.CountryID.id}, 'Distance': route.Distance, 'FlightTime': route.FlightTime},
                        'Confirmed': row['Confirmed'],
                        'Date': row['Date'],
                        'Time': row['Time'],
                        'EconomyPrice': row['EconomyPrice'],
                        'FlightNumber': row['FlightNumber'],
                    }
                    duplicated = Schedule.objects.get(id=row['id'])
                    if duplicated:
                        serializer = ScheduleSerializer(duplicated, data=schedule_data)
                        if (duplicated.Aircraft.id == aircraft.id 
                                and duplicated.Route.id == route.id 
                                and duplicated.Confirmed == row['Confirmed'] 
                                and duplicated.Date == row['Date'] 
                                and duplicated.Time == row['Time'] 
                                and int(duplicated.EconomyPrice) == int(row['EconomyPrice']) 
                                and int(float(duplicated.FlightNumber)) == int(float(row['FlightNumber']))):
                            duplicate_count += 1
                            continue
                        if serializer.is_valid():
                            serializer.save()
                            success_count += 1
                    serializer = ScheduleSerializer(data=schedule_data)
                    if serializer.is_valid():
                        serializer.save()
                        success_count += 1
                    else:
                        print(serializer.errors)

                result = {
                    'success_count': success_count,
                    'missing_fields_count': missing_fields_count,
                    'duplicate_count': duplicate_count,
                }
                return Response(result)
            except Exception as Argument: 
                logging.exception("Error") 
                return Response({'success': False, 'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'success': False, 'message': 'No Excel file provided'}, status=status.HTTP_400_BAD_REQUEST)