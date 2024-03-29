# Финальный проект

Тема: разработка приложения для численного решения обыкновенных линейных дифференциальных уравнений  
  
Проект представляет собой full-stack приложение, написанное на языке Python версии 3.10 с использованием фреймворка Django и СУБД PostgreSQL и 
позволяющее численно решать задачу Коши для обыкновенных линейных дифференциальных уравнений. Такие параметры как порядок дифференциального уравнения 
(целое положительное число), его коэффициенты (вещественные числа или функции переменной x), неоднородность уравнения (функция переменной x), 
отрезок решения (границы которого являются целыми числами), шаг решения (вещественное число), а также начальные условия (вещественные числа) 
задаются самим пользователем. Пользовательская часть приложения представляет собой веб-страницу, содержащую форму для ввода параметров уравнения, 
которое необходимо решить, и веб-страницу, отображающую все задачи, когда-либо вводимые пользователем, вместе с графиками решений этих задач. 
Все параметры уравнения сохраняются в БД в виде отдельной строки в таблице уравнений, которая посредством отношения один к одному связана с другой 
таблицей, содержащей решения всех этих уравнений. Помимо возможности добавления через форму новой дифференциальной  задачи и ее решения, также 
имеется возможность удаления той или иной задачи вместе с ее решением по усмотрению пользователя на странице всех решенных задач. Задача Коши 
для дифференциального уравнения решается посредством реализации численной схемы Рунге-Кутты четвертого порядка без использования каких-либо 
готовых решателей. Графики решений строятся при помощи библиотеки matplotlib. 
  
  
Помимо основных модулей, создаваемых Django автоматически, имеются следующие:  
Приложение main:  
  - migrations: хранит миграции, позволяющие синхронизировать структуру  базы данных с определением моделей; 
  - templates: содержит шаблоны страниц; 
  - admin.py - модуль, ответственный за регистрацию моделей, используемых в интерфейсе администратора; 
  - apps.py - модуль, определяющий конфигурацию приложения; 
  - form_validation.py - модуль, содержащий функции, ответственные за проверки заполнения полей формы; 
  - forms.py - модуль, определяющий класс EquationForm, форму для ввода параметров дифференциальных уравнений, и осуществляющий валидацию всех полей формы; 
  - models.py - хранит определение моделей (модель уравнения и модель решения); 
  - solver.py - модуль, содержащий функции, ответственные за алгоритмы решения дифференциальных уравнений и построение графиков полученных решений; 
  - tests.py - содержит тестовые классы, проверяющие корректность работы функций из модулей form_validation.py и solver.py; 
  - urls.py - модуль, хранящий конфигурацию url адресов приложения; 
  - views.py - модуль, определяющий функции, которые получают запросы пользователей, обрабатывают их и возвращают ответ;  

Static: содержит CSS файлы и хранит графики решений дифференциальных уравнений. 
  
  
Для запуска проекта нужно установить фреймворк Django, библиотеку matplotlib, адаптер psycopg2 для PostgreSQL, библиотеку pillow для работы 
с изображениями, библиотеки numexpr и numpy для вычислений, библиотеку python-dotenv. В главном приложении проекта difequation необходимо создать 
файл .env, в котором будут хранится две переменные окружения: SECRET_KEY  и PASSWORD, а также в модуле settings.py нужно будет настроить соединение 
с базой данных. Запуск осуществляется через команду python manage.py runserver в консоли.  
