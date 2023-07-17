from datetime import datetime
from submisssion.models import CalendarCutiSubmission
from userapp.models import Log, User


def create_calendar(employee_id, type, reason_emp, start_dates, end_dates):
    employees = User.objects.get(id=employee_id)
    start_date = datetime.strptime(start_dates, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_dates, '%Y-%m-%d').date()

    calendar = CalendarCutiSubmission.objects.filter(
        employee=employees,
        title=type,
        permission_type=type,
        reason=reason_emp,
        start=start_date
    )
    if not calendar.exists():
        CalendarCutiSubmission.objects.create(
            employee=employees,
            title=type,
            permission_type=type,
            reason=reason_emp,
            start=start_date,
            end=end_date
        )
        create_log(f"membuat calendar cuti untuk user {employees.name}", action="post")


def delete_calendar(employee_id, type, reason_emp, start_dates):
    employees = User.objects.get(id=employee_id)
    start_date = datetime.strptime(start_dates, '%Y-%m-%d')

    calendar = CalendarCutiSubmission.objects.filter(
        employee=employees,
        title=type,
        permission_type=type,
        reason=reason_emp,
        # start=start_date
    )
    print(calendar)
    if calendar.exists():
        calendar.delete()
    else:
        create_log("Calendar cuti tidak ditemukan.", action='delete')

def create_log(message, action):
    Log.objects.create(message=message, action=action)