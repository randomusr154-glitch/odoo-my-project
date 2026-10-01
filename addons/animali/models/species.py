from odoo import models, fields

class Specie(models.Model):
    _name = "gestione.specie"
    _description = "Specie Animale"

    name = fields.Char(string="Nome Specie", required=True)
    
    razza_ids = fields.One2many("gestione.razza", "specie_id", string="Razze")