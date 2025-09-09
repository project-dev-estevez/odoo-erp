from odoo import models, fields

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    is_vacation = fields.Boolean(
        string='Es Vacación',
        help='Marque esta casilla si este tipo de ausencia es para vacaciones'
    )