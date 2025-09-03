# SiteLink — Connect Students, Firms, and Clients in Architecture & Civil

SiteLink is a Django-based platform that bridges the gap between **students**, **architecture/civil firms**, and **clients** during the construction and internship lifecycle. It streamlines how internships are posted and applied for, how firms manage applicants, and how clients submit and track house projects—all in one unified system with role-based dashboards.

---

## 🌟 Why SiteLink?

Architecture and civil engineering students often struggle to find relevant, hands-on opportunities. Firms need a lighter way to source interns and respond to client project inquiries. Clients want a simple channel to describe their house projects and receive responses from firms.

**SiteLink** solves all three problems:
- Students discover and apply to internships with a clear, trackable process.
- Firms post openings, review applicants, and manage client-submitted projects.
- Clients submit house project details and receive approvals/notes from firms.

---

## 👥 User Roles & Capabilities

### 1) Students
- Browse **active internships** with filters (location, mode, etc.)
- View detailed internship pages (company, responsibilities, requirements, stipend, duration, deadline, perks, mode)
- Apply via an application form (name, email, phone, college, CGPA/year of passing, achievements, profile/resume upload)
- Track **application history**: when you applied and to which company
- See **notifications/success messages** after key actions

### 2) Firms
- Create and manage **internship postings**
- Review and filter **applicants** by various criteria
- See **client-submitted house projects** in a dedicated section
- **Approve** a client project and attach a **custom message** (e.g., “We’re ready to take this on—please contact us by mail or phone”)
- See success messages after updates/approvals

### 3) Clients
- Browse available firms (directory/list view)
- Submit **house project details** (requirements, scope, contact info)
- View **firm responses/approvals** and messages right on the client dashboard
- Receive success notifications after submission

### 4) Admin
- Full control via Django Admin (users, postings, applications, projects, etc.)

---

## 🧭 Key Flows

**Internship Flow**
1. Firm posts an internship.
2. Student browses and applies.
3. Firm reviews applicants, filters, and shortlists.
4. System shows student their application status/history.

**Client Project Flow**
1. Client submits a house project.
2. Firms see the new project in their dashboard.
3. A firm approves it and attaches a message.
4. Client sees that response from the firm in their dashboard.

---

## 🖥️ UX Highlights

- **Role-based dashboards** for Students, Firms, and Clients.
- Clean, simple **Auth** (Register/Login/Logout).
- Homepage with a single **Register** button in the header; **login buttons** under each role section navigate straight to login.
- **Success/Toast messages** after core actions (applied, posted, approved, saved).
- Professional, lightweight styling (HTML/CSS/Bootstrap) aligned with the SiteLink theme.

---

## 🏗️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default); can be swapped for PostgreSQL/MySQL
- **Auth:** Django’s built-in authentication with role mapping
- **Storage:** Local filesystem for development (for resume/profile uploads)

---

## 📁 Project Structure 
SiteLink1/
├─ SiteLink/ # Django project root
│ ├─ core/ # Main app (auth, dashboards, internships, projects)
│ ├─ templates/ # HTML templates
│ ├─ static/ # Static files (CSS, JS, images)
│ ├─ media/ # User uploads (e.g., resumes) - dev only
│ ├─ settings.py
│ ├─ urls.py
│ └─ manage.py
└─ requirements.txt

## 🗄️ Data Model (high level)

- **UserProfile** (extending/auth-linking Django User)
  - role: `student` | `firm` | `client`
  - profile fields (as needed)

- **Internship**
  - company_name, title, description, location
  - responsibilities, requirements, stipend, duration, deadline, perks, mode
  - firm (ForeignKey to User/Firm), created_at, is_active

- **InternshipApplication**
  - internship (FK), student (FK)
  - first_name, last_name, email, phone_number
  - college_name, year_of_passing, cgpa
  - achievements (text), resume/profile_file (upload)
  - applied_at, status (optional)

- **HouseProject**
  - client (FK), title/summary, description, location, budget (optional)
  - status (e.g., submitted/approved)
  - approval_message / firm_response (text)
  - approved_by (FK to Firm), created_at, updated_at

*(Field names may vary depending on your codebase; this is a conceptual map.)*

---

## ⚙️ Configuration

Create a `.env` (or set environment variables) with at least:
- `SECRET_KEY` — Django secret key
- `DEBUG` — `True` for development
- `ALLOWED_HOSTS` — e.g., `127.0.0.1,localhost`
- **Email settings** (optional) if you plan to send emails
- **Database URL** (if not using SQLite)

In development, static and media settings typically serve from local paths.

---

## 🚀 Quick Start (Dev)
**Virtual environment & dependencies**
   ```bash
   python -m venv venv

   # Windows:venv\Scripts\activate

   pip install django

   python manage.py makemigrations

   python manage.py migrate

  python manage.py createsuperuser

   python manage.py runserver


   






