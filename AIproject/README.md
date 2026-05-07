# AI-Powered Voice Banking Assistant

**Student:** Elnur Suinov | **ID:** 2426692 | **Module:** 6CS007  
**University:** University of Wolverhampton | **Campus:** Tashkent IDU

---

## Project Overview

An AI-powered voice banking assistant that processes natural spoken commands to perform banking operations. The system integrates:

- 🎤 **OpenAI Whisper Small** — Speech-to-Text recognition
- 🧠 **spaCy en_core_web_sm** — NLP processing and entity extraction
- 📊 **TF-IDF + Logistic Regression** — Intent classification (12 categories)
- 🤖 **Phi-3 via Ollama** — Large language model for advisory responses
- 🏦 **Django 6.0** — Web framework with PostgreSQL database
- 🔐 **2FA + Fraud Detection** — Multi-layer security architecture
- ⚡ **Celery + Redis** — Asynchronous task processing

---

## Prerequisites

Before running the project, ensure the following are installed on your machine:

| Requirement | Version | Download |
|-------------|---------|----------|
| Docker Desktop | Latest | https://www.docker.com/products/docker-desktop |
| Docker Compose | Included with Docker Desktop | — |
| Ollama | Latest | https://ollama.com/download |
| Git | Any | https://git-scm.com |

> **Note:** Minimum 8GB RAM recommended. The Whisper Small model requires ~461MB disk space and Phi-3 requires ~2.3GB.

---

## Step-by-Step Setup

### Step 1 — Install and Start Ollama

Ollama must be running on your **host machine** (not inside Docker).

**Windows / macOS:**
```bash
# Download and install from https://ollama.com/download
# Then open a terminal and run:
ollama serve
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

Verify Ollama is running by opening: http://localhost:11434

---

### Step 2 — Download the Phi-3 Model

In a new terminal window:

```bash
ollama pull phi3
```

> This downloads approximately 2.3GB. Wait for it to complete before proceeding.

---

### Step 3 — Clone or Extract the Project

**If using Git:**
```bash
git clone <repository-url>
cd AIproject
```

**If using ZIP:**
```bash
# Extract the ZIP file
# Navigate to the AIproject folder
cd AIproject
```

---

### Step 4 — Start the Application

```bash
docker-compose up --build
```

This command will:
1. Build the Django and Celery containers
2. Start PostgreSQL database
3. Start Redis message broker
4. Apply database migrations automatically
5. Download Whisper Small model on first request (~461MB, one-time)

> **First build takes 3–5 minutes.** Subsequent starts are much faster.

---

### Step 5 — Create a Superuser (Admin Account)

Open a **new terminal** while containers are running:

```bash
docker exec -it ai_django python manage.py createsuperuser
```

Enter your preferred username, email, and password when prompted.

---

### Step 6 — Load Initial Data

```bash
docker exec -it ai_django python manage.py loaddata initial_data.json
```

This populates the database with:
- Test bank account with balance £13,800
- Sample loan, deposit, and card products
- Sample risk rules for fraud detection

---

### Step 7 — Access the Application

| Service | URL |
|---------|-----|
| **Voice Banking Assistant** | http://localhost:8000 |
| **Django Admin Panel** | http://localhost:8000/admin |

Log in with the superuser credentials you created in Step 5.

---

## Using the Voice Assistant

1. Open http://localhost:8000 in **Google Chrome** or **Firefox**
2. Log in with your credentials
3. Click and **hold** the microphone button 🎤
4. Speak your banking command clearly
5. Release the button to process
6. The AI response will appear on screen and play via text-to-speech

### Example Voice Commands

| Command | Expected Response |
|---------|------------------|
| *"What is my balance?"* | Returns current account balance |
| *"Send 100 pounds"* | Executes transfer (small amount) |
| *"Send 6000 pounds"* | Triggers 2FA verification |
| *"Show recent transactions"* | Lists last 5 transactions |
| *"I need a loan"* | Phi-3 advisory with real rates |
| *"Hello"* | Personalised greeting |

### Two-Factor Authentication (2FA)

For transfers above £5,000, the system requires OTP verification:

1. Speak the transfer command (e.g. *"Send 6000 pounds"*)
2. Check the **Django admin logs** or **Celery terminal** for the OTP code
3. Speak the 6-digit code (e.g. *"My code is 971145"*)
4. Transfer completes automatically

> In development mode, OTP codes are printed to the Celery worker logs. Check the terminal running `docker-compose up`.

---

## Stopping the Application

```bash
# Stop all containers
docker-compose down

