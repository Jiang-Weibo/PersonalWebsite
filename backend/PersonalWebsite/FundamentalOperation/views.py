from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect,FileResponse
from django.template import loader
from django.shortcuts import render
#from FundamentalOperation.models import User
from FundamentalOperation import models
from django.urls import reverse
from PIL import ImageFile
from django.conf import settings
import eyed3 as e3
import os
import json

# Create your views here.


def view_home_html(request):
	# t = loader.get_template('home.html')
	# html = t.render()
	# return HttpResponse(html)
	#print("res is \n")
	#print(view_loginCheck_html(request))
	code = json.loads(view_loginCheck_html(request).content)
	if(code['response']=='NO'):
		return render(request, 'home.html')
	else:
		#print("response is NOT NO!")
		return HttpResponseRedirect(code['response'])



def view_loginCheck_html(request):
	#r = HttpRequest()
	# 给isLogin设置默认值，存在则不设置
	request.session.setdefault('isLogin','no')
	#如果已经登录则直接跳转到main页面
	if request.session['isLogin']=='yes':
		url = reverse('main')
		return JsonResponse({'response':url})

	login_id = request.POST.get('user_name','N/A')
	login_psw = request.POST.get('user_password','N/A')
	#qs是记录的集合
	qs = models.User.objects.values('user_name','user_password')
	#记录是一个字典
	for user in qs:
		if (user['user_name']==login_id) and (user['user_password']==login_psw):
			url = reverse('main')
			#将session设置为yes并且在session里添加用户名信息
			request.session['isLogin']='yes'
			request.session['user_name']=login_id
			return JsonResponse({'response':url})
	return JsonResponse({'response':'NO'})


def view_registerCheck_html(request):
	register_id = request.POST.get('user_name','N/A')
	register_password = request.POST.get('user_password','N/A')
	#print("register_id is "+register_id)
	#查看是否已被注册
	isValid = models.User.objects.filter(user_name=register_id)
	if(len(isValid)>0):
		return JsonResponse({'code':-1})
	models.User.objects.create(user_name=register_id,user_password=register_password)
	request.session['isLogin']='yes'
	request.session['user_name']=register_id
	return JsonResponse({'code':1,'url':'/home/main'})


def view_main_html(request):
	return render(request,'main.html');


def view_music_html(request):
	return render(request,'music.html');


def view_image_html(request):
	return render(request,'image.html');


def view_video_html(request):
	return render(request,'video.html');


def view_document_html(request):
	return render(request,'document.html');


def view_homework_html(request):
	return render(request,'homework.html');


def view_userinfo_html(request):

	return render(request,'userinfo.html')


def view_modifyUserInfo_html(request):
	user_name = request.session['user_name']
	user = models.User.objects.get(user_name=user_name)
	code = 0
	try:
		user.user_name = request.POST.get('user_name')
		user.user_password = request.POST.get('user_password')
		user.save()
		request.session['isLogin']='no'
		code = 1
	except Exception as e:
		code = -1
		raise e
	d = {}
	d['code']=code
	if code==1:
		d['url'] = '/home'
	return JsonResponse(d)



def view_logout_html(request):
	request.session['isLogin']='no'
	#url = reverse('')
	request.session['user_name']='null'
	print('logout')
	return JsonResponse({'url':'/home'})


def view_getImage_html(request):
	#通过session得到user_name
	un = request.session['user_name']
	#查询数据库
	#反向属性查询
	u = models.User.objects.get(user_name=un).image_set.all()
	url_dict = {}
	i=0
	for uu in u:
		url_dict[i] = uu.url
		i = i+1
	#print('set is '+settings.MEDIA_ROOT)
	return JsonResponse(url_dict)


def view_addImage_html(request):
	d = {}
	#确定目录
	virtualDir = settings.STATIC_URL+'images/'
	imgDir = 'F:\\JNU\\WebDevelop\\PersonalWebsite\\frontend\\static\\images\\'
	#异步传输，每次都传一个文件,得到的文件是Django封装的UploadedFile类型
	file = request.FILES.get('files','None')
	#写入本地文件
	with open(imgDir+file.name,'wb+') as f:
		f.write(file.read())
	#通过session得到当前登录的用户
	un = request.session['user_name']
	user = models.User.objects.get(user_name=un)
	#添加该用户的图片，注意这里Image的user_name应该是一个对象！！
	print('database: '+(virtualDir+file.name))
	models.Image.objects.create(user_name=user,url=virtualDir+file.name)
	return JsonResponse(d)


def view_inputTest_html(request):
	return render(request,'inputTest.html')


def view_getMusic_html(request):
	#通过session得到user_name
	un = request.session['user_name']
	print("in getMusic un = "+un)
	#查询数据库
	#反向属性查询
	u = models.User.objects.get(user_name=un).music_set.all()
	url_dict = {}
	i=0
	for uu in u:
		tempDic = {}
		tempDic['url'] = uu.url
		tempDic['singer_name'] = uu.singer_name
		tempDic['song_name'] = uu.song_name
		url_dict[i] = tempDic
		i = i+1
	#print('set is '+settings.MEDIA_ROOT)
	return JsonResponse(url_dict)


