from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'


    ttype_mhs = fields.Selection([('mhs', 'Mahasiswa'), ('petugas', 'Petugas')], string='Type', default='mhs')
    no_anggota = fields.Char(string="No. Anggota")

    # @api.constrains('no_anggota')
    # def _check_no_anggota(self):
    #     if not self.no_anggota:
    #         raise ValidationError(_("Tolong Masukan No Anggota"))
