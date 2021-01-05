from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from myadmin.models import Category, Product, Product_type, Brand, Feature, Contact, Review, Product_feature, ExpertHelp, WishList
from django.db.models import Q, Prefetch
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import OuterRef, Subquery, F, Min
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.template.loader import get_template
from django.template import Context
from django.core import mail
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.template import RequestContext
from social_django.models import UserSocialAuth

def demo(request):
    '''try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        #request.META.get('REMOTE_ADDR')
        g = GeoIP2('geoip/GeoLite2-Country_20200107/GeoLite2-Country.mmdb')
        x = g.country(ip)
        return HttpResponse(x['country_name'])
    except:
        return HttpResponse("No problem it's just conflict")'''
    return render(request,'demo.html')


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def login(request):
    if request.user.is_authenticated:
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return HttpResponseRedirect('/')    
    else:
        return render(request,'login.html')

def signup(request):
    if request.user.is_authenticated:
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return HttpResponseRedirect('/') 
    else:
        return render(request,'signup.html')
# Create your views here.
def save_inquiry(request):
    if request.method == 'POST':
         name = request.POST['name']
         email = request.POST['email']
         mobile = request.POST['mobile']
         message = request.POST['message']

         Contact.objects.create(
             name = name,
             email = email,
             mobile = mobile,
             message = message,
             status = 'pending',
         )

    return HttpResponse('')

def email_check(request):
    if request.method == 'POST':
        email = request.POST['email']
        data = {
        'is_taken': User.objects.filter(email=email).exists()
         }
        if data['is_taken']:
            data['error_message'] = 'Email already exists!'
        else:
            data['success_message'] = 'Email is Okay!'
    return JsonResponse(data)