# Stop and remove all data (full reset)
docker-compose down -v
```

---

## Troubleshooting

### "Ollama connection refused" error
- Ensure Ollama is running on your host machine: `ollama serve`
- Verify it is accessible at: http://localhost:11434

### Whisper model takes too long on first request
- The Whisper Small model (461MB) downloads on the first voice request
- Subsequent requests use the cached model and are much faster (3–5 seconds)

### Docker containers not starting
```bash
# Check container logs
docker-compose logs ai_django
docker-compose logs ai_celery

# Restart all containers
docker-compose down
docker-compose up --build
```

### Microphone not working in browser
- Ensure the browser has microphone permission
- Chrome: Settings → Privacy → Microphone → Allow localhost
- Firefox: Click the lock icon in address bar → Allow microphone

### Port 8000 already in use
```bash
# Find and kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill
```

---

## Project Structure

```
AIproject/
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Django + Celery container
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management
├── config/
│   └── settings.py             # Django settings
├── apps/
│   ├── accounts/               # User authentication
│   ├── banking/                # Banking service layer
│   │   ├── models.py           # BankAccount, Transaction, AuditLog
│   │   ├── services/           # BalanceService, TransferService
│   │   └── domain/             # TransactionLifecycle, RiskEngine
│   ├── ai_pipeline/            # AI processing
│   │   ├── speech_to_text.py   # Whisper STT
│   │   ├── nlp_processor.py    # spaCy NLP
│   │   ├── intent_service.py   # TF-IDF + LogReg classifier
│   │   ├── dialogue_manager.py # Intent routing
│   │   └── llm_service.py      # Phi-3 via Ollama
│   └── frontend/               # HTML templates + JS
├── static/
│   ├── css/                    # Styling
│   └── js/recorder.js          # MediaRecorder + TTS
└── fixtures/
    └── initial_data.json       # Sample data
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | Django | 6.0.1 |
| Database | PostgreSQL | 16 |
| Cache / Broker | Redis | 7.4 |
| Task Queue | Celery | 5.6.2 |
| Speech Recognition | OpenAI Whisper | Small (244M params) |
| NLP | spaCy | 3.8 + en_core_web_sm |
| Intent Classifier | scikit-learn | TF-IDF + LogReg |
| LLM | Phi-3 | via Ollama |
| Containerisation | Docker + Compose | Latest |

---

## Testing the Security Features

The following security scenarios can be verified manually:

```
ST-01: Login → transfer £6000 → enter correct OTP → transfer completes
ST-02: Login → transfer £6000 → enter wrong OTP → "Invalid OTP" message
ST-03: Enter wrong OTP 3 times → "Maximum attempts exceeded"
ST-04: Wait 5 minutes after OTP issued → "OTP expired"
ST-05: Submit same transfer twice → second request ignored (idempotency)
ST-06: Access /api/voice/ without login → redirect to login page
ST-07: Attempt transfer > £20,000 → blocked by SecurityEngine
ST-08: First login from new device → risk score elevated (visible in admin)
```

---

## Marking Examiner Notes

- The system requires **Ollama running on the host machine** before starting Docker
- On first voice request, Whisper Small downloads automatically (~461MB) — this is expected
- OTP codes in development mode appear in **Celery worker terminal output**
- All transactions, risk scores, and audit logs are visible in the **Django admin** at `/admin`
- The intent classifier model files (`intent_model.pkl`, `vectorizer.pkl`) are pre-trained and included

---

*Submitted as part of 6CS007 Project Management and Professionalism — BSc (Hons) Artificial Intelligence*
