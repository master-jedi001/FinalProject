from django.db import models


class Equation(models.Model):
    order = models.PositiveIntegerField('order')
    coefficients = models.CharField('coefficients', max_length=256)
    right_side = models.CharField('right_side', max_length=256)
    segment_begin = models.IntegerField('segment_begin')
    segment_end = models.IntegerField('segment-end')
    step = models.FloatField('step')
    init_conditions = models.CharField('init_conditions', max_length=256)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Коэффициенты: ' + str(self.coefficients) + '\n' + 'Правая часть: ' + str(self.right_side)


class Solution(models.Model):
    numerical_solution = models.JSONField('num_sol')
    graph_solution = models.CharField('graph_sol', max_length=256)
    equation = models.OneToOneField(Equation, on_delete=models.CASCADE, primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.graph_solution)
