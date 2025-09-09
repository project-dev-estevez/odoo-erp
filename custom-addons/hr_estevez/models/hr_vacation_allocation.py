from odoo import models, fields, api
from odoo.exceptions import UserError

class HrVacationAllocation(models.Model):
    _name = 'hr.vacation.allocation'
    _description = 'Asignación de Días de Vacaciones a Períodos'
    
    leave_id = fields.Many2one('hr.leave', string="Solicitud de Vacaciones", required=True, ondelete='cascade')
    period_id = fields.Many2one('hr.vacation.period', string="Período", required=True, ondelete='cascade')
    days = fields.Float(string="Días Asignados", required=True)
    employee_id = fields.Many2one('hr.employee', related='leave_id.employee_id', store=True)