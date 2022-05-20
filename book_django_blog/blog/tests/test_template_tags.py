from django.test import TestCase

from blog.forms import EmailPostForm
from blog.templatetags.style_field_tags import form_control


class TestStyleFieldTags(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form = EmailPostForm()

    def test_form_control_sm_class_in_field_class_attribute(self):
        field = self.form.fields['email']
        self.assertIsNone(field.widget.attrs.get('class'))
        for field in self.form:
            self.assertEqual(form_control(field).field.widget.attrs.get('class'), 'form-control form-control-sm')
