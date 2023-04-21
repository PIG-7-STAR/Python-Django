# def calculate_total_duration(data):
#         result = {}
#         for item in data:
#             employee_id = item["employee"]
#             working_minutes = item["working_hour"]
#             if employee_id in result:
#                 result[employee_id]["total_duration"] += working_minutes
#             else:
#                 result[employee_id] = {
#                     "total_duration": working_minutes,
#                 }
#             if result[employee_id]["total_duration"] % 100 >= 60:
#                 result[employee_id]["total_duration"] += 40
#                 result[employee_id]["total_duration"] += 100

#         return result

def calculate_total_duration(data):
    result = {}
    for item in data:
        employeeId = item["employee"]["pk"]
        working_minutes = item["working_hour"]
        if employeeId in result:
            result[employeeId]["total_duration"] += working_minutes
        else:
            result[employeeId] = {
                "total_duration": working_minutes,
            }
        if result[employeeId]["total_duration"] % 100 >= 60:
            result[employeeId]["total_duration"] += 40
            result[employeeId]["total_duration"] += 100

    return result