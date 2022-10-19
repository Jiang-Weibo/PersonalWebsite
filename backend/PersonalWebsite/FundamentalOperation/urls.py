from django.urls import path, include, re_path
from FundamentalOperation import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url
#此页面前缀为home
urlpatterns = [
	path('',views.view_home_html),
	path('loginCheck',views.view_loginCheck_html,name='loginCheck'),
	path('registerCheck',views.view_registerCheck_html,name='registerCheck'),
	path('main',view=views.view_main_html,name='main'),
	path('music',view=views.view_music_html,name='music'),
	path('image',view=views.view_image_html,name='image'),
	path('video',view=views.view_video_html,name='video'),
	path('document',view=views.view_document_html,name='document'),
	path('homework',view=views.view_homework_html,name='homework'),
	path('userinfo',view=views.view_userinfo_html,name='userinfo'),
	path('logout',view=views.view_logout_html,name='logout'),
	path('getImage',view=views.view_getImage_html,name='getImage'),
	path('addImage',view=views.view_addImage_html,name='addImage'),
	path('inputTest',view=views.view_inputTest_html,name='inputTest'),
	path('getMusic',view=views.view_getMusic_html,name='getMusic'),
	path('addMusic',view=views.view_addMusic_html,name='addMusic'),
	path('getVideo',view=views.view_getVideo_html,name='getVideo'),
	path('getDocument',view=views.view_getDocument_html,name='getDocument'),
	path('addDocument',view=views.view_addDocument_html,name='addDocument'),
	path('deleteDocument',view=views.view_deleteDocument_html,name='deleteDocument'),
	path('modifyDocument',view = views.view_modifyDocument_html,name='modifyDocument'),
	path('searchDocument',view = views.view_searchDocument_html,name='searchDocument'),
	path('modifyUserInfo',view = views.view_modifyUserInfo_html,name='modifyUserInfo'),
	path('downloadFile',view=views.view_downloadFile_html,name='downloadFile'),
]
