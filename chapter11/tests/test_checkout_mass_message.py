from odoo.tests.common import TransactionCase
from odoo import exceptions

class TestWizard(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestWizard, self).setUp(*args, **kwargs)
        # Setup test data
        admin_user = self.env.ref('base.user_admin')
        self.Checkout = self.env['library.checkout'].sudo(admin_user)
        self.Wizard = self.env['library.checkout.massmessage'].sudo(admin_user)

        a_member = self.env['library.member'].create({'name': 'John'})
        self.checkout0 = self.Checkout.create({
            'member_id': a_member.id})

    def test_button_send(self):
        """Send button should create messages on Checkouts"""
        # Add test code
        msgs_before = len(self.checkout0.message_ids)

        Wizard0 = self.Wizard.with_context(active_ids=self.checkout0.ids)
        wizard0 = Wizard0.create({'message_body': 'Hello'})
        wizard0.button_send()

        msgs_after = len(self.checkout0.message_ids)
        self.assertEqual(
            msgs_after,
            msgs_before+1,
            'Expected on additional message in the Checkout.')

    def test_button_send_empty_body(self):
        "Send button errors on empty body message"
        wizard0 = self.Wizard.create({})
        with self.assertRaises(exceptions.UserError) as e:
            wizard0.button_send()
