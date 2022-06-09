from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from .models import Solution, Equation
from .forms import EquationForm
from .solver import *
import json

logger = logging.getLogger('difequation.main')


def solutions(request):
    solutions = Solution.objects.order_by()
    logger.info('Отправлен запрос в БД на получение всех имеющихся решений дифференциальных уравнений.')
    equations = Equation.objects.order_by()
    logger.info('Отправлен запрос в БД на получение всех имеющихся дифференциальных задач Коши.')
    return render(request, 'main/solutions.html', {
                      'title': 'Решенные уравнения',
                      'span': 'Список решенных дифференциальных уравнений',
                      'equations': equations,
                      'solutions': solutions
                  })


def index(request):
    if request.method == 'POST':
        form = EquationForm(request.POST)
        if form.is_valid():
            logger.info('Форма EquationForm прошла валидацию. Все поля заполнены корректно.')
            data = form.cleaned_data
            form.save()
            logger.info('Форма EquationForm сохранена в БД difEquations.')
            x, y = runge_kutta(
                data['order'],
                data['coefficients'],
                data['right_side'],
                data['segment_begin'],
                data['segment_end'],
                data['step'],
                data['init_conditions']
            )
            logger.info('Алгоритм Рунге-Кутты завершил свою работу. Задача Коши решена.')
            last_id = Equation.objects.latest('id').id
            graph_sol = solution_plot(x, y, data['step'], last_id)
            num_sol = json.dumps(dict(zip(x, y)))
            solution = Solution(num_sol, graph_sol, last_id)
            solution.save()
            logger.info(f'Решение задачи Коши сохранено в БД difEquations с id = {last_id}.')
        else:
            return render(request, 'main/index.html', {'form': form})
    form = EquationForm()
    return render(request, 'main/index.html', {'form': form})


def delete(request, id):
    try:
        equation = Equation.objects.get(id=id)
        logger.info(f'Отправлен запрос в БД на получение объекта equation с id = {id}.')
        equation.delete()
        logger.info(f'Объекта equation с id = {id} удален.')
        return HttpResponseRedirect("/solutions")
    except ObjectDoesNotExist:
        logger.info(f'Объект equation с id = {id} не найден.')
        return HttpResponseNotFound("<h2>Object was not found</h2>")
