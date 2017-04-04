from openerp import api
from openerp import models, fields
from openerp.osv import fields as Fields
from datetime import datetime, timedelta


class send_eng_doc(models.Model):

    _name= "send.eng.doc"

    # to_company = fields.Char(string='To Company' , required=True)
    to_company = fields.Many2one('res.partner', 'To Company', required=True)

    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    province = fields.Char(string='State')
    country = fields.Char(string='Country')


    name = fields.Char(string='Transmittal Number', required=True)
    transmittal_date = fields.Date(string='Transmittal Date', required=True)
    due_date = fields.Date(string='Due Date',)
    need_to_response = fields.Date(string='Need to Response',)

    # message = fields.Char(string='Message')
    message = fields.Many2one('conf.send.message', 'Message')

    sender = fields.Char(string='Sender')
    state = fields.Selection(selection=[('new', 'New'), ('done', 'Done')])

    # master_deliver_id = fields.Many2one('master.deliver', 'Related Master Deliverables')
    master_deliver_id = fields.Many2many('master.deliver', 'master_to_send_eng', 'send_eng_id', 'master_deliver_id', string="Master Deliver")


    _defaults={
        'transmittal_date': lambda *a:datetime.now().strftime('%Y-%m-%d'),
        # 'date_end': lambda *a:(datetime.now() + timedelta(days=(6))).strftime('%Y-%m-%d'),
    }

    @api.onchange('to_company')
    def company_details(self):
        if self.to_company.id:
            if self.to_company.parent_id.id:
                if self.to_company.parent_id.street:
                    self.address = self.to_company.parent_id.street
                    if self.to_company.parent_id.street2:
                        self.address = self.address +" " + self.to_company.parent_id.street2
                self.city = self.to_company.parent_id.city or ""
                self.province = self.to_company.parent_id.state_id.name or ""
                self.country = self.to_company.parent_id.country_id.name or ""
            else :
                if self.to_company.street:
                    self.address = self.to_company.street
                    if self.to_company.street2:
                        self.address = self.address +" " + self.to_company.street2
                self.city = self.to_company.city or ""
                self.province = self.to_company.state_id.name or ""
                self.country = self.to_company.country_id.name or ""