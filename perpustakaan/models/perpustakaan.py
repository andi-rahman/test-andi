from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

#Objek/Class
class PeminjamanBuku(models.Model):
#Atribut
    _name = 'peminjaman.buku'
    _description = 'Peminjaman Buku'

    def _get_date(self):
        return fields.Date.today()

    def _get_name(self):
        return self.env['ir.sequence'].next_by_code('peminjaman.sequence')


    def action_search_anggota(self):
        if self.no_anggota:
            partner = self.env['res.partner'].search([('no_anggota', '=', self.no_anggota)], limit=1)
            if partner:
                self.anggota_id = partner.id

    def update_state(self):
        if self.state == 'dipinjam':
            self.write({'state': 'dikembalikan'})

#Fields
    name = fields.Char(string='Name', default=_get_name)
    tanggal_pinjam = fields.Date(string='Tanggal Pinjam', default=_get_date)
    tanggal_kembali = fields.Date(string='Tanggal Kembali')
    peminjam_id = fields.Many2one('res.partner', string="Peminjam")
    no_anggota = fields.Char(string="No. Anggota")
    no_telp = fields.Char(string="Phone")
    petugas_id = fields.Many2one('res.users', string="Petugas")
    anggota_id = fields.Many2one('res.partner', string="Anggota")
    total_harga_pinjam = fields.Float(string='Total Harga Pinjam', compute='_compute_total')
    state = fields.Selection(string="Status", selection=[
            ('dipinjam', 'Dipinjam'),
            ('dikembalikan', 'Dikembalikan'),
        ], default='dipinjam')
    daftar_buku_ids = fields.One2many('daftar.buku', 'peminjam_id', string='Daftar Buku')
    buku_ids = fields.Many2many('daftar.buku', string='Daftar Buku')

    @api.onchange('tanggal_pinjam')
    def _default_pengembalian(self):
        if self.tanggal_pinjam:
            pengembalian = self.tanggal_pinjam + relativedelta(weeks=1)
            self.tanggal_kembali = pengembalian

    @api.onchange('no_anggota', 'anggota_id')
    def onchange_anggota(self):
        # if self.no_anggota:
        #     partner = self.env['res.partner'].search([('no_anggota', '=', self.no_anggota)], limit=1)
        #     if partner:
        #         self.anggota_id = partner
        if self.anggota_id:
            self.no_anggota = self.anggota_id.no_anggota or False

    @api.depends('daftar_buku_ids.harga_pinjam')
    def _compute_total(self):
        for buku in self:
            buku.total_harga_pinjam = sum([line.harga_pinjam for line in buku.daftar_buku_ids])

class DaftarBuku(models.Model):
    _name = 'daftar.buku'
    _inherit = ['image.mixin']
    _description = 'Training Attendees'

    buku_id = fields.Many2one('product.product', string='Barang')
    name = fields.Char('Name')
    image = fields.Binary('image', store=True)
    harga_pinjam = fields.Float(string='Harga')
    peminjam_id = fields.Many2one('peminjaman.buku', string='NO. Peminjam')
    sinopsis = fields.Text(string='Sinopsis')


class ProductProduct(models.Model):
    _inherit = "product.product"

    sinopsis = fields.Text(string='Sinopsis')
