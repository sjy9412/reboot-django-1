from django.shortcuts import render
from .models import Job
from faker import Faker
import requests
from decouple import config

# Create your views here.
def index(request):
    return render(request, 'jobs/index.html')

def result(request):
    name = request.POST.get('name')
    try: 
        job = Job.objects.get(name=name)
    except:
        fake = Faker('en')
        job = Job.objects.create(name=name, job=fake.job())
    info = Job.objects.get(name=name)

    # 직업 결과에 따라, giphy 요청
    api_key = config('GIPHY_API_KEY')
    # 1. url 설정
    url = f'http://api.giphy.com/v1/gifs/search?api_key={api_key}&q={info.job}'
    # 2. 요청 보내기
    response = requests.get(url).json()
    # 3. 응답 결과에서 이미지 url 뽑기
    try:
        image_url = response['data'][0].get('images').get('original').get('url')
    except:
        image_url = None
    context = {
        'info': info,
        'image_url': image_url
    }
    return render(request, 'jobs/result.html', context)



