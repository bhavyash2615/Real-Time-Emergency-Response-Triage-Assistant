let patientList = [];

window.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("https://real-time-emergency-response-triage.onrender.com/patients");
    patientList = await res.json();
    console.log("Loaded patients:", patientList.length);
  } catch (err) {
    console.error("Error loading patients", err);
  }
});

function runTriage() {
  
  const patientId = document.getElementById("patientId").value;
  const symptoms = document.getElementById("symptoms").value;

  if (!patientId || !symptoms) {
    alert("Please enter both Patient ID and symptoms");
    return;
  }

  // Switch UI immediately
  document.getElementById("inputScreen").style.display = "none";
  document.getElementById("resultScreen").style.display = "block";

  // Show loading temporarily
  document.getElementById("res-condition").innerText = "Loading...";

  fetch("https://real-time-emergency-response-triage.onrender.com/triage", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      patient_id: patientId,
      current_issue: symptoms
    })
  })
  .then(res => res.json())
  .then(data => {
    console.log("BACKEND RESPONSE:", data);
    renderResult(data, patientId, symptoms);
  })
  .catch(err => {
    console.error(err);
    alert("Error connecting to backend");
  });
}


function renderResult(data, patientId) {

  // Patient basic info (only ID available)
  document.getElementById("res-id").innerText = patientId;
  

  // Condition
  document.getElementById("res-condition").innerText = data.possible_condition || "N/A";

  // -------------------------
  // Urgency mapping (IMPORTANT)
  // -------------------------
  const urgencyEl = document.getElementById("res-urgency");
  let level = data.triage_level || "Unknown";

  urgencyEl.innerText = level;
  urgencyEl.className = "triage-badge";

  if (level.includes("Immediate")) {
    urgencyEl.classList.add("triage-red");
  } 
  else if (level.includes("Very High Risk")) {
    urgencyEl.classList.add("triage-orange");
  } 
  else if (level.includes("Urgent")) {
    urgencyEl.classList.add("triage-yellow");
  } 
  else {
    urgencyEl.classList.add("triage-green");
  }

  // -------------------------
  // Latency
  // -------------------------
  document.getElementById("res-latency").innerText =
  data.latency_ms ? data.latency_ms + " ms" : "N/A";


  // -------------------------
  // Actions
  // -------------------------
  const actionsBox = document.getElementById("actionsBox");
  const actionsList = document.getElementById("res-actions");
  actionsList.innerHTML = "";

  if (data.actions && data.actions.length > 0) {
    data.actions.forEach(a => {
      const li = document.createElement("li");
      li.innerText = a;
      actionsList.appendChild(li);
    });
    actionsBox.style.display = "block";
  } else {
    actionsBox.style.display = "none";
  }

  // -------------------------
  // Next Steps
  // -------------------------
  const stepsBox = document.getElementById("stepsBox");
  const stepsList = document.getElementById("res-steps");
  stepsList.innerHTML = "";

  if (data.next_steps && data.next_steps.length > 0) {
    data.next_steps.forEach(s => {
      const li = document.createElement("li");
      li.innerText = s;
      stepsList.appendChild(li);
    });
    stepsBox.style.display = "block";
  } else {
    stepsBox.style.display = "none";
  }

  // -------------------------
  // Patient History (Diagnoses + Medications)
  // -------------------------
  let historyText = "";

  if (data.patient_context_used) {
    const diagnoses = data.patient_context_used.diagnoses || [];
    const meds = data.patient_context_used.medications || [];

    if (diagnoses.length > 0) {
      historyText += "Diagnoses:\n- " + diagnoses.join("\n- ") + "\n\n";
    }

    if (meds.length > 0) {
      historyText += "Medications:\n- " + meds.join("\n- ");
    }
  }

  document.getElementById("res-history").innerText = historyText;

  // -------------------------
  // LLM Recommendation
  // -------------------------
  document.getElementById("res-llm").innerText =
    data.llm_recommendation || "No recommendation available";

  // -------------------------
  // Performance Box
  // -------------------------
  const perfBox = document.getElementById("performanceBox");
  const perfText = document.getElementById("res-performance");

  if (data.step_times) {
    let text = "";
    for (let key in data.step_times) {
      text += key + ": " + data.step_times[key] + " ms\n";
    }
    perfText.innerText = text;
    perfBox.style.display = "block";
  } else {
    perfBox.style.display = "none";
  }

  // -------------------------
  // Hide Empty history
  // -------------------------
  const historyBox = document.getElementById("historyBox");
  if (historyText) {
    historyBox.style.display = "block";
  } else {
    historyBox.style.display = "none";
  }

  
}



document.querySelectorAll(".faq-question").forEach(btn => {
  btn.addEventListener("click", () => {
    const answer = btn.nextElementSibling;

    if (answer.style.maxHeight) {
      answer.style.maxHeight = null;
    } else {
      answer.style.maxHeight = answer.scrollHeight + "px";
    }
  });
});

document.querySelectorAll(".prompt-chip").forEach(chip => {
  chip.addEventListener("click", () => {
    const text = chip.innerText;

    const id = text.match(/\d+/)[0];
    const symptom = text.split("—")[1].trim();

    document.getElementById("patientId").value = id;
    document.getElementById("symptoms").value = symptom;

    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});


// -------------------------
// AUTOCOMPLETE LOGIC
// -------------------------
const input = document.getElementById("patientId");
const dropdown = document.getElementById("patientDropdown");

input.addEventListener("input", () => {
  const value = input.value.toLowerCase();
  dropdown.innerHTML = "";

  if (!value) {
    dropdown.style.display = "none";
    return;
  }

  const filtered = patientList.filter(id =>
    id.toString().includes(value)
  );

  filtered.slice(0, 10).forEach(id => {
    const div = document.createElement("div");
    div.innerText = id;

    div.onclick = () => {
      input.value = id;
      dropdown.style.display = "none";
    };

    dropdown.appendChild(div);
  });

  dropdown.style.display = filtered.length ? "block" : "none";
});

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
  if (!e.target.closest(".autocomplete")) {
    dropdown.style.display = "none";
  }
});

function goBack() {

  // Switch screens
  document.getElementById("resultScreen").style.display = "none";
  document.getElementById("inputScreen").style.display = "block";

  // Clear inputs
  document.getElementById("patientId").value = "";
  document.getElementById("symptoms").value = "";

  // Clear result fields (important)
  document.getElementById("res-condition").innerText = "";
  document.getElementById("res-actions").innerHTML = "";
  document.getElementById("res-steps").innerHTML = "";
  document.getElementById("res-history").innerText = "";
  document.getElementById("res-llm").innerText = "";
  document.getElementById("res-performance").innerText = "";
}

function startVoice() {
  const micBtn = document.getElementById("micBtn");
  const textarea = document.getElementById("symptoms");

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Voice not supported in this browser");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-IN";
  recognition.interimResults = false;

  micBtn.classList.add("listening");

  recognition.start();

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    textarea.value += " " + transcript;
  };

  recognition.onend = function() {
    micBtn.classList.remove("listening");
  };

  recognition.onerror = function() {
    micBtn.classList.remove("listening");
  };
}