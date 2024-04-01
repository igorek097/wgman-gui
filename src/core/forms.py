from django.forms import TextInput, CheckboxInput


class BootstrapFormMixin:
    
    required_css_class = 'fw-bold'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if type(field.widget) == CheckboxInput:
                field.widget.attrs.update({
                    'class': 'form-check-input mb-2 ms-3',
                })
                continue
            field.widget.attrs.update({
                'class': 'form-control mb-2',
            })