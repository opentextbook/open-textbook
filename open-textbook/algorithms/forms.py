from django import forms
from .models import Problem, Solution, Comment, TestCase
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class ProblemForm(forms.ModelForm):
    LEVEL = [
        ('브론즈', '브론즈'), 
        ('실버', '실버'),
        ('골드', '골드'), 
        ('플레티넘', '플레티넘')
        ]

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': '제목',

                }
            ),
        )
    problem_url = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'url',

                }
            ),
        )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': '내용',

                }
            ),
        )
    input = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': 'input',
                'style' : 'height: 80px',
                }
            ),
            initial='.'
        )  
    output = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': 'output',
                'style' : 'height: 80px',
                }
            ),
            initial='.'
        )    
    problem_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'placeholder': '문제 번호',

                }
            ),
        )     
 
    level = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': 'form-control'
                },
            choices=LEVEL,
            ),
        )  

    type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': '타입',
                
                }
            ),
            initial='비밀'
        )   
    class Meta:
        model = Problem
        exclude = ('user', 'like_users',)




class SolutionForm(forms.ModelForm):
    hint = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': '힌트를 입력해주세요.',
                'style' : 'height: 50px',
                }
            ),
            initial='힌트'
        )
    code = forms.CharField(widget=SummernoteWidget( attrs={'width': '50%', 'height': '400px'} ), label="Code", required=False )
            # attrs={
            #     # 'class':'form-control',
            #     # 'placeholder': '코드를 입력해주세요.',
            #     # 'style' : 'height: 200px',
            #     'content' : 'SummernoteWidget()',
            #     }

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': '코드 설명을 입력해주세요.',
                'style' : 'height: 100px',
                }
            ),
            initial='코드 설명'
        )
    class Meta:
        model = Solution
        exclude = ('problem', 'user', 'like_users',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('solution', 'user', 'like_users',)

class TestCaseForm(forms.ModelForm):

    input = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': 'input',
                'style' : 'height: 80px',
                }
            ),
        )  
    output = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': 'output',
                'style' : 'height: 80px',
                }
            ),
        )  

    class Meta:
        model = TestCase
        exclude = ('problem',)