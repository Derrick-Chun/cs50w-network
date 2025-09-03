
---

# 🌐 Network (Project 4)

```markdown
# CS50W Project 4 — Network

A mini social network: users post updates, follow others, like posts, and edit their own posts inline. The app supports pagination and a dedicated “Following” feed.

## Features
- **Auth**: Register / Login / Logout (Django auth)
- **Create Posts**: Text posts with validation
- **Inline Edit**: Authors can edit their own posts via AJAX
- **Likes**: Like/Unlike with live count updates
- **Profiles**: User pages with their posts + follow/unfollow
- **Following Feed**: Shows posts only from people you follow
- **Pagination**: Efficient scrolling through large feeds
- **Responsive UI**: Clean layout on mobile and desktop

## Tech Stack
- **Backend**: Django (views, models, auth)
- **Frontend**: Vanilla JS (Fetch), HTML/CSS
- **Data**: Relational models for Post, Follow, Like

## Run Locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt || pip install "Django>=4,<6"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
