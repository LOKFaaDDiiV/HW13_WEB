from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote, Author, Tag
from .forms import TagForm, QuoteForm, AuthorForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/index.html', {"quotes": quotes})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:index')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for t in choice_tags.iterator():
                new_quote.tags.add(t)

            return redirect(to='quotes:index')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, 'form': form})

    return render(request, 'quotes/quote.html', {"tags": tags, 'form': QuoteForm()})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:index')
        else:
            return render(request, 'quotes/add_author.html', {'form': form})

    return render(request, 'quotes/add_author.html', {'form': AuthorForm()})


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author.html', {"author": author})
