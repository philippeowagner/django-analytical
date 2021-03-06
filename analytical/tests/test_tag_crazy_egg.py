"""
Tests for the Crazy Egg template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.crazy_egg import CrazyEggNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class CrazyEggTagTestCase(TagTestCase):
    """
    Tests for the ``crazy_egg`` template tag.
    """

    def setUp(self):
        super(CrazyEggTagTestCase, self).setUp()
        self.settings_manager.set(CRAZY_EGG_ACCOUNT_NUMBER='12345678')

    def test_tag(self):
        r = self.render_tag('crazy_egg', 'crazy_egg')
        self.assertTrue('/1234/5678.js' in r, r)

    def test_node(self):
        r = CrazyEggNode().render(Context())
        self.assertTrue('/1234/5678.js' in r, r)

    def test_no_account_number(self):
        self.settings_manager.delete('CRAZY_EGG_ACCOUNT_NUMBER')
        self.assertRaises(AnalyticalException, CrazyEggNode)

    def test_wrong_account_number(self):
        self.settings_manager.set(CRAZY_EGG_ACCOUNT_NUMBER='123abc')
        self.assertRaises(AnalyticalException, CrazyEggNode)

    def test_uservars(self):
        context = Context({'crazy_egg_var1': 'foo', 'crazy_egg_var2': 'bar'})
        r = CrazyEggNode().render(context)
        self.assertTrue("CE2.set(1, 'foo');" in r, r)
        self.assertTrue("CE2.set(2, 'bar');" in r, r)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = CrazyEggNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Crazy Egg disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)
