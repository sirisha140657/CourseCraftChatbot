from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
import google.generativeai as genai

app = Flask(__name__)
df = pd.read_csv("all_courses.csv")

def detect_platform(url):
    url = str(url).lower()
    if 'coursera.org' in url:
        return 'Coursera'
    elif 'edx.org' in url:
        return 'edX'
    elif 'udemy.com' in url:
        return 'Udemy'
    return 'Other'

df['platform'] = df['course_url'].apply(detect_platform)

def extract_duration_weeks(text):
    if pd.isna(text):
        return 10
    nums = re.findall(r'\d+\.?\d*', str(text))
    if not nums:
        return 10
    duration = float(nums[0])
    if "month" in str(text).lower():
        duration *= 4
    return int(duration)

df['duration_weeks'] = df['estimated_time_to_complete'].apply(extract_duration_weeks)

def recommend_courses(user):
    difficulty = user['difficulty'].lower()
    course_type = user['course_type'].lower()
    skills = [s.strip() for s in user['skills'].split(',') if s.strip()]
    max_duration = int(user['duration'])
    platform_choice = user['platform']
    platforms = [platform_choice] if platform_choice.lower() != "all" else ['Coursera', 'edX', 'Udemy']

    top_courses = []

    for plat in platforms:
        plat_df = df[df['platform'].str.lower() == plat.lower()]

        if plat.lower() == 'udemy':
            if skills:
                pattern = '|'.join([re.escape(skill) for skill in skills])
                plat_df = plat_df[
                    plat_df['course_name'].str.contains(pattern, case=False, na=False) |
                    plat_df['description'].str.contains(pattern, case=False, na=False) |
                    plat_df['skills'].str.contains(pattern, case=False, na=False)
                ]
        else:
            if difficulty == 'beginner':
                plat_df = plat_df[plat_df['course_difficulty'].str.lower() == 'beginner']
            elif difficulty == 'advanced':
                plat_df = plat_df[plat_df['course_difficulty'].str.lower().isin(['advanced', 'intermediate'])]

            if course_type:
                plat_df = plat_df[plat_df['learning_product_type'].str.lower() == course_type]

            plat_df = plat_df[plat_df['duration_weeks'] <= max_duration]

            if skills:
                pattern = '|'.join([re.escape(skill) for skill in skills])
                plat_df = plat_df[
                    plat_df['course_name'].str.contains(pattern, case=False, na=False) |
                    plat_df['description'].str.contains(pattern, case=False, na=False) |
                    plat_df['skills'].str.contains(pattern, case=False, na=False)
                ]

        plat_df = plat_df.sort_values(by="course_rating", ascending=False)
        top = plat_df.head(5)
        for _, row in top.iterrows():
            course_html = f"<a href='{row['course_url']}' target='_blank' style='color:#007bff;'>{row['course_name']}</a> ({plat})"
            top_courses.append(course_html)

    return "<br><br>".join(top_courses) if top_courses else "⚠️ No matching courses found."

# ------------------ Gemini Setup ------------------
genai.configure(api_key="AIzaSyC3n_JC_PcDIq7PIgh5Rzsw8KcTk-CwP4w")  # Add your Gemini API key here
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def clean_formatting(text):
    # Remove markdown-style asterisks
    text = re.sub(r'\*+', '', text)
    
    # Convert plain URLs into clickable HTML links
    text = re.sub(
        r'https?://\S+',
        lambda m: f"<a href='{m.group()}' target='_blank' style='color:#007bff;'>{m.group()}</a>",
        text
    )
    return text.strip()

def gemini_response(prompt, skills):
    try:
        if prompt.strip():
            full_prompt = prompt
        elif skills.strip():
            full_prompt = f"Suggest the best online courses to learn the following skills: {skills.strip()}.\nInclude course links if possible."
        else:
            return "🤖 Gemini skipped: No relevant input provided."

        response = model.generate_content(full_prompt)
        return clean_formatting(response.text)
    except Exception as e:
        return f"⚠️ Gemini Error: {e}"

# ------------------ Routes ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    user_input = request.get_json()
    model_response = recommend_courses(user_input)
    gemini_text = gemini_response(user_input.get("prompt", ""), user_input.get("skills", ""))
    return jsonify({
        "model_response": model_response,
        "gemini_response": gemini_text
    })

@app.route("/gemini", methods=["POST"])
def gemini_only():
    data = request.get_json()
    query = data.get("query", "")
    try:
        response = model.generate_content(query)
        return jsonify({"response": clean_formatting(response.text)})
    except Exception as e:
        return jsonify({"response": f"⚠️ Gemini Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
