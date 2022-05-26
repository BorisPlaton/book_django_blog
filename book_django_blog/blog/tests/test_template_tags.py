from django.test import TestCase

from blog.forms import EmailPostForm
from blog.templatetags.style_field_tags import form_control


class TestStyleFieldTags(TestCase):

    def setUp(self):
        self.form = EmailPostForm()

    def test_form_control_sm_class_in_field_class_attribute(self):
        field = self.form.fields['email']
        self.assertIsNone(field.widget.attrs.get('class'))
        for field in self.form:
            self.assertEqual(form_control(field).field.widget.attrs.get('class'), 'form-control form-control-sm')

    def test_form_control_tag_with_keyword_arguments(self):
        for field in self.form:
            new_field = form_control(field, placeholder='New text', style='margin: 1px;')
            self.assertEqual(
                new_field.field.widget.attrs.get('class'),
                'form-control form-control-sm'
            )
            self.assertEqual(
                new_field.field.widget.attrs.get('placeholder'),
                'New text'
            )
            self.assertEqual(
                new_field.field.widget.attrs.get('style'),
                'margin: 1px;'
            )
