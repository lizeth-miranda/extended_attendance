from odoo import models, fields, api, _
from datetime import timedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def attendance_manual(self, next_action, entered_pin=None):
        self.ensure_one()
        now = fields.Datetime.now()
        last_attendance = self.env['hr.attendance'].search([
            ('employee_id', '=', self.id)
        ], order='create_date desc', limit=1)
        
        if last_attendance:
            last_action_time = last_attendance.check_out or last_attendance.check_in
            if last_action_time + timedelta(minutes=3) > now:
                time_left = (last_action_time + timedelta(minutes=3) - now).total_seconds() / 60
                action_type = "salida" if last_attendance.check_out else "entrada"
                message = _("Error: No puede registrarse mas de una vez {action_type} en {time_left:.1f} minutos").format(action_type=action_type, time_left=time_left)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Advertencia'),
                        'message': message,
                        'type': 'warning',
                        'sticky': False,
                        'next': {
                            'type': 'ir.actions.client',
                            'tag': 'reload',
                        },
                    }
                }
        
        return super(HrEmployee, self).attendance_manual(next_action, entered_pin)

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    is_restricted_user = fields.Boolean(compute='_compute_is_restricted_user', store=False)

    @api.depends('employee_id')
    def _compute_is_restricted_user(self):
        restricted_group = self.env.ref('extended_attendance.group_attendance_restricted')
        for attendance in self:
            attendance.is_restricted_user = restricted_group in self.env.user.groups_id

    def write(self, vals):
        if self.env.user.has_group('extended_attendance.group_attendance_restricted'):
            if 'check_in' in vals or 'check_out' in vals:
                raise models.AccessError(_("No tienes los derechos para modificar los horarios de entrada o salida en un registro de asistencia."))
        return super(HrAttendance, self).write(vals)