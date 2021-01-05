from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from myadmin.models import Category, Product_type, Brand, Country, Feature, Product, Product_feature, Contact, Currency, ExpertHelp, Review
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core import mail
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.template import RequestContext
from .utils import render_to_pdf 


def index(request):
    return render(request,'admin_login.html')

def admin_auth(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        login_admin = authenticate(request, username = username, password = password)
        if login_admin:
            if login_admin.is_superuser:
                auth_login(request, login_admin)
                return HttpResponseRedirect('/sp-admin/dashboard/')  
            else:
                messages.error(request, "You're not Admin User! Please login as User") 
                return HttpResponseRedirect('/login/')    
        else:
            messages.error(request, "Invalid Username or Password!")
            return HttpResponseRedirect('/sp-admin/')

def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return HttpResponseRedirect('/sp-admin/')
    else:
        return HttpResponseRedirect('/sp-admin/')

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def dashboard(request):
    context={}
    user_count = User.objects.filter(is_superuser = 0).count()
    recent_user = User.objects.filter(is_superuser = 0).order_by('-date_joined')[:10]
    inquiry_count = Contact.objects.count()
    brand_count = Brand.objects.count()
    product_count = Product.objects.count()
    context={
        'user_count': user_count,
        'inquiry_count': inquiry_count,
        'brand_count': brand_count,
        'product_count': product_count,
        'recent_user': recent_user
    }
    return render(request,'dashboard.html', context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def setting(request):
    return render(request,'admin_setting.html')

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def admin_info_update(request):
    if request.method == "POST":
        user_id = request.user.id
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        User.objects.filter(id=user_id).update(first_name= first_name, last_name = last_name)
    return HttpResponse('')

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def category(request):
    context = {}
    try:
        category_data = Category.objects.all()
        if category_data:
            context['category_data'] = category_data
    except:
        messages.error(request, "Opps! Something went wrong Please try Again")
    return render(request,'category.html',context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def add_category(request):
    if request.method == "POST":
        add_category = request.POST['add_category']
        category_title = request.POST['category_title']
        category_slug = request.POST['category_slug']
        try:
            check_category = Category.objects.filter(category_slug = category_slug)
            if check_category:
                exists_err = {'error' : 'already exists!'}
                data = {
                    'is_taken': exists_err
                }
            else:
                obj = Category.objects.create(category_name = add_category, category_title = category_title ,category_slug = category_slug)
                data = {
                    'category_added': 'success'
                }
        except:
            data = {
                    'err': 'Opps! Something Went wrong please try again!'
            }
    return JsonResponse(data)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def product_type(request):
    context = {}
    try:
        category_name = Category.objects.only('category_name')
        context['category_name'] = category_name
        product_type_data = Product_type.objects.all()
        if product_type_data:
            context['product_type_data'] = product_type_data
    except:
        messages.error(request, "Opps! Something went wrong Please try Again")
    return render(request,'product_type.html',context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def add_product_type(request):
    if request.method == "POST":
        type_name = request.POST['type_name']
        type_title = request.POST['type_title']
        category = request.POST['category']
        type_slug = request.POST['type_slug']
        type_desc = request.POST['type_desc']
        try:
            check_type = Product_type.objects.filter(product_type_slug = type_slug)
            if check_type:
                exists_err = {'error' : 'already exists!'}
                data = {
                    'is_taken': exists_err
                }
            else:
                obj = Product_type.objects.create(product_type_name = type_name, 
                product_type_title = type_title ,product_type_description = type_desc, 
                category_id = category , product_type_slug = type_slug)
                type_data = {'type_id':obj.product_type_id,'type_name':obj.product_type_name,'type_slug':obj.product_type_slug}
                data = {
                    'type_data': type_data
                }
        except:
            data = {
                'err': "failed"
            }

    return JsonResponse(data)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def brand(request):
    context = {}
    try:
        category_name = Category.objects.only('category_name')
        country_data = Country.objects.all()
        context = {
            'category_name': category_name,
            'country_data' : country_data
        }
    except:
        messages.error(request, "Opps! Something went wrong Please try Again")
    return render(request,'add_brand.html',context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def add_brand(request):
    if request.method == "POST":
        brand_name = request.POST['brand_name']
        brand_slug = request.POST['brand_slug']
        brand_title = request.POST['brand_title']
        brand_website = request.POST['brand_website']
        brand_category = request.POST['category']
        brand_country = request.POST['country']
        brand_info = request.POST['brand_info']
        brand_desc = request.POST['brand_desc']
        brand_logo = request.FILES['brand_logo']
        brand_logo_alt_text = request.POST['logo_alt_text']
        try:
            check_brand = Brand.objects.filter(brand_slug = brand_slug)
            if check_brand:
                exists_err = {'error' : 'already exists!'}
                data = {
                    'is_taken': exists_err
                }
            else:
                obj = Brand.objects.create(brand_name = brand_name, brand_slug = brand_slug, brand_logo = brand_logo, 
                brand_logo_alt_text = brand_logo_alt_text, brand_title = brand_title, category_id = brand_category ,
                country_id = brand_country,brand_website = brand_website, brand_info = brand_info, brand_description = brand_desc)
                data = {
                    'brand_data': 'brand added'
                }
        except:
            data = {
                'err': "failed"
            }
        return JsonResponse(data)
    else:
        return HttpResponse("Opps! There is no data to save")

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def show_brand(request):
    context = {}
    try:
        brand_data = Brand.objects.all()
        context['brand_data'] = brand_data
    except:
        messages.error(request, "Opps! Something went wrong Please try Again")
    return render(request,'brand.html', context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def feature(request):
    context = {}
    try:
        feature_data = Feature.objects.all()
        product_type_data = Product_type.objects.values('product_type_id','product_type_name')
        context={
            'feature_data': feature_data,
            'product_type_data': product_type_data
        }
    except:
        messages.error(request, "Opps! Something went wrong Please try Again")
    return render(request,'feature.html',context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def add_feature(request):
    if request.method == "POST":
        feature = request.POST['feature']
        product_type = request.POST['product_type']
        feature_has_value = request.POST['feature_has_value']
        try:
            feature_check = Feature.objects.filter(product_type_id = product_type, feature_name = feature)
            if feature_check:
                data = {
                    'feature_exist': 'feature_exist'
                }
            else:
                obj = Feature.objects.create(feature_name = feature, product_type_id = product_type, feature_has_value = feature_has_value)
                data = {
                    'feature_added': 'success'
                }
        except:
            data = {
                'err': 'Opps! Something Went wrong please try again!'
            }
    return JsonResponse(data)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def product(request):
    context = {}
    try:
        product_data = Product.objects.all()
        context['product_data'] = product_data
    except:
        messages.error(request, "Opps! Something went wrong Please try Again")
    return render(request,'product.html', context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def new_product(request):
    context={}
    product_type_data = Product_type.objects.values('product_type_id','product_type_name') 
    brand_data = Brand.objects.values('brand_id','brand_name') 
    currency_data = Currency.objects.values('currency_id', 'currency_symbol')
    context={
        'product_type_data': product_type_data,
        'brand_data': brand_data,
        'currency_data': currency_data,
    }
    return render(request, 'new-product.html', context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def add_product(request):
    if request.method == "POST":
        product_title = request.POST['product_title']
        product_info = request.POST['product_info']
        product_name = request.POST['product_name']
        product_slug = request.POST['product_slug']
        product_link = request.POST['product_link']
        product_price = request.POST['product_price']
        currency_id = request.POST['currency']
        price_term = request.POST['price_term']
        product_brand = request.POST['brand']
        product_type = request.POST['product_type']
        product_desc = request.POST['product_desc']
        
        try:
            check_product = Product.objects.filter(product_slug = product_slug)
            if check_product:
                exists_err = {'error' : 'already exists!'}
                data = {
                    'is_taken': exists_err
                }
            else:
                obj = Product.objects.create(product_title = product_title, product_info = product_info,
                 product_name = product_name, product_slug = product_slug, product_price = product_price, 
                 currency_id = currency_id, product_subscription = price_term, product_link = product_link, product_type_id = product_type, brand_id = product_brand, product_description = product_desc)
                data = {
                    'product_data': 'product added'
                }
        except:
            data = {
                'err': "failed"
            }
        return JsonResponse(data)
    else:
        return HttpResponse("Opps! There is no data to save")

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def edit_features(request, product_id):
    product_data = get_object_or_404(Product, product_id=product_id)
    if product_data:
        features_data = Feature.objects.filter(product_type_id = product_data.product_type_id)
        product_feature_check = Product_feature.objects.filter(product_id = product_id)
        if product_feature_check:
            context = {
                'features_data': features_data,
                'product_data': product_data
            }
        else:
            context = {
                'features_data': features_data,
                'product_data': product_data

            }  
    else:
        return HttpResponse("Opps! Product Not Found")
    return render(request, 'product-features.html', context)

def inquiries(request):
    inquiry_data = Contact.objects.all()
    context={
        'inquiry_data': inquiry_data
    }
    return render(request, 'inquiries.html', context)

def inquiry_reply(request, contact_id):
    inquiry_data = get_object_or_404(Contact, contact_id = contact_id)
    if inquiry_data:
        context = {
            'inquiry_data': inquiry_data,
        }
    else:
        return HttpResponse("Opps! Inquiry Not Found")
    return render(request, 'inquiry-reply.html', context)

def inquiry_reply_send(request):
    if request.method == "POST":
        contact_id = request.POST['contact_id']
        reply = request.POST['reply']
        contact_data = Contact.objects.get(contact_id = contact_id)
        if contact_data:
            subject = 'Your Inquiry Reply - Suggest Point'
            data = {'name': contact_data.name,
                    'message': contact_data.message,
                    'reply': reply,
                   }
            html_message = render_to_string('inquiry_reply_mail.html' , data)
            plain_message = strip_tags(html_message)
            from_email = 'Suggest Point Team'
            to = contact_data.email
            email_send  = mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            if email_send:
                print(email_send)
                update_status = Contact.objects.filter(contact_id = contact_id).update(status = 'completed')
                if update_status:
                    data = {
                        'sent': 'success'
                    }
            else:
                data = {
                    'err': 'error'
                }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def inquiry_delete(request):
    if request.method == "POST":
        contact_id = request.POST['contact_id']
        delete_inquiry = Contact.objects.filter(contact_id = contact_id).delete()
        if delete_inquiry:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def expert_help_inquiries(request):
    inquiry_data = ExpertHelp.objects.all()
    context={
        'inquiry_data': inquiry_data
    }
    return render(request, 'expert-help.html', context)

def expert_help_reply(request, help_id):
    inquiry_data = get_object_or_404(ExpertHelp, help_id = help_id)
    if inquiry_data:
        context = {
            'inquiry_data': inquiry_data,
        }
    else:
        return HttpResponse("Opps! Inquiry Not Found")
    return render(request, 'expert-help-reply.html', context)

def expert_help_reply_send(request):
    if request.method == "POST":
        help_id = request.POST['help_id']
        reply = request.POST['reply']
        contact_data = ExpertHelp.objects.get(help_id = help_id)
        if contact_data:
            subject = 'Expert Help Inquiry Reply  - Suggest Point'
            data = {'name': contact_data.customer_name,
                    'message': contact_data.customer_note,
                    'ticket': contact_data.ticket_code,
                    'reply': reply, 
                   }
            html_message = render_to_string('expert-help-reply-mail.html' , data)
            plain_message = strip_tags(html_message)
            from_email = 'suggestpoint.info@gmail.com'
            to = contact_data.customer_email
            email_send  = mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            if email_send:
                update_status = ExpertHelp.objects.filter(help_id = help_id).update(status = 'completed')
                if update_status:
                    data = {
                        'sent': 'success'
                    }
            else:
                data = {
                    'err': 'error'
                }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def expert_help_inquiry_delete(request):
    if request.method == "POST":
        help_id = request.POST['help_id']
        delete_inquiry = ExpertHelp.objects.filter(help_id = help_id).delete()
        if delete_inquiry:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def product_delete(request):
    if request.method == "POST":
        product_id = request.POST['product_id']
        delete_product = Product.objects.filter(product_id = product_id).delete()
        if delete_product:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def brand_delete(request):
    if request.method == "POST":
        brand_id = request.POST['brand_id']
        delete_brand = Brand.objects.filter(brand_id = brand_id).delete()
        if delete_brand:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def feature_delete(request):
    if request.method == "POST":
        feature_id = request.POST['feature_id']
        delete_feature = Feature.objects.filter(feature_id = feature_id).delete()
        if delete_feature:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')


def product_type_delete(request):
    if request.method == "POST":
        product_type_id = request.POST['product_type_id']
        delete_product_type = Product_type.objects.filter(product_type_id = product_type_id).delete()
        if delete_product_type:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def category_delete(request):
    if request.method == "POST":
        category_id = request.POST['category_id']
        delete_category = Category.objects.filter(category_id = category_id).delete()
        if delete_category:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def show_user(request):
    user_data = User.objects.filter(is_superuser = 0)
    context={
        'user_data': user_data
    }
    return render(request, 'user.html', context)

def user_delete(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        delete_user = User.objects.filter(id = user_id).delete()
        if delete_user:
            data = {
                'deleted': 'deleted',
            }
        else:
            data = {
                'err': 'error'
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Opps! Nothing found here')

def generate_user_pdf(request, *args, **kwargs):
    users_data = User.objects.filter(is_superuser = 0)
    if users_data:
        context = {
            'users_data': users_data,
            }
        pdf = render_to_pdf('user-pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Users_%s.pdf" %("Suggest_Point_Users_Details")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
                response['Content-Disposition'] = content
            return response
        else:
            return HttpResponse("Not found")
    else:
        return HttpResponseRedirect('No users Found') 

def edit_category(request, category_id):
    category_data = get_object_or_404(Category, category_id = category_id)
    context = {
        'category_data': category_data,
    }
    return render(request, 'edit-category.html', context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def update_category(request):
    if request.method == "POST":
        edit_category_name = request.POST['edit_category_name']
        edit_category_title = request.POST['edit_category_title']
        edit_category_slug = request.POST['edit_category_slug']
        category_id = request.POST['category_id']
        try:
            check_category = Category.objects.filter(category_slug = edit_category_slug).exclude(category_id = category_id)
            if check_category:
                data = {
                    'is_taken': 'exists'
                }
            else:
                updated = Category.objects.filter(category_id = category_id).update(category_name = edit_category_name,category_title = edit_category_title, category_slug = edit_category_slug)
                if updated:
                    data = {
                        'updated': 'success'
                    }
                else:
                    data = {
                        'err': 'error'
                    }
        except:
            data = {
                    'err': 'Opps! Something Went wrong please try again!'
            }
    return JsonResponse(data)

def edit_product_type(request, product_type_id):
    product_type_data = get_object_or_404(Product_type, product_type_id = product_type_id)
    category_data = Category.objects.exclude(category_id = product_type_data.category_id)
    context = {
        'product_type_data': product_type_data,
        'category_data':category_data,
    }
    return render(request, 'edit-product-type.html', context)
    
@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def update_product_type(request):
    if request.method == "POST":
        edit_product_type_name = request.POST['edit_product_type_name']
        edit_product_type_title = request.POST['edit_product_type_title']
        category = request.POST['category']
        edit_product_type_slug = request.POST['edit_product_type_slug']
        edit_product_type_desc = request.POST['edit_product_type_desc']
        product_type_id = request.POST['product_type_id']
        try:
            check_product_type = Product_type.objects.filter(product_type_slug = edit_product_type_slug).exclude(product_type_id = product_type_id)
            if check_product_type:
                data = {
                    'is_taken': 'exists'
                }
            else:
                updated = Product_type.objects.filter(product_type_id = product_type_id).update(product_type_name = edit_product_type_name,
                product_type_title = edit_product_type_title, category_id = category, product_type_slug = edit_product_type_slug,
                product_type_description = edit_product_type_desc)
                if updated:
                    data = {
                        'updated': 'success'
                    }
                else:
                    data = {
                        'err': 'error'
                    }
        except:
            data = {
                    'err': 'Opps! Something Went wrong please try again!'
            }
    return JsonResponse(data)

def edit_feature(request, feature_id):
    feature_data = get_object_or_404(Feature, feature_id = feature_id)
    product_type_data = Product_type.objects.exclude(product_type_id = feature_data.product_type_id)
    context = {
        'feature_data': feature_data,
        'product_type_data':product_type_data,
    }
    return render(request, 'edit-feature.html', context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def update_feature(request):
    if request.method == "POST":
        edit_feature = request.POST['edit_feature']
        product_type = request.POST['product_type']
        feature_has_value = request.POST['feature_has_value']
        feature_id = request.POST['feature_id']
        try:
            check_feature = Feature.objects.filter(feature_name = edit_feature).exclude(feature_id = feature_id)
            if check_feature:
                data = {
                    'is_taken': 'exists'
                }
            else:
                updated = Feature.objects.filter(feature_id = feature_id).update(feature_name = edit_feature,
                product_type_id = product_type, feature_has_value = feature_has_value)
                if updated:
                    data = {
                        'updated': 'success'
                    }
                else:
                    data = {
                        'err': 'error'
                    }
        except:
            data = {
                    'err': 'Opps! Something Went wrong please try again!'
            }
    return JsonResponse(data)

def edit_brand(request, brand_id):
    brand_data = get_object_or_404(Brand, brand_id = brand_id)
    category_data = Category.objects.exclude(category_id = brand_data.category_id)
    country_data = Country.objects.exclude(country_id = brand_data.country_id)
    context = {
        'brand_data': brand_data,
        'category_data':category_data,
        'country_data': country_data,
    }
    return render(request, 'edit-brand.html', context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def update_brand(request):
    if request.method == "POST":
        brand_name = request.POST['brand_name']
        brand_slug = request.POST['brand_slug']
        brand_title = request.POST['brand_title']
        brand_website = request.POST['brand_website']
        brand_category = request.POST['category']
        brand_country = request.POST['country']
        brand_info = request.POST['brand_info']
        brand_desc = request.POST['brand_desc']
        brand_id = request.POST['brand_id']
        try:
            check_brand = Brand.objects.filter(brand_slug = brand_slug).exclude(brand_id = brand_id)
            if check_brand:
                data = {
                    'is_taken': 'exists'
                }
            else:
                updated = Brand.objects.filter(brand_id = brand_id).update(brand_name = brand_name, brand_slug = brand_slug,
                brand_title = brand_title, category_id = brand_category ,
                country_id = brand_country, brand_website = brand_website ,brand_info = brand_info, brand_description = brand_desc)
                if updated:
                    data = {
                        'updated': 'success'
                    }
                else:
                    data = {
                        'err': 'error'
                    }
        except:
            data = {
                    'err': 'Opps! Something Went wrong please try again!'
            }
    return JsonResponse(data)

def edit_product(request, product_id):
    product_data = get_object_or_404(Product, product_id = product_id)
    product_type_data = Product_type.objects.exclude(product_type_id = product_data.product_type_id)
    brand_data = Brand.objects.exclude(brand_id = product_data.brand_id)
    currency_data = Currency.objects.values('currency_id', 'currency_symbol')

    context = {
        'product_data': product_data,
        'product_type_data':product_type_data,
        'brand_data': brand_data,
        'currency_data': currency_data,
    }
    return render(request, 'edit-product.html', context)

@login_required(login_url='/sp-admin/')
@staff_member_required(login_url='/login/')
def update_product(request):
    if request.method == "POST":
        product_title = request.POST['product_title']
        product_info = request.POST['product_info']
        product_name = request.POST['product_name']
        product_slug = request.POST['product_slug']
        product_price = request.POST['product_price']
        product_currency = request.POST['currency']
        product_price_term = request.POST['price_term']
        product_link = request.POST['product_link']
        product_brand = request.POST['brand']
        product_type = request.POST['product_type']
        product_desc = request.POST['product_desc']
        product_id = request.POST['product_id']
        try:
            check_product = Product.objects.filter(product_slug = product_slug).exclude(product_id = product_id)
            if check_product:
                data = {
                    'is_taken': 'exists'
                }
            else:
                updated = Product.objects.filter(product_id = product_id).update(product_title = product_title, product_info = product_info,
                 product_name = product_name, product_slug = product_slug, product_price = product_price, 
                 currency_id = product_currency, product_subscription = product_price_term, product_link = product_link, product_type_id = product_type, brand_id = product_brand, product_description = product_desc)
                if updated:
                    data = {
                        'updated': 'success'
                    }
                else:
                    data = {
                        'err': 'error'
                    }
        except:
            data = {
                    'err': 'Opps! Something Went wrong please try again!'
            }
    return JsonResponse(data)

def pending_reviews(request):
    review_data = Review.objects.filter(review_status = 'pending')
    context={
        'review_data': review_data
    }
    return render(request, 'reviews.html', context)

def review_delete(request):
    if request.method == "POST":
        review_id = request.POST['review_id']
        delete_review = Review.objects.filter(review_id = review_id).delete()
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
        return HttpResponse('Opps! Nothing found here')
def review_approve(request, review_id):
    delete_review = Review.objects.filter(review_id = review_id).update(review_status = 'approved')
    if delete_review:
        messages.success(request,'Review Approved Successfully!')
        return HttpResponseRedirect('/sp-admin/review/')
    else:
        messages.error(request,'Review Approved failed! Please Try Again')
        return HttpResponseRedirect('/sp-admin/review/')

def approved_reviews(request):
    review_data = Review.objects.filter(review_status = 'approved')
    context={
        'review_data': review_data
    }
    return render(request, 'approved-reviews.html', context)