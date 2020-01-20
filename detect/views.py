import mimetypes
import os
import sys
from fileinput import filename
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import details, ImageOb
from django.contrib.auth.models import User
from . import ocr
from .forms import ImageObForm
import random

class Streaming:

    @staticmethod
    def home(request):
        dicti={'hideim': 'hidden'}
        if request.method == "POST":
            form = ImageObForm(request.POST, request.FILES)
            if form.is_valid():

                print('valid')
                img = form.cleaned_data.get("image")
                title = form.cleaned_data.get("title")
                obj = ImageOb.objects.create(
                    image=img,
                    title=title
                )

                ImageOb.objects.all().delete()
                obj.save()
                dicti = Streaming.detect(request)

        context = {}
        context['form'] = ImageObForm(initial={'title': random.randint(1111, 9999)})
        context.update(dicti)
        return render(request, 'greenEye/index2.html', context)

    @staticmethod
    def load(request):
        if request.method == "POST":
            form = ImageObForm(request.POST, request.FILES)
            #if form.is_valid():
            print('valid')
            img = form.cleaned_data.get("image")
            title = form.cleaned_data.get("title")
            obj = ImageOb.objects.create(
                img=img
            )
            obj.save()

        return redirect('/')

    @staticmethod
    def detect(request):
        img = ImageOb.objects.latest('pk').image
        dicti = ocr.trace_plate(img.url.split('/')[-1])
        return dicti

    @staticmethod
    def go_live(request):
        return render(request, 'go_live.html')

    @staticmethod
    def download(request):
        img = ImageOb.objects.latest('pk').image
        wrapper = FileWrapper(open(os.path.join(sys.path[0],img.url)))  # img.file returns full path to the image
        content_type = mimetypes.guess_type(filename)[0]  # Use mimetypes to get file type
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(img.file)
        response['Content-Disposition'] = "attachment; filename=%s" % img.name
        return response

    @staticmethod
    def detect_again(request):
        img = ImageOb.objects.latest('pk').image
        return {'dicti': img.url}
