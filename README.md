
---

### 2) `cs50w-network`
```bash
cd ~/cs50w-network

cat > README.md <<'EOF'
# CS50W Project 4 — Network

A mini social network where users post updates, follow others, and like posts. Includes pagination, inline editing, and separate feeds for “All Posts” and “Following”.

## Features
- Register/Login/Logout (Django auth)
- Create & edit posts (inline edit with AJAX)
- Pagination on the main feed
- Profile pages with user’s posts
- Follow/Unfollow users
- “Following” feed shows only authors you follow
- Like/Unlike with real-time count updates
- Clean, responsive layout

## Tech Stack
- Django (views, models, auth)
- Vanilla JavaScript (Fetch API for async actions)
- HTML/CSS

## Quickstart
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt || pip install "Django>=4,<6"
python manage.py migrate
python manage.py createsuperuser  # create an admin for testing
python manage.py runserver