def view_getDocument_html(request):
	#通过session得到user_name
	un = request.session['user_name']
	#print("in getDocument un = "+un)
	#查询数据库
	#反向属性查询
	u = models.User.objects.get(user_name=un).document_set.all()
	url_dict = {}
	i=0
	for uu in u:
		tempDic = {}
		tempDic['content'] = uu.content
		tempDic['author'] = uu.author
		tempDic['title'] = uu.title
		tempDic['date'] = uu.date
		url_dict[i] = tempDic
		i = i+1
	#print('set is '+settings.MEDIA_ROOT)
	return JsonResponse(url_dict)


def view_addDocument_html(request):
	virtualDir = settings.STATIC_URL+'document/'
	documentDir = 'F:\\JNU\\WebDevelop\\PersonalWebsite\\frontend\\static\\document\\'
	author = request.POST.get('author','null')
	title = request.POST.get('title','null')
	mainBody = request.POST.get('mainBody','null')
	date = request.POST.get('date','null')
	user_name = request.session['user_name']
	user = models.User.objects.get(user_name=user_name)
	#写入数据库
	models.Document.objects.create(user_name=user,author=author,title=title,date=date,content=mainBody)
	return render(request,'main.html');


def view_deleteDocument_html(request):
	user_name = request.session['user_name']
	user = models.User.objects.get(user_name=user_name)
	title = request.POST.get('title')
	code = 0
	try:
		doc = models.Document.objects.get(user_name=user,title=title)
		doc.delete()
	except Exception as e:
		code = -1
		print("删除失败!")
		raise e
	d = {'code':code}
	return JsonResponse(d)


def view_modifyDocument_html(request):
	user_name = request.session['user_name']
	user = models.User.objects.get(user_name=user_name)
	originalTitle = request.POST.get('originalTitle')
	title = request.POST.get('title')
	author = request.POST.get('author')
	content = request.POST.get('content')
	date = request.POST.get('date')
	code = 0
	try:
		doc = models.Document.objects.get(user_name=user,title=originalTitle)
		doc.title = title
		doc.author = author
		doc.content = content
		doc.date = date
		print("date is "+date)
		doc.save()
	except Exception as e:
		code = -1
		print("修改失败!")
		raise e
	d = {'code':code}
	return JsonResponse(d)


def view_searchDocument_html(request):
	user_name = request.session['user_name']
	user = models.User.objects.get(user_name=user_name)
	keyWord = request.POST.get('keyWord')
	u = models.Document.objects.filter(user_name=user).filter(title__contains = keyWord)
	url_dict = {}
	i=0
	for uu in u:
		tempDic = {}
		tempDic['content'] = uu.content
		tempDic['author'] = uu.author
		tempDic['title'] = uu.title
		tempDic['date'] = uu.date
		url_dict[i] = tempDic
		i = i+1
	#print('set is '+settings.MEDIA_ROOT)
	return JsonResponse(url_dict)



def view_addMusic_html(request):
	d = {}
	#确定目录
	virtualDir = settings.STATIC_URL+'music/'
	musicDir = 'F:\\JNU\\WebDevelop\\PersonalWebsite\\frontend\\static\\music\\'
	#异步传输，每次都传一个文件,得到的文件是Django封装的UploadedFile类型
	file = request.FILES.get('files','None')
	#写入本地文件
	with open(musicDir+file.name,'wb+') as f:
		f.write(file.read())
	#通过session得到当前登录的用户
	un = request.session['user_name']
	user = models.User.objects.get(user_name=un)
	#添加该用户的图片，注意这里Image的user_name应该是一个对象！！
	#print('database: '+(virtualDir+file.name))
	fileName = e3.load(musicDir+file.name)
	#print(fileName.tag.title)
	models.Music.objects.create(user_name=user,url=virtualDir+file.name,song_name=fileName.tag.title,singer_name=fileName.tag.artist)
	return JsonResponse(d)


def view_getVideo_html(request):
	#通过session得到user_name
	un = request.session['user_name']
	print("in getVideo un = "+un)
	#查询数据库
	#反向属性查询
	u = models.User.objects.get(user_name=un).video_set.all()
	url_dict = {}
	i=0
	for uu in u:
		tempDic = {}
		tempDic['url'] = uu.url
		tempDic['video_name'] = uu.video_name
		url_dict[i] = tempDic
		i = i + 1
	#print('set is '+settings.MEDIA_ROOT)
	return JsonResponse(url_dict)


def view_downloadFile_html(request):
	#通过session得到user_name
	un = request.session['user_name']
	#print("in downloadFile un = "+un)
	systemPath = settings.STATICFILES_DIRS[0]
	print(systemPath)
	fileType = request.POST.get('type','N/A')
	if fileType=='music':
		#u = model.User.objects.get(user_name=un).music_set.all().filter()
		song_name = request.POST.get('song_name')
		singer_name = request.POST.get('singer_name')
		fileName = song_name+singer_name
		filePath = models.User.objects.get(user_name=un).music_set.all().get(song_name=song_name,singer_name=singer_name).url
		print(filePath)
		filePath = filePath.replace('statics','')
		filePath = systemPath+filePath
		print(filePath)
		response = FileResponse(open(filePath, 'rb'), filename=fileName, as_attachment=True)
		#response['Content-Type'] = 'application/octet-stream'
		return response

	return JsonResponse({'code':-1})