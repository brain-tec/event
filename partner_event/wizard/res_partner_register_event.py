# -*- coding: utf-8 -*-
# © 2014 Tecnativa S.L. - Pedro M. Baeza
# © 2015 Tecnativa S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Antonio Espinosa
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ResPartnerRegisterEvent(models.TransientModel):
    _name = 'res.partner.register.event'

    event = fields.Many2one('event.event', required=True)
    errors = fields.Text(readonly=True)

    def _prepare_registration(self, partner):
        return {
            'event_id': self.event.id,
            'partner_id': partner.id,
            'name': partner.name,
            'email': partner.email,
            'phone': partner.phone,
            'date_open': fields.Datetime.now(),
        }

    @api.multi
    def button_register(self):
        registration_obj = self.env['event.registration']
        errors = []
        for partner in self.env['res.partner'].browse(
                self.env.context.get('active_ids', [])):
            try:
                with self.env.cr.savepoint():
                    registration_obj.create(
                        self._prepare_registration(partner))
            except:
                errors.append(partner.name)
        if errors:
            self.errors = '\n'.join(errors)
            data_obj = self.env.ref('partner_event.'
                                    'res_partner_register_event_view')
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': [data_obj.id],
                'res_id': self.id,
                'target': 'new',
            }
