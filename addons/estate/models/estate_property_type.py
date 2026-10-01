from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    name = fields.Char(required=True)

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties") # blocco modificato


    _sql_constraints = [
        (
            'unique_type_name',
            'UNIQUE(name)',
            'The property type must be unique.'
        ),
    ]