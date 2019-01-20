from odoo import models, fields

class BookReport(models.Model):
    _name = 'library.book.report'
    _description = 'Book Report'
    _auto = False

    name = fields.Char('Title')
    publisher_id = fields.Many2one('res.partner')
    date_published = fields.Date()

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW library_book_report AS
            (SELECT *
            FROM library_book
            WHERE active=True)
        """)
