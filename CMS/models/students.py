from odoo import models, fields, api

class StuentData(models.Model):
    _name = "student.detail"
    _description = "Details about Student"

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection([('M', 'Male'), ('F', 'Female')], string='Gender')
    grade = fields.Integer(string="Grade")
    rollnum = fields.Integer(string="Roll Number", required=True)
    subject_id = fields.Many2many('subject.detail', default=lambda self: self._default_m2m_values())

    def _default_m2m_values(self):
        default_record_ids = [1, 2, 3, 4, 5]
        return [(6, 0, default_record_ids)]


    