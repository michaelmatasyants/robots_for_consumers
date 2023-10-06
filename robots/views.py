import json
from datetime import date, timedelta
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse
from django.utils.timezone import make_aware, datetime
from django.db.models import Count
from .models import Robot
from .forms import RobotCreationForm


@csrf_exempt
def create_robot(request):
    '''Create new Robot instance for the db, based on the received json file'''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        model, version = data.get('model'), data.get('version')
        robot_data = {
            'serial': f'{model}-{version}',
            'model': model,
            'version': version,
            'created': make_aware(datetime.strptime(data.get('created'),
                                                    '%Y-%m-%d %H:%M:%S')),
        }
        robot_form = RobotCreationForm(robot_data)
        if robot_form.is_valid():
            robot, created = Robot.objects.get_or_create(**robot_data)
            if created:
                data = {'message': 'Produced robot with serial number: '
                                   f'{robot.serial} added to Robot'}
            else:
                data = {'message': f'Robot with serial number: {robot.serial} '
                                   'has been already added before'}
            return JsonResponse(data, status=201)
        else:
            return JsonResponse({'error': 'Invalid Json data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'},
                            status=405)


@csrf_exempt
def get_all_robots(request):
    '''Fetches all robots from Robot and returns in dict'''
    if request.method == 'GET':
        data = {
            'robots_qt': Robot.objects.count(),
            'robots': [{'serial': robot.serial,
                        'model': robot.model,
                        'version': robot.version,
                        'created': robot.created}
                       for robot in Robot.objects.all()]
        }
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'},
                            status=405)


def get_production_report(request):
    end_period = date.today()
    start_period = end_period - timedelta(days=6)
    distinct_models = Robot.objects.filter(created__gte=start_period)  \
                           .values_list('model', flat=True).distinct()  \
                           .order_by('model')
    report_name = 'Отчет по производству роботов за последнюю неделю.xlsx'
    with pd.ExcelWriter(report_name) as excel_writer:
        for model in distinct_models:
            robots_by_model = Robot.objects  \
                .filter(created__gte=start_period, model=model)  \
                .values('model', 'version')  \
                .annotate(produced_robots_qty=Count('serial'))
            df = pd.DataFrame(list(robots_by_model))
            df.columns = ['Модель', 'Версия', 'Количество за неделю']
            df.to_excel(excel_writer,
                        engine='xlsxwriter',
                        sheet_name=model,
                        index=False)
    return FileResponse(open(report_name, 'rb'))
