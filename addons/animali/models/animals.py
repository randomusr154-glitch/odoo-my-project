from odoo import models, fields, api
from datetime import date

class Animals(models.Model):
    _name = "gestione.animals"
    _description = "Animale Domestico"

    name = fields.Char(string="Nome Animale", required=True)

    date_of_birth = fields.Date(string="Data di nascita")
    eta = fields.Integer(string="Età", compute="_compute_eta", store=True)

    specie_id = fields.Many2one("gestione.specie", string="Specie")
    razza_id = fields.Many2one("gestione.razza", string="Razza")

    colore = fields.Char(string="Colore", required=True)
    
    sesso = fields.Selection([
        ('maschio', 'Maschio'),
        ('femmina', 'Femmina'),
        ('altro', 'Altro')
    ], string="Sesso", required=True)

    partner_id = fields.Many2one('res.partner', string="Proprietario")

    @api.depends('date_of_birth')
    def _compute_eta(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                birth_date = fields.Date.from_string(record.date_of_birth)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.eta = max(0, age)
            else: 
                record.eta = 0

    @api.onchange('specie_id')
    def _onchange_specie_id(self):
        if self.razza_id and self.razza_id.specie_id and self.razza_id.specie_id != self.specie_id:
            self.razza_id = False

    @api.onchange('razza_id')
    def _onchange_razza_id(self):
        if self.razza_id and self.razza_id.specie_id:
            self.specie_id = self.razza_id.specie_id