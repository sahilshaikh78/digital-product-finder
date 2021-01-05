from django.urls import path
from client import views

urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('contact/',views.contact),
    path('user/send_inquiry/',views.save_inquiry),
    path('register/',views.signup),
    path('email_check/',views.email_check), 
    path('register-user/',views.register_user), 
    path('login/',views.login),
    path('login_auth/',views.login_auth),
    path('logout/',views.logout), 
    path('demo/',views.demo),
    path('personal_info_update/',views.personal_info_update),
    path('search_suggestion/',views.search_suggestion), 
    path('fetch_top_product_type/',views.fetch_top_product_type), 
    path('category/<slug:slug_text>/',views.category_search), 
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_type_search), 
    path('<slug:category_slug>-reviews/<slug:brand_slug>/',views.brand_profile), 
    path('<slug:category_slug>/add-review/brand/<slug:brand_slug>/',views.review), 
    path('review/save_review/',views.save_review), 
    path('save_expert_help/',views.save_expert_help), 
    path('<slug:category_slug>-comparison/<slug:brand_slug1>-vs-<slug:brand_slug2>/',views.compare_2_brand), 
    path('account/',views.account_profile_setting),  
    path('account/update-password/', views.account_change_password, name='account_change_password'),
    path('account/change-password/', views.change_password, name='change_password'),
    path('account/wishlist/', views.wishlist, name='wishlist'),
    path('account/reviews/', views.reviews, name='reviews'),
    path('save_wishlist/',views.save_wishlist), 
    path('remove_wishlist/',views.remove_wishlist), 
    path('delete_user_review/', views.delete_user_review, name='delete_user_review'),
    path('categories/',views.categories),
    path('price_chart/<slug:category_slug>/',views.price_chart), 
     

]
