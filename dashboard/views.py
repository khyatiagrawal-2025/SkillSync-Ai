import os
import requests
import markdown
from pathlib import Path
from dotenv import load_dotenv

from google import genai

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

# Aapke saare models import ho rahe hain
from .models import UserProgressProfile, UserSkill, Task, UserBadge, SavedAIRoadmap

# ==========================================
# ⚙️ ENVIRONMENT & API SETUP
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)

# Keys fetch karna
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")

# Gemini Client Initialize karna
if not GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY .env file mein nahi mili!")
    client = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)


# ==========================================
# 📊 1. MAIN DASHBOARD VIEW
# ==========================================
@login_required
@never_cache
def dashboard(request):
    student = request.user 
    total_students = User.objects.count()
    context = {
        'total_students': total_students,
        'student': student,
        'user': request.user
    }
    return render(request, "dashboard/dashboard.html", context)


# ==========================================
# 🗺️ 2. ROADMAP BASE VIEW
# ==========================================
def roadmap_view(request):
    return render(request, 'dashboard/roadmap.html')


# ==========================================
# ⚙️ 3. SETTINGS VIEW
# ==========================================
@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")


# ==========================================
# 🤖 4. AI SKILL ADVISOR (GITHUB + GOAL)
# ==========================================
@login_required
def skill_advisor(request):
    if request.method == "POST":
        github_username = request.POST.get('github_id', '').strip()
        user_interest = request.POST.get('interest', '').strip()

        try:
            # --- STEP A: Fetch GitHub Data (Safe Mode) ---
            repo_string = "No active repositories found or API limit reached."
            bio = "Not available"
            public_repos = 0
            
            if github_username:
                try:
                    user_url = f"https://api.github.com/users/{github_username}"
                    
                    # Agar Token hai, toh limits badhane ke liye headers bhejenge
                    headers = {}
                    if GITHUB_TOKEN:
                        headers['Authorization'] = f"token {GITHUB_TOKEN}"

                    # 5-second timeout taaki server hang na ho
                    user_response = requests.get(user_url, headers=headers, timeout=5) 
                    
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        repos_data = requests.get(f"{user_url}/repos?sort=updated&per_page=5", headers=headers, timeout=5).json()
                        
                        bio = user_data.get('bio', 'No bio provided')
                        public_repos = user_data.get('public_repos', 0)
                        
                        repo_details = []
                        for repo in repos_data:
                            if isinstance(repo, dict):
                                lang = repo.get('language') or 'Unknown'
                                repo_details.append(f"- {repo.get('name')} (Language: {lang})")
                        
                        if repo_details:
                            repo_string = "\n".join(repo_details)
                except requests.exceptions.RequestException as e:
                    print(f"⚠️ GitHub API Fetch Error (Ignored): {e}")

            # --- STEP B: Smart Prompt Construction ---
            prompt = f"""
            Act as an expert tech career mentor. 
            
            Developer's Current Profile (from GitHub):
            - Username: {github_username if github_username else 'Not Provided'}
            - Bio: {bio}
            - Total Public Repos: {public_repos}
            - Recent Projects & Main Languages: 
            {repo_string}
            
            THEIR FUTURE GOAL / TARGET ROLE: "{user_interest}"
            
            Based strictly on their existing skills (if GitHub data is available) and what they want to learn (their goal), provide a clear, step-by-step learning roadmap to bridge the gap.
            
            Structure your response:
            1. Analyze their current skill level.
            2. Explain how their past knowledge helps with their new goal.
            3. Provide a step-by-step roadmap to achieve the goal.
            4. MUST include a detailed Markdown Table summarizing the Timeline, Topics, and Resources.
            """

            # --- STEP C: Gemini API Call ---
            if not client:
                raise Exception("Gemini API key configure nahi hui hai. Kripya .env file check karein.")

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            ai_text = response.text

            # --- STEP D: Markdown to HTML Conversion ---
            html_content = markdown.markdown(ai_text, extensions=['tables', 'fenced_code'])

            # --- STEP E: Prepare Temporary Data Object for UI ---
            class TempData:
                user_skill = f"{github_username} ➔ {user_interest}" if github_username else user_interest
                recommendation = html_content
            
            query_obj = TempData()

            # --- STEP F: Save to Database ---
            title_text = f"{github_username} to {user_interest.capitalize()}" if github_username else f"{user_interest.capitalize()} Roadmap"
            
            SavedAIRoadmap.objects.create(
                user=request.user,
                title=title_text[:255], 
                ai_content=html_content
            )
            
            return render(request, 'dashboard/result.html', {'data': query_obj})

        except Exception as e:
            print(f"🔴 CRITICAL ERROR IN SKILL ADVISOR: {e}") 
            # Fallback error response for the UI
            class TempError:
                user_skill = "Error Occurred"
                recommendation = f"<h3>Oops! Kuch technical issue aa gaya:</h3><p>{str(e)}</p><p>Please try again in a few moments.</p>"
            return render(request, 'dashboard/result.html', {'data': TempError()})

    return render(request, 'dashboard/roadmap.html')


# ==========================================
# 📈 5. PROGRESS DASHBOARD VIEW
# ==========================================
@login_required
def progress_dashboard(request):
    user = request.user
    profile, created = UserProgressProfile.objects.get_or_create(user=user)
    skills = UserSkill.objects.filter(user=user).order_by('-proficiency')
    recent_tasks = Task.objects.filter(user=user).order_by('-created_at')[:10]
    earned_badges = UserBadge.objects.filter(user=user).select_related('badge')
    saved_roadmaps = SavedAIRoadmap.objects.filter(user=user).order_by('-generated_at')
    
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
        'level_progress_pct': min(level_progress_pct, 100),
    }
    return render(request, 'dashboard/progress.html', context)


# ==========================================
# 📄 6. SAVED ROADMAP DETAIL VIEW
# ==========================================
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

