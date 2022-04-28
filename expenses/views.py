from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from products.forms import SearchForm, DateForm, DestroyObjectForm
from django.contrib.postgres.search import SearchVector

@login_required
def expenses_list(request):

    search_form = SearchForm()

    date_form = DateForm()

    query = None

    date_query_start = None
    date_query_end = None

    expenses = Expense.objects.filter(user=request.user)

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            expenses = expenses.annotate(search=SearchVector('nombre'),).filter(search=query)

    if 'date_query_start' and 'date_query_end' in request.GET:
        form = DateForm(request.GET)
        if form.is_valid():
            date_query_start = form.cleaned_data['date_query_start'].strftime("%Y-%m-%d")
            date_query_end = form.cleaned_data['date_query_end'].strftime("%Y-%m-%d")
            expenses = expenses.filter(fecha__range=[date_query_start, date_query_end])



    return render(request, 'expenses/expenses_list.html',{
                                                            'expenses':expenses,
                                                            'search_form':search_form,
                                                            'date_form':date_form,
                                                            'query':query,
                                                            'date_query_start':date_query_start,
                                                            'date_query_end':date_query_end,
                                                            })

@login_required
def expense_create(request):

    expense_form = ExpenseForm(request.POST or None)

    if expense_form.is_valid():  
        tipo = expense_form.cleaned_data.get('tipo')
        nombre = expense_form.cleaned_data.get('nombre')
        monto = expense_form.cleaned_data.get('monto')

        attrs = {'tipo':tipo, 'nombre':nombre, 
            'monto':monto, 'user':request.user}

        new_expense = Expense(**attrs)
        new_expense.save()

        return redirect('expenses:expenses_list')

    return render(request, 'expenses/expense_create.html',{'expense_form':expense_form})

@login_required
def expense_detail(request, id):

    expense = get_object_or_404(Expense, id=id)

    if request.method == 'POST':
        destroy_object_form = DestroyObjectForm(request.POST)
        expense.delete()
        
        return redirect('expenses:expenses_list')
        
    else:
        destroy_object_form = DestroyObjectForm()

    return render(request,'expenses/expense_detail.html', {'expense':expense,
                                                            'destroy_object_form':destroy_object_form,
                                                            })

