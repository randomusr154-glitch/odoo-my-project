from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('Accepted', 'accepted'), ('Refused', 'refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(default=lambda self: fields.Date.add(fields.Date.today(), days=7))

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        if self.date_deadline:
            start_date = fields.Date.to_date(self.create_date) if self.create_date else fields.Date.context_today(self)
            delta = self.date_deadline - start_date
            self.validity = delta.days
        else:
            self.validity = 7

    @api.onchange('validity')
    def _onchange_validity(self):
        start_date = fields.Date.to_date(self.create_date) if self.create_date else fields.Date.context_today(self)
        self.date_deadline = start_date + timedelta(days=self.validity)
        
    def accept_action(self):
        for record in self:
            if "Accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError("E' già stata accettata un'altra offerta per questo immobile!")

            record.status = "Accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "Offer_Accepted"

        return True


    def refuse_action(self):
        for record in self:
            record.status = "Refused"
        return True

    _sql_constraints = [
        (
            'check_offer_price',
            'CHECK(price > 0)',
            'The offer price must be strictly positive.'
        )
    ]