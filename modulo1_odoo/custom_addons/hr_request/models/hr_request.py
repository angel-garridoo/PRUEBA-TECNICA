# hr_request/models/hr_request.py
from odoo import models, fields, api
# pyrefly: ignore [missing-import]
from odoo.exceptions import UserError 


class HrRequest(models.Model):

    _name = 'hr.request'

    _description = 'Solicitud Interna de Empleado'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    nombre = fields.Char(
        string='Nombre de la Solicitud',
        required=True,
        tracking=True
    )


    tipo = fields.Selection(
        selection=[
            ('vacaciones', 'Vacaciones'),
            ('permiso', 'Permiso'),
            ('anticipo', 'Anticipo'),
            ('otro', 'Otro'),
        ],
        string='Tipo de Solicitud',
        required=True,
        tracking=True
    )

    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado',
        required=True,
        ondelete='restrict',
        tracking=True
    )

    fecha_solicitud = fields.Date(
        string='Fecha de Solicitud',
        default=fields.Date.today,
        required=True
    )

    estado = fields.Selection(
        selection=[
            ('nuevo', 'Nuevo'),
            ('aprobado', 'Aprobado'),
            ('rechazado', 'Rechazado'),
        ],
        string='Estado',
        default='nuevo',
        required=True,
        tracking=True
    )

    observaciones = fields.Text(
        string='Observaciones'
    )

    def action_aprobar(self):
        """
        Cambia el estado a 'aprobado'.
        'self' puede ser un solo registro o varios (Odoo trabaja con recordsets).
        El bucle for garantiza que funcione en ambos casos.
        """
        for record in self:
            if record.estado != 'nuevo':
                raise UserError(
                    'Solo se pueden aprobar solicitudes en estado Nuevo.'
                )

            record.write({'estado': 'aprobado'})

    def action_rechazar(self):
        """
        Cambia el estado a 'rechazado'.
        Misma lógica que aprobar.
        """
        for record in self:
            if record.estado != 'nuevo':
                raise UserError(
                    'Solo se pueden rechazar solicitudes en estado Nuevo.'
                )
            record.write({'estado': 'rechazado'})
