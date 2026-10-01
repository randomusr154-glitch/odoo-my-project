from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import _
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[('North', 'north'), ('South', 'south'), ('East', 'east'), ('West', 'west')])
    active = fields.Boolean(default=True)
    state = fields.Selection(copy=False, default="New", selection=[('New', 'new'), ('Offer_Received', 'offer_received'), ('Offer_Accepted', 'offer_accepted'), ('Sold', 'sold'), ('Cancelled', 'cancelled')])
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Integer(compute="_compute_best_price")
   

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids.exists():
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            if not self.garden_area:
                self.garden_area = 10
            if not self.garden_orientation:
                self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold_action(self):
        for record in self:
            if record.state == "Cancelled":
                raise UserError(_("A cancelled property cannot be sold."))
            record.state = "Sold"
        return True

    def cancel_action(self):
        for record in self:
            if record.state == "Sold":
                raise UserError(_("A sold property cannot be cancelled."))
            record.state = "Cancelled"
        return True

    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            'The expected price must be strictly positive.'
        ),
        (
            'check_selling_price', 
            'CHECK(selling_price >= 0)',
            'The selling price must be positive.'
        )
    ]