def register_user(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            username = email.split("@")[0]
            save_user = User.objects.create_user(username = username, first_name = name, email = email, password = password)
            if save_user:
                user = authenticate(request, username = username, password = password)
                if user:
                    if user.is_superuser == 0:          
                        auth_login(request, user)
                        messages.success(request,'You are succesfully Registered!')
                        if 'next' in request.POST:
                            return redirect(request.POST.get('next'))
                        else:
                            return HttpResponseRedirect('/')  
                    else:
                        messages.info(request, "You're Admin user so go to admin to login")
                        return render(request,'/')
                else:
                    messages.error(request, "Invalid Username and Password")
                    return render(request,'login.html')   
            else:
                messages.error(request,'Registration failed! please try again')
                return HttpResponseRedirect('/register/')
        except:
            messages.info(request,'Opps! something went wrong please try again')
            return HttpResponseRedirect('/register/')
    return HttpResponseRedirect('/register/')

@login_required(login_url='/login/')
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  

def login_auth(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        username = email.split("@")[0]
        login_user = authenticate(request, username = username, password = password)
        if login_user:
            auth_login(request, login_user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect('/')  
        else:
            messages.error(request, "Invalid Username or Password!")
            return HttpResponseRedirect('/login/')    

@login_required(login_url='/login/')
def account_profile_setting(request):
    context = {
        'setting': 'profile'
    }
    return render(request, 'account.html', context)

@login_required(login_url='/login/')
def account_change_password(request):
    user_auth_check = UserSocialAuth.objects.filter(user_id = request.user.id)
    if user_auth_check:
        context = {
        'setting': 'password',
        'social_auth': 'yes'
        }
    else:
        context = {
        'setting': 'password',
        'social_auth': 'no'
        }
    
    return render(request, 'account.html', context)

@login_required(login_url='/login/')
def wishlist(request):
    wishlist_data = WishList.objects.filter(user_id = request.user.id).select_related('brand')
    if wishlist_data:
        context = {
            'setting': 'wishlist',
            'wishlist_data': wishlist_data
        }
    else:  
        context = {
            'setting': 'wishlist',
        }
    return render(request, 'account.html', context)

@login_required(login_url='/login/')
def reviews(request):
    user_review = Review.objects.filter(user_id = request.user.id)

    if user_review:
        review_data = Brand.objects.filter(brand_id__in = [brand.brand_id for brand in user_review])
        review_data = zip(user_review,review_data)
        context = {
            'setting': 'review',
            'review_data': review_data
        }
    else:  
        context = {
            'setting': 'review',
        }
    return render(request, 'account.html', context)

@login_required(login_url='/login/')
def personal_info_update(request):
    if request.method == "POST":
        user_id = request.user.id
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        User.objects.filter(id=user_id).update(first_name= first_name, last_name = last_name)
    return HttpResponse('')


"""def slug_demo(request, slug_text):
    
    data = get_object_or_404(Product_type, type_slug=slug_text)
    if data:
        return HttpResponse(data.type_description)
    else:
        return HttpResponse("<h1>Opps! Fool Man nothing Found</h1>")"""

def search_suggestion(request):
    if request.method == "GET":
        if 'search_query' in request.GET:
            search_query = list(request.GET['search_query'].split())
            if search_query != '':
                for item in search_query:
                    category_data = Category.objects.filter(category_name__icontains=item).values('category_name','category_slug')
                    product_type_data = Product_type.objects.filter(product_type_name__icontains=item).values('product_type_name','product_type_slug','category__category_slug')[:10]
                    brand_data = Brand.objects.filter(brand_name__icontains=item).values('brand_name','brand_slug','category__category_slug')[:10]
                data = {}
                data = {
                    'category_data' : list(category_data),
                    'product_type_data' : list(product_type_data),
                    'brand_data' : list(brand_data),

                }
                return JsonResponse(data,safe=False)        
            else:
                return HttpResponse("OPPS! nothing found here:)")
        return HttpResponse("OPPS! nothing found here:)")
    return HttpResponse("OPPS! nothing found here:)")

def fetch_top_product_type(request):
    if request.method == "GET":
        product_type_data = Product_type.objects.values('product_type_name','product_type_slug','category__category_slug')[0:20]
        data = {}
        data = {
            'product_type_data' : list(product_type_data),
        }
        return JsonResponse(data,safe=False)        
    return HttpResponse("OPPS! nothing found here:)")


#searching views started
def category_search(request, slug_text):
    context={}
    category_data = Category.objects.filter(category_slug = slug_text)
    if category_data:
        category_data = Category.objects.get(category_slug = slug_text)
        brand_data = Product.objects.filter(
                brand__category__category_slug = slug_text
            ).annotate(
                min_brand_price=Min('brand__products__product_price')
            ).filter(
                product_price=F('min_brand_price')
            ).order_by('product_price').prefetch_related('product_features')
        top_brands = Brand.objects.filter(category__category_slug = slug_text).prefetch_related(
            Prefetch('products', queryset=Product.objects.annotate(
                min_brand_price=Min('brand__products__product_price')
            ).filter(
                product_price=F('min_brand_price')
            ).order_by('product_id').prefetch_related('product_features')))
        review_data = {}
        for brand_id in brand_data:
            review_res = Review.objects.filter(brand_id = brand_id.brand_id)
            count = 0
            overall_rating = 0
            for data in review_res:
                overall_rating = overall_rating + data.overall_rating
                count = count + 1
            try:
                overall_rating = overall_rating/count
            except:
                overall_rating = 0
            if overall_rating <= 5.0 and overall_rating > 4.5:
                overall_rating = 5
            elif overall_rating > 4.0 and overall_rating <= 4.5:
                overall_rating = 4.5
            elif overall_rating <= 4.0 and overall_rating > 3.5:
                overall_rating = 4.0
            elif overall_rating > 3.0 and overall_rating <= 3.5:
                overall_rating = 3.5
            elif overall_rating <= 3.0 and overall_rating > 2.5:
                overall_rating  = 3.0
            elif overall_rating > 2.0 and overall_rating <= 2.5:
                overall_rating = 2.5
            elif overall_rating <= 2.0 and overall_rating > 1.5:
                overall_rating = 2.0
            elif overall_rating > 1.0 and overall_rating <= 1.5:
                overall_rating = 1.5
            else:
                overall_rating = 1.0
            review_data[brand_id.brand_id] = overall_rating
        product_type_data = Product_type.objects.filter(category__category_slug = slug_text).values('product_type_name','product_type_slug')
        result_count = brand_data.count()
        paginator = Paginator(brand_data, 5)
        page = request.GET.get('page')
        try:
            brand_result = paginator.page(page)
        except PageNotAnInteger:
            brand_result = paginator.page(1)
        except EmptyPage:
            brand_result = paginator.page(paginator.num_pages)
        context={
            'category_data': category_data,
            'result_count' : result_count,
            'product_type_data': product_type_data,
            'brand_result':brand_result,
            'review_data': review_data,
            'top_brands': top_brands,
        }
    else:
        return HttpResponse("Opps! Nothing Found")

    return render(request,'category-search.html', context)

def product_type_search(request, category_slug, product_slug):
    context={}
    product_type_res = Product_type.objects.filter(category__category_slug = category_slug, product_type_slug = product_slug)
    if product_type_res:
        product_type_res1 = Product_type.objects.get(product_type_slug = product_slug)
        category_data = Category.objects.get(category_slug = category_slug)
        brand_data = Product.objects.filter(
                product_type__product_type_slug = product_slug
            ).annotate(
                min_brand_price=Min('brand__products__product_price')
            ).filter(
                product_price=F('min_brand_price')
            ).order_by('product_price').prefetch_related('product_features')
        top_brands = Brand.objects.filter(category__category_slug = category_slug).prefetch_related(
            Prefetch('products', queryset=Product.objects.annotate(
                min_brand_price=Min('brand__products__product_price')
            ).filter(
                product_price=F('min_brand_price')
            ).order_by('product_id').prefetch_related('product_features')))
        review_data = {}
        for brand_id in brand_data:
            review_res = Review.objects.filter(brand_id = brand_id.brand_id)
            count = 0
            overall_rating = 0
            for data in review_res:
                overall_rating = overall_rating + data.overall_rating
                count = count + 1
            try:
                overall_rating = overall_rating/count
            except:
                overall_rating = 0
            if overall_rating <= 5.0 and overall_rating > 4.5:
                overall_rating = 5
            elif overall_rating > 4.0 and overall_rating <= 4.5:
                overall_rating = 4.5
            elif overall_rating <= 4.0 and overall_rating > 3.5:
                overall_rating = 4.0
            elif overall_rating > 3.0 and overall_rating <= 3.5:
                overall_rating = 3.5
            elif overall_rating <= 3.0 and overall_rating > 2.5:
                overall_rating  = 3.0
            elif overall_rating > 2.0 and overall_rating <= 2.5:
                overall_rating = 2.5
            elif overall_rating <= 2.0 and overall_rating > 1.5:
                overall_rating = 2.0
            elif overall_rating > 1.0 and overall_rating <= 1.5:
                overall_rating = 1.5
            else:
                overall_rating = 1.0
            review_data[brand_id.brand_id] = overall_rating
        product_type_data = Product_type.objects.filter(Q(category__category_slug=category_slug) & ~Q(product_type_slug=product_slug)).values('product_type_name','product_type_slug')
        result_count = brand_data.count()
        paginator = Paginator(brand_data, 5)
        page = request.GET.get('page')
        try:
            product_result = paginator.page(page)
        except PageNotAnInteger:
            product_result = paginator.page(1)
        except EmptyPage:
            product_result = paginator.page(paginator.num_pages)
        context={
            'product_type_data': product_type_data,
            'category_data': category_data,
            'result_count' : result_count,
            'product_result': product_result,
            'review_data': review_data,
            'top_brands': top_brands,
            'product_type_res': product_type_res,
            'product_type_res1': product_type_res1
        }
    else:
        return HttpResponse("Opps! Nothing Found")

    return render(request,'product-search.html', context)

def brand_profile(request, category_slug, brand_slug):
    context = {}
    brand_path = request.path.split('/')[2]
    category_url = request.path.split('/')[1].split('-')[0]
    brand_data = Brand.objects.get(brand_slug = brand_slug)
    review_rating_data = Review.objects.filter(brand_id = brand_data.brand_id, review_status = 'approved')
    product_data = Product.objects.filter(brand__brand_id = brand_data.brand_id).prefetch_related('product_features').order_by('product_type_id')
    alternatives_data = Brand.objects.filter(category__category_slug = category_slug).exclude(brand_slug = brand_slug).prefetch_related(
    Prefetch('products', queryset=Product.objects.annotate(
                min_brand_price=Min('brand__products__product_price')
            ).filter(
                product_price=F('min_brand_price')
            ).order_by('product_id').prefetch_related('product_features')))

    wishlist_data = WishList.objects.filter(user_id = request.user.id, brand_id = brand_data.brand_id).count()
    overall_rating_count = 0
    features_rating_count = 0
    vfm_count = 0
    eou_count = 0
    cs_count = 0
    row_count = 0
    for ratings in review_rating_data:
        overall_rating_count = overall_rating_count + ratings.overall_rating
        features_rating_count = features_rating_count + ratings.features_rating
        vfm_count = vfm_count + ratings.value_for_money_rating
        eou_count = eou_count + ratings.ease_of_use_rating
        cs_count = cs_count + ratings.customer_support_rating
        row_count = row_count + 1
    try:
        overall_rating_count = overall_rating_count/row_count
        features_rating_count = features_rating_count/row_count
        vfm_count = vfm_count/row_count
        eou_count = eou_count/row_count
        cs_count = cs_count/row_count
    except:
        overall_rating_count = 0
    rating_count_list = [overall_rating_count, features_rating_count, vfm_count, eou_count, cs_count]
    counter = 0
    for counts in rating_count_list:
        if counts <= 5.0 and counts > 4.5:
            counts = 5
        elif counts > 4.0 and counts <= 4.5:
            counts = 4.5
        elif counts <= 4.0 and counts > 3.5:
            counts = 4.0
        elif counts > 3.0 and counts <= 3.5:
            counts = 3.5
        elif counts <= 3.0 and counts > 2.5:
            counts  = 3.0
        elif counts > 2.0 and counts <= 2.5:
            counts = 2.5
        elif counts <= 2.0 and counts > 1.5:
            counts = 2.0
        elif counts > 1.0 and counts <= 1.5:
            counts = 1.5
        else:
            counts = 1.0
        counter = counter + 1
        if counter == 1:
            overall_rating_count = counts
        elif counter == 2:
            features_rating_count = counts
        elif counter == 3:
            vfm_count = counts
        elif counter == 4:
            eou_count = counts
        else:
            cs_count = counts 
    feature_rating_dict = {
        'features_rating_count': { 
            'name': 'Feature',
            'rating': features_rating_count,
         },
         'vfm_count':{
             'name': 'Value for money',
             'rating': vfm_count,
         },
        'eou_count':{
            'name': 'Ease of use',
            'rating': eou_count,
        },
        'cs_count': {
            'name': 'Customer support',
            'rating': cs_count,    
        },
    }
    context={
        'category_url': category_url,
        'brand_path': brand_path,
        'brand_data': brand_data,
        'overall_rating': overall_rating_count,
        'review_rating_data': review_rating_data,
        'feature_rating_dict': feature_rating_dict,
        'product_data': product_data,
        'alternatives_data': alternatives_data,
        'wishlist_data': wishlist_data,
    }

    return render(request,'brand-profile.html', context)

def price_chart(request, category_slug):
    label = []
    price = []
    brand_name_to_price_map = dict(
        Product.objects.filter(
            brand__category__category_slug = category_slug
        ).annotate(min_brand_price=Min('brand__products__product_price')
            ).filter(
                product_price=F('min_brand_price')
            ).order_by(
             'product_price'
        ).values_list(
            'brand__brand_name',
            'product_price',
        )
    )
    for key,value in brand_name_to_price_map.items(): 
        label.append(key)
        price.append(value)
    data={
        'label': label,
        'data': price,
    }
    return JsonResponse(data)

def review(request, category_slug, brand_slug):
    context = {}
    user_id = request.user.id
    category_path = request.path.split('/')[1]
    brand_path = request.path.split('/')[4]
    brand_data = Brand.objects.get(brand_slug = brand_slug)

    user_review_check = Review.objects.filter(user_id = user_id, brand_id = brand_data.brand_id)
    if(user_review_check):
        context={
            'category_url': category_path,
            'brand_path': brand_path,
            'brand_data': brand_data,
            'user_review_exists': 'review_exists'
        }
    else:    
        context={
            'category_url': category_path,
            'brand_path': brand_path,
            'brand_data': brand_data
        }

    print(context)
    return render(request, 'review.html', context)

def save_review(request):
    if request.method == "POST":
        user_id = request.user.id
        features_count = request.POST.get('features_count')
        value_for_money_count = request.POST.get('value_for_money_count')
        ease_of_use_count = request.POST.get('ease_of_use_count')
        customer_support_count = request.POST.get('customer_support_count')
        review_title = request.POST.get('review_title')
        review_body = request.POST.get('review_body')
        brand_id = request.POST.get('brand_id')
        overall_rating = (float(features_count) + float(value_for_money_count) + float(ease_of_use_count) + float(customer_support_count)) / 4
        if overall_rating <= 5.0 and overall_rating > 4.5:
            overall_rating = 5
        elif overall_rating > 4.0 and overall_rating <= 4.5:
            overall_rating = 4.5
        elif overall_rating <= 4.0 and overall_rating > 3.5:
            overall_rating = 4.0
        elif overall_rating > 3.0 and overall_rating <= 3.5:
            overall_rating = 3.5
        elif overall_rating <= 3.0 and overall_rating > 2.5:
            overall_rating  = 3.0
        elif overall_rating > 2.0 and overall_rating <= 2.5:
            overall_rating = 2.5
        elif overall_rating <= 2.0 and overall_rating > 1.5:
            overall_rating = 2.0
        elif overall_rating > 1.0 and overall_rating <= 1.5:
            overall_rating = 1.5
        else:
            overall_rating = 1.0
        user_review_check = Review.objects.filter(user_id = user_id, brand_id = brand_id)
        if(user_review_check):
            data = {
            'exists': 'exists'
            }
        else:
            try:
                obj = Review.objects.create(brand_id = brand_id, 
                features_rating = features_count, value_for_money_rating = value_for_money_count,
                ease_of_use_rating = ease_of_use_count, customer_support_rating = customer_support_count,
                overall_rating = overall_rating, review = review_body, user_id = user_id, review_title = review_title)
                if obj:
                    data = {
                        'review_added': 'success'
                    }
                else:
                    data = {
                        'not_added': 'err'
                    }            
            except:
                data = {
                    'not_added': 'err'
                }
    return JsonResponse(data)


def save_expert_help(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        customer_email = request.POST['customer_email']
        customer_mo_number = request.POST['customer_mo_number']
        suggestion_category = request.POST['suggestion_category']
        customer_help_note = request.POST['customer_help_note']
        customer_inquiry_page_url = request.get_full_path()

        inquiry_saved  = ExpertHelp.objects.create(
             customer_name = customer_name,
             customer_email = customer_email,
             customer_mobile = customer_mo_number,
             customer_note = customer_help_note,
             status = 'pending',
             customer_help_category_id = suggestion_category,
             customer_inquiry_page_url = customer_inquiry_page_url
         )
        if inquiry_saved:
            saved_inquiry_data = ExpertHelp.objects.get(help_id = inquiry_saved.help_id)
            subject = 'Great! Your Expert Suggestions Help Sucessfully Booked - Suggest Point'
            data = {'customer_name': customer_name,
                    'suggestion_category':suggestion_category,
                    'ticket_code': saved_inquiry_data.ticket_code,
                   }
            html_message = render_to_string('suggestion_confirm_mail.html' , data)
            plain_message = strip_tags(html_message)
            from_email = 'Suggest Point Team'
            to = customer_email
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            data = {
                'saved': 'success'
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse("Opps! nothing found here.")

def compare_2_brand(request, category_slug, brand_slug1, brand_slug2):
    context = {}
    brand_data_1 = get_object_or_404(Brand, brand_slug=brand_slug1)
    brand_data_2 = get_object_or_404(Brand, brand_slug=brand_slug2)
    review_rating_data_1 = Review.objects.filter(brand_id = brand_data_1.brand_id)
    review_rating_data_2 = Review.objects.filter(brand_id = brand_data_2.brand_id)
    review_data_1 = Review.objects.filter(brand_id = brand_data_1.brand_id)[:3]
    review_data_2 = Review.objects.filter(brand_id = brand_data_2.brand_id)[:3]
    review_data = zip(review_data_1,review_data_2)
    features_rating_count_1 = 0
    vfm_count_1 = 0
    eou_count_1 = 0
    cs_count_1 = 0
    features_rating_count_2 = 0
    vfm_count_2 = 0
    eou_count_2 = 0
    cs_count_2 = 0
    row_count_1 = 0
    row_count_2 =0
    if(review_rating_data_1):
        for ratings_1 in review_rating_data_1:
            features_rating_count_1 = features_rating_count_1 + ratings_1.features_rating
            vfm_count_1 = vfm_count_1 + ratings_1.value_for_money_rating
            eou_count_1 = eou_count_1 + ratings_1.ease_of_use_rating
            cs_count_1 = cs_count_1 + ratings_1.customer_support_rating
            row_count_1 = row_count_1 + 1
        try:
            features_rating_count_1 = features_rating_count_1/row_count_1
            vfm_count_1 = vfm_count_1/row_count_1
            eou_count_1 = eou_count_1/row_count_1
            cs_count_1 = cs_count_1/row_count_1
        except:
            features_rating_count_1,vfm_count_1,eou_count_1,cs_count_1 = 0


    if(review_rating_data_2):
        for ratings_2 in review_rating_data_2:
            features_rating_count_2 = features_rating_count_2 + ratings_2.features_rating
            vfm_count_2 = vfm_count_2 + ratings_2.value_for_money_rating
            eou_count_2 = eou_count_2 + ratings_2.ease_of_use_rating
            cs_count_2 = cs_count_2 + ratings_2.customer_support_rating
            row_count_2 = row_count_2 + 1
        try:
            features_rating_count_2 = features_rating_count_2/row_count_2
            vfm_count_2 = vfm_count_2/row_count_2
            eou_count_2 = eou_count_2/row_count_2
            cs_count_2 = cs_count_2/row_count_2
        except:
            features_rating_count_2,vfm_count_2,eou_count_2,cs_count_2 = 0

    rating_count_list_1 = [features_rating_count_1, vfm_count_1, eou_count_1, cs_count_1]
    rating_count_list_2 = [features_rating_count_2, vfm_count_2, eou_count_2, cs_count_2]

    counter_1 = 0
    for counts in rating_count_list_1:
        if counts <= 5.0 and counts > 4.5:
            counts = 5.0
        elif counts > 4.0 and counts <= 4.5:
            counts = 4.5
        elif counts <= 4.0 and counts > 3.5:
            counts = 4.0
        elif counts > 3.0 and counts <= 3.5:
            counts = 3.5
        elif counts <= 3.0 and counts > 2.5:
            counts  = 3.0
        elif counts > 2.0 and counts <= 2.5:
            counts = 2.5
        elif counts <= 2.0 and counts > 1.5:
            counts = 2.0
        elif counts > 1.0 and counts <= 1.5:
            counts = 1.5
        else:
            counts = 1.0
        counter_1 = counter_1 + 1
        if counter_1 == 1:
            features_rating_count_1 = counts
        elif counter_1 == 2:
            vfm_count_1 = counts
        elif counter_1 == 3:
            eou_count_1 = counts
        else:
            cs_count_1 = counts 
    counter_2 = 0
    for counts_2 in rating_count_list_2:
        if counts_2 <= 5.0 and counts_2 > 4.5:
            counts_2 = 5.0
        elif counts_2 > 4.0 and counts_2 <= 4.5:
            counts_2 = 4.5
        elif counts_2 <= 4.0 and counts_2 > 3.5:
            counts_2 = 4.0
        elif counts_2 > 3.0 and counts_2 <= 3.5:
            counts_2 = 3.5
        elif counts_2 <= 3.0 and counts_2 > 2.5:
            counts_2  = 3.0
        elif counts_2 > 2.0 and counts_2 <= 2.5:
            counts_2 = 2.5
        elif counts_2 <= 2.0 and counts_2 > 1.5:
            counts_2 = 2.0
        elif counts_2 > 1.0 and counts_2 <= 1.5:
            counts_2 = 1.5
        else:
            counts_2 = 1.0
        counter_2 = counter_2 + 1
        if counter_2 == 1:
            features_rating_count_2 = counts_2
        elif counter_2 == 2:
            vfm_count_2 = counts_2
        elif counter_2 == 3:
            eou_count_2 = counts_2
        else:
            cs_count_2 = counts_2
    rating_dict = {
        'features_rating_count': { 
            'name': 'Feature',
            'rating': features_rating_count_1,
            'rating_2': features_rating_count_2,
         },
         'vfm_count':{
             'name': 'Value for money',
             'rating': vfm_count_1,
             'rating_2': vfm_count_2,
         },
        'eou_count':{
            'name': 'Ease of use',
            'rating': eou_count_1,
            'rating_2': eou_count_2,
        },
        'cs_count': {
            'name': 'Customer support',
            'rating': cs_count_1, 
            'rating_2': cs_count_2,    
        },
    }
    if brand_data_1 and brand_data_2:
        context = {
            'brand_data_1': brand_data_1,
            'brand_data_2': brand_data_2,
            'rating_dict': rating_dict,
            'review_data': review_data,
        }
        return render(request, 'compare_brand.html', context)
    else:
        return HttpResponse("not found")

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/account/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change-password.html', {
        'form': form
    })


def save_wishlist(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        brand_id = request.POST['brand_id']
        wishlist_check = WishList.objects.filter(brand_id = brand_id, user_id = user_id).count()
        if wishlist_check == 1:
            data = {
                'exists': 'exists'
            }
        else:
            wishlist_saved  = WishList.objects.create(
                user_id = user_id,
                brand_id = brand_id,
            )
            if wishlist_saved:
                data = {
                    'saved': 'success'
                }
            else:
                data = {
                    'err': 'error'
                }
        return JsonResponse(data)
    else:
        return HttpResponse("Opps! nothing found here.")

def remove_wishlist(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        brand_id = request.POST['brand_id']
        wishlist_check = WishList.objects.filter(brand_id = brand_id, user_id = user_id).count()
        if wishlist_check == 1:
            wishlist_deleted = WishList.objects.filter(brand_id = brand_id, user_id = user_id).delete()
            if wishlist_deleted:
                data = {
                    'deleted': 'success'
                }
            else:
                data = {
                    'err': 'error'
                }
        else:
            data = {
                'not_exists': 'exists'
            }

        return JsonResponse(data)
    else:
        return HttpResponse("Opps! nothing found here.")

def categories(request):
    category_data = Category.objects.all().prefetch_related('product_types')
    context = {
        'category_data': category_data
    }
    return render(request, 'categories.html', context)

def delete_user_review(request):
    if request.method == 'POST':
        review_id = request.POST['review_id']
        user_id = request.user.id
        delete_review = Review.objects.filter(review_id = review_id, user_id = user_id).delete()
        if delete_review:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse("Opps! nothing found here.")