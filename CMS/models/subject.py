from odoo import  api, fields, models

class SubjectData(models.Model):
    _name = "subject.detail"
    _description = "Subject Detail Data"

    name = fields.Char(string=u'Name', required=True)
    teachername = fields.Char(string="Teacher's Name")
    
    
