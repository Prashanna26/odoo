from odoo import _, models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

# Estate Property Model
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _order = "id desc"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,
                                    default=fields.Date.add(fields.Date.today(),months=3),
                                    string="Availability Form")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, 
                                 copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north','North'),
                                           ('south', 'South'),
                                           ('east', 'East'), 
                                           ('west', 'West')])
    state = fields.Selection([('new','New'),
                               ('offer_received','Offer Recieved'),
                               ('offer_accepted', 'Offer Accepted'), 
                               ('sold', 'Sold'), 
                               ('cancel', 'Canceled')],
                               default='new', 
                               string="Status")
    active = fields.Boolean(default=True)
    buyer = fields.Many2one('res.partner', string="buyer", readonly=True)
    seller = fields.Many2one('res.users', string="seller")
    property_type_id = fields.Many2one('estate.property.type', string="Property_Type")
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.offer', "property_id", required=True)
    total_area = fields.Integer(compute="_compute_total" ,string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")

    @api.depends('living_area','garden_area')
    def _compute_total(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_price = 0

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for rec in self:
            if rec.selling_price:
                min_val = rec.expected_price * 0.9
                if min_val > rec.selling_price:
                    raise ValidationError(_('The offer value must be greater than 90% of Expected Price!!'))

    _sql_constraints = {
    ('check_expected_price', 'CHECK(expected_price >= 0)',
     'The expected price cannot be less than 0!!'), 
     ('check_selling_price', 'CHECK(selling_price >= 0)',
      'The selling price cannot be less than 0!!')
    }


    @api.onchange('garden')
    def onchange_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_area = 10
                rec.garden_orientation = "north"

            else:
                rec.garden_area = 0
                rec.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_canceled(self):
        if any(rec.state != 'new' and rec.state !='cancel' for rec in self):
            raise UserError("You can only delete new or canceled property!!")
            

    def sold_action(self):
        for rec in self:
            if rec.state == 'cancel':
                raise UserError(_("You Cannot Sell Canceled Property"))
            else:
                rec.state = 'sold'
                return True

    def cancel_action(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(_("You Cannot Cancel Sold Property"))
            else:
                rec.state = 'cancel'
                return True


# Estate Property Type Model
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _sql_constraints = {
        ('property_tag_unique', 'unique(name)', 'The Proprty Tag must be different!!')
    }

# Estate Offer Model
class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "Estate Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'), 
                               ('refused','Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string= "Validity(days)")
    date_deadline = fields.Date(compute="_compute_validity_date", inverse="_inverse_validity_date")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    
    @api.depends("validity", "date_deadline")
    def _compute_validity_date(self):
        for rec in self:
            if rec.create_date:
                rec.date_deadline = rec.create_date.date() + timedelta(days=rec.validity)
            else:
                rec.date_deadline = datetime.now().date() + timedelta(days=rec.validity)

    def _inverse_validity_date(self):
        for rec in self:
            if rec.create_date:
                rec.validity = (rec.date_deadline - rec.create_date.date()).days
            else:
                rec.validity = (rec.date_deadline - datetime.now().date()).days

    _sql_constraints = {
    ('check_expected_price', 'CHECK(price >= 0)',
     'The Offered price cannot be less than 0!!')
     }


    @api.model_create_multi
    def create(self, vals):
        offer = self.env["estate.offer"].search([("property_id","=",vals[0]["property_id"])]).mapped("price")
        if offer:
            max_offer = max(offer)
            if max_offer and vals[0]['price'] < max_offer:
                raise exceptions.ValidationError(f"Cannot create offer with lower amount than {int(max_offer)}.")
        res = super().create(vals)
        res.property_id.state = 'offer_received'
        return res


    def action_accept(self):
            total_offers = self.property_id.offer_ids
            for rec in self:
                if any(offer.status == "accepted" for offer in total_offers):
                    raise UserError("Two offers cannot  be accepted at the same time!")
                rec.status = 'accepted'
                rec.property_id.buyer = rec.partner_id.id
                rec.property_id.selling_price = rec.price
                rec.property_id.state = 'offer_accepted'


    def action_refuse(self):
        for rec in self:
            rec.status = 'refused'