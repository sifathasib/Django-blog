from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag
from .forms import CommentForm,EmailForm
from django.db.models import Count
# Create your views here.
def post_list(request,tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag =  get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list,2)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{
        'tag':tag,
        'page':page,
        'post':post
    }) 
    

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,publish__year= year,publish__month= month,publish__day= day)
    comments = post.comments.filter(active=True)
    new_comment= None
    if(request.method == 'POST'):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published .filter(tags__in = post_tags_ids).exclude(id= post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,'blog/post/detail.html',{
        'post':post,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form,
        'similar_posts':similar_posts
    })

def share_post(request,id):
    post = get_object_or_404(Post,id = id,status='published')
    sent=False
    if(request.method=='POST'):
        email_form = EmailForm(request.POST)
        cd = email_form.cleaned_data
        post_url = request.build_absolute_uri(post.get_absolute_url())
        subject = f"{cd['name']} recommands you to read {post.title}"
        message = f"read {post.title} at {post_url}\n\n{cd['name']}'s comments {cd['comment']}"
        send_mail(subject,message,'sifatdevelopmenttesting@gmail.com',cd['to'])
    else:
        email_form = EmailForm()
    return render(request,'blog/post/share.html',{
        'email_form':email_form,
        'post':post,
        'sent':sent
    })