import unittest
from odoo.tests import common, tagged
from datetime import datetime, timedelta
import random

@tagged('post_install', '-at_install')
class TestExtendedAttendance(common.TransactionCase):
    def setUp(self):
        super(TestExtendedAttendance, self).setUp()
        self.env = self.env(context=dict(self.env.context, tracking_disable=True))
        self.employee_model = self.env['hr.employee']
        self.attendance_model = self.env['hr.attendance']
        
        # Limpiar registros de asistencia existentes
        self.attendance_model.search([]).unlink()

    def test_multiple_attendances(self):
        """Test creating multiple attendance records for 300 employees"""
        employees = self.employee_model.create([{'name': f'Employee {i}'} for i in range(300)])
        all_attendances = []

        for employee in employees:
            last_checkout = datetime.now() - timedelta(days=31)
            for _ in range(5):
                check_in_time = last_checkout + timedelta(hours=random.randint(1, 24))
                check_out_time = check_in_time + timedelta(hours=random.randint(1, 12))

                attendance = self.attendance_model.create({
                    'employee_id': employee.id,
                    'check_in': check_in_time,
                    'check_out': check_out_time,
                })

                all_attendances.append(attendance)
                last_checkout = check_out_time

                self.assertTrue(attendance.id, "El registro de asistencia no se creó correctamente")
                self.assertEqual(attendance.employee_id, employee, "El empleado no coincide")
                self.assertTrue(attendance.check_in, "No se registró el check-in")
                self.assertTrue(attendance.check_out, "No se registró el check-out")
                self.assertTrue(attendance.check_out > attendance.check_in, "El check-out debe ser posterior al check-in")

        self.assertEqual(len(all_attendances), 1500, "No se crearon exactamente 1500 registros de asistencia")

        print(f"\n\033[92m===== Resumen de registros de asistencia creados =====\033[0m")
        print(f"Total de empleados: {len(employees)}")
        print(f"Total de registros de asistencia: {len(all_attendances)}")
        print(f"Promedio de registros por empleado: {len(all_attendances) / len(employees)}")

        # Mostrar algunos ejemplos de registros
        sample_size = min(10, len(all_attendances))
        print(f"\nMostrando {sample_size} registros de ejemplo:")
        for attendance in random.sample(all_attendances, sample_size):
            print(f"Empleado: {attendance.employee_id.name}")
            print(f"Check-in:  {attendance.check_in}")
            print(f"Check-out: {attendance.check_out}")
            print(f"Duración:  {attendance.check_out - attendance.check_in}")
            print("---")

        print(f"\n\033[92m===== Se crearon y verificaron exitosamente {len(all_attendances)} registros de asistencia para {len(employees)} empleados =====\033[0m")

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExtendedAttendance)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("\n\033[92m===== All Extended Attendance tests executed successfully! =====\033[0m\n")
    else:
        print("\n\033[91m===== Some Extended Attendance tests failed. Please check the output above. =====\033[0m\n")

if __name__ == '__main__':
    run_tests()