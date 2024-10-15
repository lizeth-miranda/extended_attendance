{
    'name': 'Extended Attendance',
    'version': '1.1',
    'category': 'Human Resources',
    'depends': ['web', 'hr_attendance'],
    'data': [
        'security/extended_attendance_security.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_attendance_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'extended_attendance/static/src/js/my_attendances.js',
            'extended_attendance/static/src/js/greeting_message_extension.js',
        ],
    },
    'installable': True,
    'application': False,
}