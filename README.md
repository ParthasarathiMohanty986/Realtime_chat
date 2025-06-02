# 💬 Real-Time Chat App with Django, HTMX & WebSockets

A full-stack real-time chat application built using **Django**, **Django Channels**, **HTMX**, and **WebSockets**. It provides a seamless and interactive chat experience with support for **public chats**, **private messaging**, **custom group chats**, **file sharing**, and **live online presence tracking** — all without page reloads.


## 🚀 Features

- 🗣️ **Public Chat Room** – A global room where all logged-in users can chat together
- 🔐 **Private Messaging** – One-to-one direct messages between users
- 👥 **Custom Group Chats** – Users can create groups and invite friends
- 🟢 **Online User Tracking** – See who is online in real-time
- 📁 **File Sharing** – Upload and exchange files in any chat
- 🧠 **Live Typing Indicators** – Know when someone is typing
- ⚡ **Real-Time Messaging** – Achieved using Django Channels & WebSockets
- 👤 **User Authentication** – Login, logout, and access control for chat features

---

## 🛠️ Tech Stack

### Backend
- **Django** – Backend web framework for models, authentication, and views
- **Django Channels** – WebSocket support and asynchronous consumers
- **ASGI** – Enables asynchronous communication between client and server
- **WebSockets** – Real-time bidirectional communication protocol

### Frontend
- **HTMX** – Enhances interactivity with server-rendered components
- **HTML5, CSS3** – Layout and styling
- **JavaScript** – Minimal use for file upload and enhanced UX



#### Getting the files
Download zip file<br> 
or <br>
git clone command (need git to be installed) and remove git folder afterwards
```
git clone https://github.com/andyjud/django-starter.git . && rm -rf .git
```
<br><br><br>

## Setup

#### - Create Virtual Environment
###### # Mac
```
python3 -m venv venv
source venv/bin/activate
```

###### # Windows
```
python3 -m venv venv
.\venv\Scripts\activate.bat
```

<br>

#### - Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

<br>

#### - Migrate to database
```
python manage.py migrate
python manage.py createsuperuser
```

<br>

#### - Run application
```
python manage.py runserver
```

<br>

#### - Generate Secret Key ( ! Important for deployment ! )
```
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
exit()
