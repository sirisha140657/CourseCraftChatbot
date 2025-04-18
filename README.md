
 ##🤖 AI-Powered Course Recommender Chatbot

Welcome to the **AI Course Recommender Chatbot**! 🎓✨  
This intelligent assistant helps students discover the best online courses across platforms like **Coursera**, **Udemy**, and **edX** — personalized to their skills, interests, and learning goals. 🚀



##🧠 Key Features

- 💬 *Chatbot Interface* – Conversational UI for smooth user experience.
- 🎯 *Personalized Recommendations* – Based on user skills, preferred difficulty, course type, duration, and platform.
- 🛠️ *Hybrid Recommendation Engine* – Combines rule-based filtering 🔍 and content-based techniques 🧩.
- 🌐 *Multi-Platform Support* – Courses aggregated from:
  - Coursera 📘  
  - Udemy 📕  
  - edX 📗
- 🤝 *Gemini API Integration* – Generates additional smart suggestions using Google’s Gemini AI 🤖.
- 📊 *Clean & Ranked Output* – Courses are ranked, formatted with clickable links, and presented clearly.

---
COURSE_RECOMMENDER/             
├── static/                    # 🌐 Static files (JS, CSS, icons)
│   ├── favicon.ico            # ⭐ Browser icon
│   ├── script.js              # ⚙️ JavaScript for frontend interaction
│   └── style.css              # 🎨 Custom styling (optional)
├── templates/
│   └── index.html             # 🖥️ Frontend chatbot interface
├── all_courses.csv            # 📊 Course dataset from Coursera, Udemy, edX
├── skilllist.txt              # 🧾 List of skills for filtering
├── app.py                     # 🚀 Flask backend with chatbot & recommendation logic
├── requirements.txt           # 📦 Required Python packages
└── README.md                  # 📄 You are here!
```

---

## 🧪 How It Works

1. **User enters preferences** via chatbot (skills, difficulty, course type, duration, platform).
2. The backend **filters and ranks** relevant courses using:
   - Rule-based logic for matching criteria.
   - Content-based filtering to check skill relevance.
3. **Gemini AI** suggests extra personalized courses based on skills.
4. Results are **combined, formatted**, and shown with clickable links 🔗.

---

## 🧰 Tech Stack

- **Python** 🐍 (Flask for backend)
- **HTML + JavaScript** 🌐 (chatbot frontend)
- **Pandas** 📊 (for dataset filtering)
- **Gemini API** 🤖 (for AI course suggestions)
- **CSV Dataset** 📂 (containing real courses from top platforms)

---

## 🚀 Getting Started

1. Clone the repo  
   ```bash
   git clone https://github.com/yourusername/ai-course-chatbot.git
   cd ai-course-chatbot
   ```

2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

3. 🔐 **Set your Gemini API key**

   Create a file named `.env` in the root folder and add your Gemini API key:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

   Or set it in your environment variables before running:

   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

4. Run the Flask app  
   ```bash
   python app.py
   ```

5. Open your browser and chat away 🗨️ at `http://localhost:5000`

---

## 📌 Example Prompts

> *"I want beginner-friendly Python courses from Coursera."*  
> *"Show me short, project-based web development courses."*  
> *"Give me AI-related courses I can finish in under 4 weeks."*

---

