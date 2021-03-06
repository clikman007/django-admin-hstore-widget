from django.conf import settings
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.widgets import AdminTextareaWidget
from django.contrib.postgres.forms import forms
from django.template.loader import get_template
from django.utils.safestring import mark_safe


class HStoreFormWidget(AdminTextareaWidget):

    @property
    def media(self):
        internal_js = [
            "django_admin_hstore/underscore-min.js",
            "django_admin_hstore/django-admin-hstore.js"
        ]

        js = [static("admin/js/%s" % path) for path in internal_js]

        return forms.Media(js=js)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
            # it's called "original" because it will be replaced by a copy
        attrs['class'] = 'hstore-original-textarea'

        # get default HTML from AdminTextareaWidget
        html = super(HStoreFormWidget, self).render(name, value, attrs)

        # prepare template context
        template_context = {
            'field_name': name,
            'STATIC_URL': settings.STATIC_URL,
        }

        # get template object
        template = get_template('admin/django-admin-hstore-field-widget.html')
        # render additional html
        additional_html = template.render(template_context)

        # append additional HTML and mark as safe
        html = html + additional_html
        html = mark_safe(html)

        return html
