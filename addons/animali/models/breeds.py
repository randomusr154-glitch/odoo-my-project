from odoo import models, fields

class Razza(models.Model):
    _name = "gestione.razza"
    _description = "Razza Animale"

    name = fields.Char(string="Nome Razza", required=True)
    
    specie_id = fields.Many2one("gestione.specie", string="Specie", required=False, ondelete='cascade')