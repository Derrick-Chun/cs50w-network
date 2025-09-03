# CS50W Project 4 — Network

A mini social network built with Django (backend) and vanilla JavaScript (frontend). Users can create posts, follow other users, like posts, and edit their own posts inline. Pagination and a dedicated “Following” feed keep the UI fast and focused.

## Features

- **Auth:** Register / Login / Logout (Django auth)
- **Create Posts:** Compose and submit text posts with validation
- **Inline Edit:** Authors can edit their own posts via AJAX, no page reload
- **Likes:** Like/Unlike with immediate count updates
- **Profiles:** User pages show their posts and follow/unfollow controls
- **Following Feed:** Timeline of posts only from people you follow
- **Pagination:** Efficient navigation through large feeds
- **Responsive UI:** Clean layout on mobile and desktop
- **Graceful Errors:** Simple inline messages on fetch/API failures

## Tech Stack

- **Frontend:** HTML/CSS, Vanilla JS (Fetch API)
- **Backend:** Django (views, models, auth)
- **Data:** Relational models for Post, Follow, Like

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt || pip install "Django>=4,<6"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
