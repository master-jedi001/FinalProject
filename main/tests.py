import unittest
from solver import *
from form_validation import *
import numpy as np


class TestSolverFunctions(unittest.TestCase):

    def test_func(self):
        self.assertEqual(func('x**3', 3), 27, '3 в кубе должно равняться 27')

    def test_max_error(self):
        y = [0, 1, 2.5, 3.1, 4, 5.2]
        z = lambda t: t
        x = [0, 1, 2, 3, 4, 5]
        self.assertEqual(max_error(y, z, x), 0.5, 'Максимальная ошибка должна была равняться 0.5')

    def test_runge_kutta_functions(self):
        x, y = runge_kutta(5, '243, 405, 270, 90, 15, 1', '0', 0, 5, 0.01, '0, 3, -9, -8, 0')
        z = lambda t: -1 / 12 * (129 * t ** 3 + 16 * t ** 2 - 54 * t - 36) * t * np.exp(-3 * t)
        self.assertTrue(max_error(y, z, x) < 0.0001, 'Максимальная ошибка численного решения превышает 0.0001')

        x, y = runge_kutta(3, '0, 9, -6, 1', 'x*exp(3*x) + exp(3*x)*cos(2*x)', 0, 2, 0.01, '0, 0, 1')
        z_1 = lambda t: 234 * t ** 3 - 234 * t ** 2 + 1560 * t - 169
        z_2 = lambda t: - 162 * np.sin(2 * t) - 243 * np.cos(2 * t) + 412 * np.exp(-3 * t)
        z = lambda t: 1 / 4212 * np.exp(3 * t) * (z_1(t) + z_2(t))
        self.assertTrue(max_error(y, z, x) < 0.0001, 'Максимальная ошибка численного решения превышает 0.0001')

        x, y = runge_kutta(2, '9*x, -3*(2*x+1), x+1', '2*exp(4*x)', 0, 1, 0.01, '0, 1')
        z = lambda t: 2 * t * np.exp(4 * t)/(t+1)**2 + 1/2*np.exp(3*t)*(1/(t+1)**2 - 1)
        self.assertTrue(max_error(y, z, x) < 0.0001, 'Максимальная ошибка численного решения превышает 0.0001')

        x, y = runge_kutta(2, 'x, 2, x', '0', 1, 20, 0.01, '1, 0')
        z = lambda t: (np.cos(1) - np.sin(1)) * np.cos(t) / t + (np.cos(1) + np.sin(1)) * np.sin(t) / t
        self.assertTrue(max_error(y, z, x) < 0.0001, 'Максимальная ошибка численного решения превышает 0.0001')


class TestFormValidationFunctions(unittest.TestCase):

    def test_is_math_expr(self):
        self.assertTrue(is_math_expr('2 + 3'), '2 + 3 является математическим выражением, должно было быть True')
        self.assertTrue(is_math_expr('cos(x)'), 'cos(x) является математическим выражением, должно было быть True')
        self.assertFalse(is_math_expr('y ** 2'), 'y ** 2 не является функцией x, должно было быть False')
        self.assertFalse(is_math_expr('hello'), 'hello не является математическим выражением, должно было быть False')

    def test_is_number(self):
        self.assertTrue(is_number('23.5'), '23.5 является числом, результат должен был быть True')
        self.assertFalse(is_number('4, 5'), '4, 5 не является числом, результат должен был быть False')
        self.assertFalse(is_number('hello'), 'hello не является числом, результат должен был быть False')

    def test_are_init_conditions_valid(self):
        self.assertTrue(are_init_conditions_valid('0, -3, 5', 3), '"0, -3, 5", 5 - должно было получиться True')
        self.assertFalse(are_init_conditions_valid('0', 2), '"0", 2 - должно было получиться False')
        self.assertFalse(are_init_conditions_valid('1, 3, hello, 8, -3', 5), '"1, 3, hello, 8, -3", 5 - False')

    def test_are_coefficients_valid(self):
        self.assertTrue(are_coefficients_valid('12, cos(x), x, 4', 3), '"12, cos(x), x, 4", 3 - должно было быть True')
        self.assertFalse(are_coefficients_valid('1, 0, 3, x ** 2', 2), '"1, 0, 3, x ** 2", 2 - должно быть False')
        self.assertFalse(are_coefficients_valid('2, -6, 0', 2), '"2, -6, 0", 2 - должно быть False')
        self.assertFalse(are_coefficients_valid('15, cos(y), 1', 2), '"15, cos(y), 1", 2 - должно быть False')
        self.assertFalse(are_coefficients_valid('15, 0, hello', 2), '"15, 0, hello", 2 - должно быть False')


if __name__ == '__main__':
    unittest.main()
