from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import TextForm
from .models import(
    Blog,
    Category,
    Reply,
    Tag,
    Comment,
)

# Create your views here.

def home(request):
    blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    context = {
        "blogs": blogs,
        "tags": tags
    }
    return render(request, 'home.html', context)

def blogs(request):
    queryset = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')
    
    context = {
        "blogs": blogs,
        "tags": tags,
        "paginator": paginator
    }
    return render(request, 'blogs.html', context)


def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Blog.objects.order_by('-created_date')[:5]
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs
    }
    return render(request, 'category_blogs.html', context)

def tag_blogs(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = tag.tag_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Blog.objects.order_by('-created_date')[:5]
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs
    }
    return render(request, 'category_blogs.html', context)

def blog_details(request, slug):
    form = TextForm
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id=blog.category.id)
    related_blogs = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:5]

    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                user = request.user,
                blog = blog,
                text = form.cleaned_data.get('text'),
            )
            return redirect('blog_details', slug=slug)

    context = {
        "blog": blog,
        "related_blogs" : related_blogs,
        "tags": tags,
        "form": form,
    }
    return render(request, 'blog_details.html', context)

@login_required(login_url='/')
def add_reply(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )
    return redirect('blog_details', slug=blog.slug)

def search_blogs(request):
    search_key = request.GET.get('search', None)
    recent_blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    
    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key)
        ).distinct()

        context = {
            "blogs": blogs,
            "recent_blogs": recent_blogs,
            "tags": tags,
            "search_key": search_key
        }

        return render(request, 'search.html', context)

    else:
        return redirect('home')
