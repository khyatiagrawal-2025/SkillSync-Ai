import os
from pathlib import Path
from google import genai
#from import Groq
import markdown
from django.shortcuts import get_object_or_404

from dotenv import load_dotenv
from django.conf import settings

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

# Aapke saare models ek hi line mein import kar diye hain
from .models import AIQuery, UserProgressProfile, UserSkill, Task, UserBadge, SavedAIRoadmap
from home import models # Agar home app se kuch chahiye ho toh

# .env file se API setup
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(settings.BASE_DIR, '.env'))

# API key from .env file
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY nahi mili! Check karein ki .env file mein hai.")
    client = None
else:
    client = genai.Client(api_key=API_KEY)


# -------------------------------------------------------------------
# 1. Dashboard View
# -------------------------------------------------------------------
@login_required
@never_cache
def dashboard(request):
    # Current logged-in user ko hi student maan rahe hain
    student = request.user 
    # Total registered users count
    total_students = User.objects.count()

    context = {
        'total_students': total_students,
        'student': student,
        'user': request.user
    }
    return render(request, "dashboard/dashboard.html", context)


# -------------------------------------------------------------------
# 2. Roadmap Base View
# -------------------------------------------------------------------
def roadmap_view(request):
    return render(request, 'dashboard/roadmap.html')


# -------------------------------------------------------------------
# 3. Settings View
# -------------------------------------------------------------------
@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")


# -------------------------------------------------------------------
# 4. AI Skill Advisor (Generate & Save Roadmap)
# -------------------------------------------------------------------
@login_required
def skill_advisor(request):
    if request.method == "POST":
        skill = request.POST.get('skill')

        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        # 🔥 SMART PROMPT: AI ko text aur table dono use karne ka instruction
        prompt = f"""
        Act as an expert mentor. Give me a detailed, step-by-step roadmap to learn {skill} for a complete beginner. 
        
        Please structure your response intelligently:
        1. Use clear text paragraphs and bullet points for explanations, tips, and theory.
        2. MUST include a Markdown Table to summarize the timeline, topics, or resources (e.g., Week | Topic | Resources).
        
        Keep the formatting clean and engaging.
        """

        try:
            # 1. Gemini se data mangwana
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            ai_text = response.text

            # 2. Markdown ko HTML mein convert karna (Text ko paragraph, Table ko <table> banayega)
            html_content = markdown.markdown(ai_text, extensions=['tables', 'fenced_code'])

            # 3. AIQuery table mein save karna (Aapka purana DB)
            query_obj = AIQuery.objects.create(
                user_skill=skill, 
                recommendation=html_content
            )

            # 4. SavedAIRoadmap table mein save karna (Progress Page ke liye)
            SavedAIRoadmap.objects.create(
                user=request.user,
                title=f"{skill.capitalize()} Roadmap", 
                ai_content=html_content
            )
            
            # 5. Result page par final HTML bhejna
            return render(request, 'dashboard/result.html', {'data': query_obj})

        except Exception as e:
            # Agar koi API ya DB error aaye toh crash hone ke bajaye error.html par bhejna
            print(f"MAIN ERROR YE HAI: {e}") 
            return render(request, 'dashboard/error.html', {'error': str(e)})

    # Agar request GET hai (page normal khula hai form fill karne ke liye)
    return render(request, 'dashboard/roadmap.html')

# -------------------------------------------------------------------
# 5. Progress Dashboard (Main UI View)
# -------------------------------------------------------------------
@login_required
def progress_dashboard(request):
    user = request.user
    
    # 1. Get or Create Profile
    profile, created = UserProgressProfile.objects.get_or_create(user=user)
    
    # 2. Fetch Skills, Tasks, and Badges
    skills = UserSkill.objects.filter(user=user).order_by('-proficiency')
    recent_tasks = Task.objects.filter(user=user).order_by('-created_at')[:10]
    earned_badges = UserBadge.objects.filter(user=user).select_related('badge')
    
    # 3. Fetch Saved AI Roadmaps (Ye ab Skill Advisor se aayega)
    saved_roadmaps = SavedAIRoadmap.objects.filter(user=user).order_by('-generated_at')
    
    # 4. Next Level Math
    xp_for_next_level = profile.current_level * 250 
    xp_remaining = max(0, xp_for_next_level - profile.total_xp)
    level_progress_pct = (profile.total_xp / xp_for_next_level) * 100 if xp_for_next_level > 0 else 0

    context = {
        'profile': profile,
        'skills': skills,
        'recent_tasks': recent_tasks,
        'earned_badges': earned_badges,
        'saved_roadmaps': saved_roadmaps,
        'xp_remaining': xp_remaining,
        'xp_for_next_level': xp_for_next_level,
        'level_progress_pct': min(level_progress_pct, 100), # Cap at 100%
    }
    
    return render(request, 'dashboard/progress.html', context)

#roadmap_detail view for showing full roadmap content
@login_required
def roadmap_detail(request, roadmap_id):
    roadmap = get_object_or_404(SavedAIRoadmap, id=roadmap_id, user=request.user)
    context = {
        'roadmap': roadmap
    }
    return render(request, 'dashboard/roadmap_detail.html', context)


#-----------------------------------------------------------------#
#---GROQ INTEGRATION FOR AI ADVISOR (ALTERNATIVE TO GEMINI)---

# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )

# @login_required
# def ask_groq_advisor(request):
#     # Ye hum testing ke liye hardcode kar rahe hain, baad mein form se lenge
#     user_prompt = "Give me a 3-step short roadmap to learn Cyber Security for web apps."
    
#     try:
#         # Groq ke server ko request bhej rahe hain
#         completion = client.chat.completions.create(
#             # Yahan Llama-3 ka 70 Billion parameter wala model use kar rahe hain
#             model="llama3-70b-8192", 
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are a highly skilled mentor. Provide technical advice in clean markdown format."
#                 },
#                 {
#                     "role": "user",
#                     "content": user_prompt
#                 }
#             ],
#             temperature=0.7, # Creativty level (0 se 1 ke beech)
#             max_tokens=1024, # Maximum lamba jawab kitna ho sakta hai
#         )
        
#         # Exact markdown text nikalna
#         ai_reply = completion.choices[0].message.content
        
#     except Exception as e:
#         ai_reply = f"System Error: {str(e)}"
        
#     context = {
#         'roadmap_content': ai_reply,
#         'title': 'Cyber Security Path (Powered by Groq)'
#     }
    
#     # Aap isko apne usi purane roadmap_detail.html (ya result.html) par bhej sakte ho
#     return render(request, 'dashboard/result.html', context)

