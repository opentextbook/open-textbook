from django.urls import path
from . import views
app_name = 'algorithms'

urlpatterns = [
    # 문제
    path('', views.problem_index, name='problem_index'),
    path('create/', views.problem_create, name='problem_create'),
    path('<int:problem_pk>/', views.problem_detail, name='problem_detail'),
    path('<int:problem_pk>/update/', views.problem_update, name='problem_update'),
    path('<int:problem_pk>/delete/', views.problem_delete, name='problem_delete'),
    # 솔루션
    path('<int:problem_pk>/solution/', views.solution_index, name='solution_index'),
    path('<int:problem_pk>/solution/create/', views.solution_create, name='solution_create'),
    path('<int:problem_pk>/solution/<int:solution_pk>/update/', views.solution_update, name='solution_update'),
    path('<int:problem_pk>/solution/<int:solution_pk>/delete/', views.solution_delete, name='solution_delete'),
    path('<int:problem_pk>/solution/<int:solution_pk>/comments/', views.solution_comment, name='solution_comment'),
    path('<int:problem_pk>/solution/comments/<int:comment_pk>/delete/', views.solution_comment_delete, name='solution_comment_delete'),
    path('<int:problem_pk>/solution/<int:solution_pk>/likes/', views.solution_like, name='solution_like'),
    # 테스트케이스
    path('<int:problem_pk>/testcase/', views.testcase_index, name='testcase_index'),
    path('<int:problem_pk>/testcase/create/', views.testcase_create, name='testcase_create'),
    path('<int:problem_pk>/testcase/<int:testcase_pk>/update/', views.testcase_update, name='testcase_update'),
    path('<int:problem_pk>/testcase/<int:testcase_pk>/delete/', views.testcase_delete, name='testcase_delete'),
]
