import os
from pathlib import Path
from google import genai
from httpx import request
import markdown
from .models import AIQuery
from dotenv import load_dotenv
from django.conf import settings

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def dashboard(request):
    # 1. Current logged-in user ko hi student maan rahe hain
    student = request.user 
    
    # 2. Total registered users count
    total_students = User.objects.count()

    context = {
        'total_students': total_students,
        'student': student, # Ab ye sahi hai
        'user': request.user
    }
    
    return render(request, "dashboard/dashboard.html", context)

#def roadmap_view(request):
 #   return render(request, 'dashboard/roadmap.html')

@login_required
def progress_view(request):
    return render(request, 'dashboard/progress.html')

@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")



#.env file se API

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(settings.BASE_DIR, '.env'))

#api key from .env file
API_KEY = os.getenv("GEMINI_API_KEY")
#API_KEY = ""
if not API_KEY:
    print("Error: GEMINI_API_KEY nahi mili! Check karein ki .env file main folder mein hai.")
    client = None
else:
    client = genai.Client(api_key=API_KEY)

@login_required
def skill_advisor(request):
    if request.method == "POST":
        skill = request.POST.get('skill')
        
        prompt = f"Give me a detailed roadmap for {skill} for a beginner."

        try:
            # 1. Gemini API Call
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            ai_text = response.text
            html_content = markdown.markdown(ai_text)  # Agar aapko markdown se HTML convert karna hai

            # 2. Database mein save karein
            query_obj = AIQuery.objects.create(
                user_skill=skill, 
                recommendation=html_content
            )
            
            return render(request, 'dashboard/result.html', {'data': query_obj})

        except Exception as e:
            # Error handling
            print(f"MAIN ERROR YE HAI: {e}") 
            return render(request, 'dashboard/error.html', {'error': str(e)})

    return render(request, 'dashboard/roadmap.html')