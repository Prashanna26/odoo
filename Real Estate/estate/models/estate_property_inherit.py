from odoo import models, fields, api

class EstatePropertyInherit(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 
                                   'seller',
                                   domain="[('state','=','new'), ('state','=','offer_received')]")
