let currentQuestion = 0;
let userData = {
  difficulty: "",
  course_type: "",
  skills: "",
  duration: "",
  platform: "",
  prompt: ""
};

const questions = [
  "What is your preferred difficulty level? (Beginner, Intermediate, Advanced)",
  "What type of course are you looking for? (Specialization, Certificate Course, etc.)",
  "What skills do you want to learn? (comma-separated)",
  "What is the maximum duration in weeks?",
  "Preferred platform? (Coursera, edX, Udemy or All)"
];

const keys = ["difficulty", "course_type", "skills", "duration", "platform"];

function appendMessage(message, type) {
  const chatbox = document.getElementById("chatbox");
  const bubble = document.createElement("div");
  bubble.classList.add("chat-bubble", type === "user" ? "user-bubble" : "bot-bubble");
  bubble.innerHTML = message;
  chatbox.appendChild(bubble);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function showTypingIndicator() {
  const chatbox = document.getElementById("chatbox");
  const typing = document.createElement("div");
  typing.classList.add("chat-bubble", "bot-bubble");
  typing.id = "typing";
  typing.innerHTML = `Typing<span class="typing-indicator"><span></span><span></span><span></span></span>`;
  chatbox.appendChild(typing);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function removeTypingIndicator() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

function resetChat() {
  document.getElementById("chatbox").innerHTML = "";
  document.getElementById("user-input").value = "";
  currentQuestion = 0;
  userData = {
    difficulty: "",
    course_type: "",
    skills: "",
    duration: "",
    platform: "",
    prompt: ""
  };
  appendMessage("🔄 Starting over... Hi there! I’m your AI Course Assistant 👋", "bot");
  setTimeout(() => {
    appendMessage(questions[0], "bot");
  }, 800);
}

function nextQuestion() {
  const input = document.getElementById("user-input").value.trim();
  if (input === "" && currentQuestion < questions.length) return;

  if (currentQuestion < questions.length) {
    appendMessage(input, "user");
    userData[keys[currentQuestion]] = input;
    currentQuestion++;
    document.getElementById("user-input").value = "";

    if (currentQuestion < questions.length) {
      showTypingIndicator();
      setTimeout(() => {
        removeTypingIndicator();
        appendMessage(questions[currentQuestion], "bot");
      }, 800);
    } else {
      showTypingIndicator();
      setTimeout(() => {
        removeTypingIndicator();
        appendMessage("💬 You can enter a custom query or leave blank.", "bot");
      }, 600);
    }
  } else if (currentQuestion === questions.length) {
    appendMessage(input || "(blank)", "user");
    userData["prompt"] = input;
    document.getElementById("user-input").value = "";
    currentQuestion++;
    submitData();
  } else {
    if (input === "") return;
    appendMessage(input, "user");
    document.getElementById("user-input").value = "";
    showTypingIndicator();
    fetch("/gemini", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input })
    })
    .then(res => res.json())
    .then(data => {
      removeTypingIndicator();
      appendMessage("<strong>Gemini:</strong><br>" + data.response, "bot");
    });
  }
}

function submitData() {
  showTypingIndicator();
  fetch("/result", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  })
  .then(response => response.json())
  .then(data => {
    removeTypingIndicator();
    appendMessage(
      "<strong>Top Reccommendations:</strong><br>" + data.gemini_response +
      "<br><br><strong>Other Recommendations:</strong><br>" + data.model_response,
      "bot"
    );
    
    setTimeout(() => {
      appendMessage("🤖 You can now ask any question, or click 'Start Over' to begin again.", "bot");
    }, 500);
  })
  .catch(err => {
    console.error("❌ Error submitting data:", err);
    removeTypingIndicator();
    appendMessage("⚠️ Something went wrong while fetching recommendations. Please try again.", "bot");
  });
}

window.onload = () => {
  appendMessage("Hi there! I’m your AI Course Assistant 👋", "bot");
  setTimeout(() => {
    appendMessage(questions[0], "bot");
  }, 1000);
};

document.getElementById("send-btn").addEventListener("click", nextQuestion);
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    nextQuestion();
  }
});
document.getElementById("start-over-btn").addEventListener("click", resetChat);
