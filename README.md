# Cognitive Orchestrator

A unified, self-hosted AI personal assistant built with **Django**, **Tailwind CSS**, and **SQLite**.

## 🚀 One-Command Start

Everything runs through Django. You no longer need `npm` or `node`.

1. **Install Dependencies**:
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

2. **Run Server**:
   ```bash
   cd backend
   python manage.py runserver
   ```

3. **Access App**:
   Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🛠 Tech Stack

- **Backend**: Django & Django REST Framework
- **Frontend**: Django Templates + Tailwind CSS + Alpine.js
- **Database**: SQLite (Local only)
- **AI**: Google Gemini (Customizable in Settings)

## 📁 Project Structure

- `backend/`: The complete application.
  - `api/templates/`: HTML templates for all pages.
  - `api/models.py`: Database schema for Users, Chats, Memories, and Reminders.
  - `api/views.py`: Logic for both HTML rendering and REST API.
  - `db.sqlite3`: Your local personal database.

---

## 📝 Features

- **Dashboard**: Bento-style grid with AI chat and process streams.
- **Memory Vault**: Neural database for notes, articles, and snippets.
- **Reminders**: Task management with tags and due dates.
- **Settings**: Local encryption and AI provider configuration.
- **Dark Mode**: Optimized for high-focus AI orchestration.
