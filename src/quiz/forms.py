from django import forms
from django.core.exceptions import ValidationError

from .models import Choice


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                f'Questions count must be range '
                f'from {self.instance.QUESTION_MIN_LIMIT} '
                f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
            )
        cnt = self.instance.ORDER_NUM_MIN_LIMIT
        for form in self.forms:
            if form.cleaned_data['order_num'] != cnt or cnt > self.instance.QUESTION_MAX_LIMIT:
                raise ValidationError(
                    f'Questions order num must be range '
                    f'from {self.instance.ORDER_NUM_MIN_LIMIT} '
                    f'to {self.instance.QUESTION_MAX_LIMIT} inclusive ,'
                    f'and should increase by 1'
                )
            cnt += 1


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):

        # num_correct_answers = sum(1 for form in self.forms if form.cleaned_data['is_correct'])

        num_correct_answers = sum(form.cleaned_data['is_correct'] for form in self.forms)

        if num_correct_answers == 0:
            raise ValidationError('You must select at least 1 option.')

        if num_correct_answers == len(self.forms):
            raise ValidationError('NOT allowed to select all options.')


class ChoiceForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text']


ChoicesFormSet = forms.modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
