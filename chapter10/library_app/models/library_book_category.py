from odoo import api, fields, models

class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Book Category'
    _parent_store = True

    name = fields.Char(translate=True, required=True)
    # Hierarchy fields
    parent_id = fields.Many2one(
        'library.book.category',
        'Parent Category',
        ondelete='restrict')
    parent_path = fields.Char(index=True)

    # Optional but good to have:
    child_ids = fields.One2many(
        'library.book.category',
        'parent_id',
        'Subcategories')
    
    highlighted_id = fields.Reference(
        [('library.book', 'Book'), ('res.partner', 'Author')],
        'Category Highlight'
    )
