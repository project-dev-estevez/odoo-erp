# models/purchase_requisition.py
from odoo import models, fields, api

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    def action_view_alternatives(self):
        # Obtener todas las alternativas relacionadas con esta solicitud
        alternatives = self.env['purchase.requisition.alternative'].search([('requisition_id', '=', self.id)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alternativas de Cotización',
            'res_model': 'purchase.requisition.alternative',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', alternatives.ids)],
            'target': 'current',
        }