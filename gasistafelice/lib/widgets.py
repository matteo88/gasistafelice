from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.forms import SplitDateTimeField, TextInput, MultiWidget
from django.contrib.admin import widgets as admin_widgets

from django.conf import settings

from itertools import chain

from django.forms.widgets import Select, CheckboxSelectMultiple, CheckboxInput, mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape

#--------------------------------------------------------------------------------

class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, *args, **kw):
        self.related_model = related_model
        return super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

    def render(self, name, value, *args, **kwargs):
        rel_to = self.related_model
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        related_url = reverse('admin:%s_%s_add' % info)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                (related_url, name))
        output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))

#--------------------------------------------------------------------------------

class RelatedMultipleFieldWidgetCanAdd(widgets.SelectMultiple):

    def __init__(self, related_model, *args, **kw):
        self.related_model = related_model
        return super(RelatedMultipleFieldWidgetCanAdd, self).__init__(*args, **kw)

    def render(self, name, value, *args, **kwargs):
        rel_to = self.related_model
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        related_url = reverse('admin:%s_%s_add' % info)
        output = [ super(RelatedMultipleFieldWidgetCanAdd, self).render(
            name, value, *args, **kwargs
        ) ]
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                (related_url, name))
        output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))

#--------------------------------------------------------------------------------

class SplitDateTimeFormatAwareWidget(admin_widgets.AdminSplitDateTime):

    def __init__(self, *args, **kw):
        super(SplitDateTimeFormatAwareWidget, self).__init__(*args, **kw)
        self.widgets[0].format=settings.DATE_INPUT_FORMATS[0]
        self.widgets[1].widget = admin_widgets.AdminTimeWidget()
        self.widgets[1].format=settings.TIME_INPUT_FORMATS[0]

#--------------------------------------------------------------------------------

class DateFormatAwareWidget(admin_widgets.AdminDateWidget):

    def __init__(self, *args, **kw):
        super(DateFormatAwareWidget, self).__init__(*args, **kw)
        self.format=settings.DATE_INPUT_FORMATS[0]

#--------------------------------------------------------------------------------

class SplitDateTimeFieldWithClean(SplitDateTimeField):

    def render(self, name, *args, **kwargs):
        html = super(SplitDateTimeFieldWithClean, self).render(name, *args, **kwargs)
        plus = "<label >Test:</label>"
        return html+plus

#--------------------------------------------------------------------------------

class CheckboxSelectMultipleWithDisabled(CheckboxSelectMultiple):
    """
    Subclass of Django's checkbox select multiple widget that allows disabling checkbox-options.
    To disable an option, pass a dict instead of a string for its label,
    of the form: {'label': 'option label', 'disabled': True}
    """
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            if final_attrs.has_key('disabled'):
                del final_attrs['disabled']
            if isinstance(option_label, dict):
                if dict.get(option_label, 'disabled'):
                    final_attrs = dict(final_attrs, disabled = 'disabled' )
                option_label = option_label['label']
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''            
            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

