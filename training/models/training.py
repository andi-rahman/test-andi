from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TrainingCourse(models.Model):
    _name = 'training.module'
    _description = 'Training Course'

    def _get_name(self):
        return "Nama"
        # return fields.Date.today()

    def _get_date(self):
        return fields.Date.today()

    def _get_number(self):
        return self.env['ir.sequence'].next_by_code('training.sequence')
        # return self.env['sale.order'].next_by_code('training.sequence')

    date = fields.Date(string='Training Date', default=_get_date)
    training_number = fields.Char(string='Number', readonly=True, default=_get_number)
    name = fields.Char(string='Name', default=_get_name)

    registration_amount = fields.Float(string='Registration Amount')
    description = fields.Text(string='description')
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('done', 'Done')], string="Status", default='draft')
    total_attendees = fields.Integer(string='Total Attendees', compute='_compute_total', store=True)
    total_attendees_presence = fields.Integer(string='Total Attendees Presence', compute='_compute_total_presence')
    phone = fields.Char(string="Phone")
    trainer_id = fields.Many2one('res.users', string="Trainer")
    assistant_ids = fields.Many2many('res.users', string="Assistant")

    attendee_ids = fields.One2many('training.attendees', 'training_id', string='Attendees')

    def update_state(self):
        if self.state == 'draft':
            self.write({'state': 'inprogress'})

    @api.depends('attendee_ids')
    def _compute_total(self):
        for item in self:
            item.total_attendees = len(item.attendee_ids)

    @api.depends('attendee_ids.presence')
    def _compute_total_presence(self):
        for item in self:
            attendees = item.attendee_ids.filtered(lambda a: a.presence)
            item.total_attendees_presence = len(attendees)
            # item.total_attendees_presence = len(attendees)

    @api.onchange('trainer_id')
    def _onchange_trainer_id(self):
        if self.trainer_id:
            self.phone = self.trainer_id.phone

    _sql_constraints = [
        ('training_unique', 'UNIQUE(name)', 'A name must  be unique!'),
    ]

    @api.constrains('registration_amount')
    def _check_registration_amount(self):
        if self.registration_amount <= 0:
            raise ValidationError('Registration amount must be greater than zero')

    def action_create_multi_attandee(self):
        view = self.env.ref('training.wizard_training_view')
        return {
            'name': ('Create Attandee'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'multi.add.attendee.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': self.env.context,
        }

    def action_create_partner(self):
        view = self.env.ref('training.wizard_training_view_partner')
        return {
            'name': ('Create Attandee'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'multi.add.attendee.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': self.env.context,
        }

    # @api.constrains('total_attendees')
    # def _check_attendees(self):
    #     if self.total_attendees < 3:
    #         raise ValidationError('Total Attendees harus lebih dari 3')


class TrainingAttendees(models.Model):
    _name = 'training.attendees'
    _description = 'Training Attendees'

    attendee_id = fields.Many2one('res.partner', string='Attendee')
    presence = fields.Boolean(string='Presence')
    training_id = fields.Many2one('training.module', string='Training')
    phone = fields.Char(related="attendee_id.phone", string="Phone")
    is_select = fields.Boolean("Select")
    sequence = fields.Integer(string='Sequence', default=10)


class ResUsers(models.Model):
    _inherit = 'res.users'

    training_ids = fields.Many2many(
        'training.module', string='Training')

    def _compute_training(self):
        training_obj = self.env['training.module']
        training = training_obj.search([('trainer_id', '=', self.id)])
        self.training_ids = training.ids
