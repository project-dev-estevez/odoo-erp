# -*- coding: utf-8 -*-
{
    "name": "Reclutamiento Estevez",
    "summary": "Extensión del módulo de reclutamiento para Estevez.Jor",
    "description": """
        Este módulo extiende el módulo de reclutamiento para agregar la lógica de negocio de Estevez.Jor
    """,
    "author": "Estevez.Jor",
    "website": "https://estevezjorinternacional.com",
    "category": "Human Resources",
    "version": "0.1",
    "depends": ["hr", "hr_estevez", "hr_recruitment"],
    "data": [
        "security/ir.model.access.csv",
        'views/hr_applicant_view_form_inherit.xml',
        "data/hr_requisition_uniform_data.xml",
        "data/hr_requisition_epp_data.xml",
        "views/hr_requisition_views.xml",
    ],
    "installable": True,
    "application": False,
}