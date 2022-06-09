from .models import Equation
from django.forms import ModelForm
from .form_validation import *

logger = logging.getLogger('difequation.main')


class EquationForm(ModelForm):
    class Meta:
        model = Equation
        fields = [
            "order",
            "coefficients",
            "right_side",
            "segment_begin",
            "segment_end",
            "step",
            "init_conditions"
        ]

    def clean(self):
        super(EquationForm, self).clean()

        order = self.cleaned_data.get('order')
        coefficients = self.cleaned_data.get('coefficients')
        right_side = self.cleaned_data.get('right_side')
        segment_begin = self.cleaned_data.get('segment_begin')
        segment_end = self.cleaned_data.get('segment_end')
        step = self.cleaned_data.get('step')
        init_conditions = self.cleaned_data.get('init_conditions')

        if order > 25:
            self._errors['order'] = self.error_class(['Порядок дифференциального уравнения не должен превышать 25.'])
            logger.info(f'Порядок дифференциального уравнения n = {order} превышает 25.')

        if segment_end <= segment_begin:
            self._errors['segment_end'] = self.error_class(['Конец расчетной области доолжен быть больше начала.'])
            logger.info(f'Конец расчетной области {segment_end} не больше начала расчетной области {segment_begin}')
        elif segment_end - segment_begin > 1000:
            self._errors['segment_end'] = self.error_class(['Расчетная область не должна превышать 1000.'])
            logger.info(f'Слишком большая расчетная область: [{segment_begin}, {segment_end}].')

        if (segment_end - segment_begin) / step % 1 != 0.0:
            self._errors['step'] = self.error_class(['Некорректно выбран шаг. Число узлов сетки не будет целым числом.'])
            logger.info(f'Некорректно выбран шаг сетки {step}.')
            logger.info(f'Число узлов сетки не будет целым на промежутке [{segment_begin}, {segment_end}].')

        if not are_coefficients_valid(coefficients, order):
            my_string = 'Проверьте правильность формата ввода, коэффициенты должны разделяться запятой с пробелом и ' \
                        'должны быть вещественными числами или функциями переменной x. Количество коэффициентов ' \
                        f'должно быть {order + 1}. Коэффициент при старшей производной должен быть отличным от нуля.'
            self._errors['coefficients'] = self.error_class([my_string])
            logger.info(f'Коэффициенты уравнения {coefficients} не прошли валидацию.')

        if not are_init_conditions_valid(init_conditions, order):
            my_string = 'Проверьте правильность формата ввода, начальные условия должны разделяться запятой с пробелом'\
                        f'и должны быть вещественными числами. Количество начальных условий должно быть {order}.'
            self._errors['init_conditions'] = self.error_class([my_string])
            logger.info(f'Начальные условия {init_conditions} не прошли валидацию.')

        if not is_math_expr(right_side):
            my_string = 'Правая часть уравнения должна содержать корректные синтаксические выражения и быть функцией ' \
                        'переменной x.'
            self._errors['right_side'] = self.error_class([my_string])
            logger.info(f'Правая часть уравнения не прошла валидацию. {right_side} не является математическим выражением.')

        return self.cleaned_data
