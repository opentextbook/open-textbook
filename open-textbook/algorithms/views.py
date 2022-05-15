from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from algorithms.models import Problem, Solution, TestCase, Comment
from .forms import ProblemForm, SolutionForm, CommentForm, TestCaseForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
@require_safe
def problem_index(request):
    problems = Problem.objects.order_by('-problem_number')

    f_levels = request.GET.get('level')
    if f_levels != '전부' and f_levels: #filtered level이 존재한다면
        query = Q()
        for f_level in f_levels:
            query = query | Q(level__icontains=f_level)
            problems = problems.filter(query).order_by('-problem_number')
    else:
        f_levels = '전부'

    f_nums = request.GET.get('num') if request.GET.get('num') else ''
    if f_nums.isdigit():
        query = Q()
        query = query | Q(problem_number__icontains=f_nums)
        problems = problems.filter(query).order_by('-problem_number')

    paginator = Paginator(problems, 20) # 20은 한 페이지에 보일 글 수

    page_number = request.GET.get('page') # 현재 페이지 넘버
    page_obj = paginator.get_page(page_number)

    page_numbers_range = 10
    max_index = len(paginator.page_range) # 총 페이지 수
    current_page = int(page_number) if page_number else 1 # 페이지 넘버가 0일때(초기화면) 1로 바꿔줌

    previous_page = 0 
    if current_page > 10: # 만약 현재 페이지가 11 이상일 때 전으로 가는 버튼 활성화 
        previous_page = ((current_page - 1) // page_numbers_range) * page_numbers_range # 그 버튼 누르면 가는 페이지(11~20은 10으로 감) 

    next_page = 0
    if max_index > 10 and ((current_page - 1) // page_numbers_range) != ((max_index - 1) // page_numbers_range): # 총 페이지 수가 10 이상이고, 마지막 칸(27이 총 페이지 수라면 21~27)이 아닐 경우
        next_page = ((current_page - 1) // page_numbers_range + 1) * page_numbers_range + 1 # 그 버튼 누르면 가는 페이지(1~10은 11로 감)

    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range # 현재 페이지가 13이라면 11 ~ 20까지 보여주기 위한 인덱스들
    end_index = start_index + page_numbers_range
    if end_index >= max_index: # 11 ~ 20을 봐야 되는데 총 페이지가 16이라면 16까지로 바꿔줌
        end_index = max_index
    page_range = paginator.page_range[start_index:end_index] # 위에서 계산한 범위만큼 화면에 표시

    levels = ['브론즈', '실버', '골드', '플레티넘']

    context = {
        'problems' : page_obj,
        'page_range' : page_range,
        'previous_page' : previous_page,
        'next_page' : next_page,
        'current_page' : current_page,
        'levels' : levels,
        'current_level' : f_levels,
        'search_num' : f_nums
    }
    return render(request, 'algorithms/problem_index.html', context)

@require_http_methods(['GET', 'POST'])
def problem_create(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('algorithms:problem_index')
    else:
        form = ProblemForm()
    context = {
        'form':form,
    }
    return render(request, 'algorithms/problem_create.html', context)

@require_safe
def problem_detail(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    context = {
        'problem': problem,
    }
    return render(request, 'algorithms/problem_detail.html', context)

@require_http_methods(['GET', 'POST'])
def problem_update(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect('algorithms:problem_detail', problem_pk)
    else:
        form = ProblemForm(instance=problem)
    context = {
        'problem': problem,
        'form': form,
    }
    return render(request, 'algorithms/problem_update.html', context)

def problem_delete(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    if request.method == "POST":
        problem.delete()
        return redirect('algorithms:problem_index')
    return redirect('algorithms:problem_detail', problem.pk)

@require_safe
def solution_index(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    solutions = problem.solution_set.order_by('-like_users')
    comment_form = CommentForm()
    context = {
        'solutions' : solutions,
        'problem' : problem,
        'comment_form' : comment_form
    }
    return render(request, 'algorithms/solution_index.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def solution_create(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    if request.method == 'POST':
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.user = request.user
            solution.problem = problem
            solution.save()
            return redirect('algorithms:solution_index', problem.pk)
    else:
        form = SolutionForm()
    context = {
        'form': form,
        'problem': problem,
    }
    return render(request, 'algorithms/solution_create.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def solution_update(request, problem_pk, solution_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    solution = get_object_or_404(Solution, pk=solution_pk)
    if request.user == solution.user:
        if request.method == 'POST':
            form = SolutionForm(request.POST, instance=solution)
            if form.is_valid():
                form.save()
                return redirect('algorithms:solution_index', problem.pk)
        else:
            form = SolutionForm(instance=solution)
    else:
        return redirect('algorithms:solution_index', problem.pk)
    context = {
        'problem': problem,
        'form': form,
    }
    return render(request, 'algorithms/solution_update.html', context)

@require_POST
def solution_delete(request, problem_pk, solution_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    solution = get_object_or_404(Solution, pk=solution_pk)
    if request.user.is_authenticated:
        if request.user == solution.user:
            solution.delete()
    return redirect('algorithms:solution_index', problem.pk)

@require_POST
def solution_comment(request, problem_pk, solution_pk):
    if request.user.is_authenticated:
        problem = get_object_or_404(Problem, pk=problem_pk)
        solution = get_object_or_404(Solution, pk=solution_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.solution = solution
            comment.save()
        return redirect('algorithms:solution_index', problem.pk)
    return redirect('accounts:signin')

def solution_comment_delete(request, problem_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('algorithms:solution_index', problem_pk)

@require_POST
def solution_like(request, problem_pk, solution_pk):
    if request.user.is_authenticated:
        problem = get_object_or_404(Problem, pk=problem_pk)
        solution = get_object_or_404(Solution, pk=solution_pk)
        if solution.like_users.filter(pk=request.user.pk).exists():
            solution.like_users.remove(request.user)
            liked = False
        else:
            solution.like_users.add(request.user)
            liked = True
        context = {
            'liked': liked,
            'count': solution.like_users.count()
        }
        return JsonResponse(context)
    return HttpResponse(status=401)

@require_safe
def testcase_index(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    testcases = problem.testcase_set.all()
    context = {
        'testcases': testcases,
        'problem': problem
    }
    return render(request, 'algorithms/testcase_index.html', context)

@require_http_methods(['GET', 'POST'])
def testcase_create(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.problem = problem
            form.save()
            return redirect('algorithms:testcase_index', problem.pk)
    else:
        form = TestCaseForm()
    context = {
        'problem': problem,
        'form': form
    }
    return render(request, 'algorithms/testcase_create.html', context)

@require_http_methods(['GET', 'POST'])
def testcase_update(request, problem_pk, testcase_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    testcase = get_object_or_404(TestCase, pk=testcase_pk)
    if request.method == 'POST':
        form = TestCaseForm(request.POST, instance=testcase)
        if form.is_valid():
            form.save()
            return redirect('algorithms:testcase_index', problem.pk)
    else:
        form = TestCaseForm(instance=testcase)
    context = {
        'problem': problem,
        'form': form
    }
    return render(request, 'algorithms/testcase_update.html', context)


@require_POST
def testcase_delete(request, problem_pk, testcase_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    testcase = get_object_or_404(TestCase, pk=testcase_pk)
    if request.user.is_authenticated:
        if request.user.is_superuser: #관리자 권한이 있는 자만 삭제 가능
            testcase.delete()
    return redirect('algorithms:testcase_index', problem.pk)