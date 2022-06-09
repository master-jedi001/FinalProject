# functions for form validation
import logging
import numexpr as ne
import numpy
import random

logger_1 = logging.getLogger('exception')
logger_2 = logging.getLogger('difequation.main')


def is_math_expr(expr):
    try:
        x = random.randint(0, 100)
        return isinstance(ne.evaluate(expr), numpy.ndarray)
    except KeyError:
        logger_1.exception('Аргумент функции is_math_expr не является числовым выражением или функцией переменной x.')
        return False
    except SyntaxError:
        logger_1.exception('Аргумент функции is_math_expr содержит синтаксическую ошибку.')
        return False
    except TypeError:
        logger_1.exception('В качестве аргумента функции is_math_expr возможно передается неподдерживаемый тип выражения.')
        return False
    except ValueError:
        logger_1.exception('Аргумент функции is_math_expr не является строкой.')
        return False
    except BaseException:
        logger_1.exception('В ходе работы функции is_math_expression возникла ошибка.')
        return False


def is_number(expr):
    try:
        float(expr)
        return True
    except TypeError:
        logger_1.exception('Некорректная работа с типами при вызове функции is_number.')
        return False
    except ValueError:
        logger_1.exception('Аргумент функции is_number не является числом.')
        return False
    except BaseException:
        logger_1.exception('В ходе работы функции is_number возникла ошибка.')
        return False


def are_init_conditions_valid(my_str, n):
    my_list = my_str.split(', ')
    if len(my_list) != n:
        logger_2.debug(f'Количество начальных условий {my_list} не соответствует порядку уравнения {n}.')
        return False
    validity = True
    for lst in my_list:
        if not is_number(lst):
            logger_2.debug(f'Начальное условие {lst} не является числом.')
            validity = False
    return validity


def are_coefficients_valid(my_str, n):
    my_list = my_str.split(', ')
    if len(my_list) != n + 1 or my_list[n] == '0':
        logger_2.debug(f'Количество коэффициентов {my_list} не соответствует порядку уравнения {n}.')
        logger_2.debug(f'Или коэффициент при старшей производной равен нулю.')
        return False
    validity = True
    for lst in my_list:
        if not is_math_expr(lst):
            logger_2.debug(f'Коэффициент {lst} не является математическим выражением.')
            validity = False
    return validity
