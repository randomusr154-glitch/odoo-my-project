from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    name = fields.Char(required=True)

    _sql_constraints = [
        (
            'unique_tag_name',
            'UNIQUE(name)',
            'The tag name must be unique.'
        )
    ]