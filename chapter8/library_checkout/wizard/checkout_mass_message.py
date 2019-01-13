from odoo import api, exceptions, fields, models
import logging
_logger = logging.getLogger(__name__)

class CheckoutMassMessage(models.TransientModel):
    _name = 'library.checkout.massmessage'
    _description = 'Send Message to Borrowers'
    checkout_ids = fields.Many2many(
        'library.checkout',
        string='Checkouts')
    message_subject = fields.Char()
    message_body = fields.Html()

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        checkout_ids = self.env.context.get('active_ids')
        defaults['checkout_ids'] = checkout_ids
        return defaults

    @api.multi
    def button_send(self):
        # import pdb; pdb.set_trace()
        # import ipdb; ipdb.set_trace()
        import pudb; pu.db
        self.ensure_one()
        if not self.checkout_ids:
            raise exceptions.UserError(
                '请至少选择一条借阅记录来发送消息!')
        if not self.message_body:
            raise exceptions.UserError(
                '请填写要发送的消息体!')
        for checkout in self.checkout_ids:
            checkout.message_post(
                body=self.message_body,
                subject=self.message_subject,
                subtype='mail.mt_comment',
            )
        _logger.debug(
            'Message on %d to followers: %s',
            checkout.id,
            checkout.message_follower_ids)      
        _logger.info(
            'Posted %d messages to Checkouts: %s',
            len(self.checkout_ids),
            str(self.checkout_ids),
        )
        return True
