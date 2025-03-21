# models/purchase_requisition_alternative.py
from odoo import models, fields

class PurchaseRequisitionAlternative(models.Model):
    _name = "purchase.requisition.alternative"
    _description = "Alternativas de Cotización"

    name = fields.Char(string="Nombre", required=True)
    requisition_id = fields.Many2one('purchase.requisition', string="Solicitud de Cotización")
    # Añade más campos según necesites (ej: producto, cantidad, proveedor, etc.)