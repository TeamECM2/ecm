from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from tutorial.authhelper import get_signin_url, get_token_from_code, get_user_email_from_id_token
from tutorial.outlookservice import get_my_messages
from lxml import html
import pickle
import os
#import tokenizer

def home(request):
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user_email = get_user_email_from_id_token(token['id_token'])
  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['user_email'] = user_email
  return HttpResponseRedirect(reverse('tutorial:mail'))

def mail(request):
  access_token = request.session['access_token']
  user_email = request.session['user_email']
  # If there is no token in the session, redirect to home
  if not access_token:
  	return HttpResponseRedirect(reverse('tutorial:home'))
  else:
  	messages = get_my_messages(access_token, user_email)
  	if 'value' not in messages:
  		return render(request, 'tutorial/mail.html', dict())
  	for i in range(0, len(messages['value'])):
  		messages['value'][i]['Body']['Content'] = html.fromstring(messages['value'][i]['Body']['Content']).text_content() 	
  		pickle.dump( messages['value'][i]['Body']['Content'], open( "save.p", "wb" ), protocol=2 )
  		os.system("py tokenizer.py")
  		a = pickle.load(open("temp.p", "rb"))
  		messages['value'][i]['Body']['Keywords'] = (','.join(a))
  	context = { 'messages': messages['value'] }
  	return render(request, 'tutorial/mail.html', context)