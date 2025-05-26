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
    "depends": ['base', 'hr', 'hr_estevez', 'hr_recruitment', 'survey', 'hr_recruitment_survey', 'utm'],
    "data": [
        # Archivos de seguridad
        "security/hr_recruitment_security.xml",
        "security/ir.model.access.csv",
        
        # Archivos de datos
        "data/hr_requisition_uniform_data.xml",
        "data/hr_requisition_epp_data.xml",
        "data/ir_cron_first_stage_data.xml",
        "data/ir_cron_interviews_data.xml",
        "data/ir_cron_psychometric_data.xml",
        "data/ir_cron_driving_test_data.xml",
        # 'data/mail_templates_inherit.xml',

        # Archivos de informes
        'report/hr_applicant_doctor_report.xml',
        'report/hr_applicant_doctor_report_templates.xml',
        
        # Archivos de vistas
        'views/hr_applicant_document_views.xml',
        'views/hr_applicant_view_form_inherit.xml',
        'views/hr_candidate_view_form_inherit.xml',
        "views/hr_requisition_views.xml",
    ],
    "installable": True,
    "application": False,
    "i18n": ["i18n/es_419.po", "i18n/es.po"],
}