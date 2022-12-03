from django.shortcuts import render, HttpResponse, redirect

from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
from django.db.models import Q
import django_excel as excel
from home.models import Excel
import csv

csv_f="a"
# Create your views here.
def index(request):
    data = Excel.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        Excel.objects.filter(
            Q(Title_icontains=q) | Q(authors_icontains=q)
            | Q(dbid_icontains=q))

    return render(request, 'index.html', {'data': data})
#if i>0 or k==o and pp=1:

def search(request):
    global csv_f
    query = str(request.GET['query']).strip()

    allPosts = Excel.objects.filter()#here something wrong vro 
    str_1=query.replace("and"," & ").replace("or"," | ").replace("{","").replace("}","")
    str_3=str_1.split()
    str_2=[]
    for i in str_3:
      a=i.replace(" ","")
      str_2.append(a)
    s=""
    for i in str_2:
        if i!="|":
          if i!="&":
            s+=str(i+" ").replace(i,f"Q(Title__contains='{i}')")
        if i.strip()=="|":
          s+="|"
        if i.strip()=="&":
          s+="&"
    f_s=s.replace(") Q(",") | Q(")
    print(f_s)
    new_allposts = allPosts.filter(eval(str(f_s)))
    allPosts=new_allposts
    csv_f=allPosts
    params = {'allPosts': allPosts}
    return render(request, 'search.html', params)

def venue_csv(request):
    global csv_f
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment,filename=venues.text'
    writer = csv.writer(response)
    venues = Excel.objects.all()
    writer.writerow(['Title', 'Author', 'WOSid'])
    for i in csv_f:
        writer.writerow([i.Title, i.authors, i.dbid])
#doctype','Keywords','Source'
#i.Docu,i.Keyw,i.Source
    return response
