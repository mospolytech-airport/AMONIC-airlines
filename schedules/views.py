import tablib
from django.views.decorators.csrf import csrf_protect
from import_export.formats.base_formats import XLSX
from import_export import resources

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
        # Does not work correctly
        data_fields = ('id', 'Date', 'Time', 'Aircraft', 'Route', 'EconomyPrice', 'Confirmed', 'FlightNumber')
        if request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']

            schedule_resource = ScheduleResource()
            dataset = tablib.Dataset()
            dataset.load(excel_file.read(), format='xlsx')

            success_count = 0
            duplicate_count = 0
            missing_fields_count = 0
            
            for row in dataset:
                row = dict(map(lambda x, y: (x, y), data_fields, row))

                serializer = ScheduleSerializer(data=row)

                if serializer.is_valid():
                    existing_schedule = Schedule.objects.filter(
                        Date=row['Date'],
                        Time=row['Time'],
                        Aircraft=row['Aircraft'],
                        Route=row['Route'],
                        EconomyPrice=row['EconomyPrice'],
                        Confirmed=row['Confirmed'],
                        FlightNumber=row['FlightNumber']
                    ).first()
                    
                    if existing_schedule:
                        duplicate_count += 1
                        continue


                    serializer.save()
                    success_count += 1
                else:
                    print(serializer.errors)
                    missing_fields_count += 1

            return Response({
                'success_count': success_count,
                'duplicate_count': duplicate_count,
                'missing_fields_count': missing_fields_count,
            }, status=status.HTTP_200_OK)

        else:
            return Response({'success': False, 'message': 'No Excel file provided'}, status=status.HTTP_400_BAD_REQUEST)