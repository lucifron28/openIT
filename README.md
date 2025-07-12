# AQUEST

## API Endpoints

## TechStack
- Frontend: Sveltekit/Vite
- Backend: Django + Django Rest Framework
- Database: PostgreSQL

### Authentication
This system uses JWT Auth
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout
- `POST /api/users/token/refresh/` - Refresh JWT token


### Projects
- `GET /api/projects/projects/` - List user's projects
- `POST /api/projects/projects/` - Create new project
- `GET /api/projects/projects/{id}/` - Get project details
- `PUT /api/projects/projects/{id}/` - Update project
- `DELETE /api/projects/projects/{id}/` - Delete project
- `GET /api/projects/projects/{id}/tasks/` - Get project tasks
- `POST /api/projects/projects/{id}/create_task/` - Create task in project
- `GET /api/projects/projects/{id}/stats/` - Get project statistics
- `POST /api/projects/projects/{id}/assign_member/` - Assign user to project

### Tasks
- `GET /api/projects/tasks/` - List all accessible tasks
- `POST /api/projects/tasks/` - Create new task
- `GET /api/projects/tasks/{id}/` - Get task details
- `PUT /api/projects/tasks/{id}/` - Update task
- `DELETE /api/projects/tasks/{id}/` - Delete task
- `POST /api/projects/tasks/{id}/complete/` - Mark task as completed
- `POST /api/projects/tasks/{id}/assign/` - Assign task to user
- `GET /api/projects/tasks/my_tasks/` - Get tasks assigned to current user
- `GET /api/projects/tasks/created_by_me/` - Get tasks created by current user


### Setup Guide

- Clone the repository
`git clone https://github.com/lucifron28/openIT/`

- Build using Docker
`docker compose build`

- Run the Container
`Docker compose up`

- Access the database
`docker compose exec db psql -U postgres -d backend`


## URLs
- Frontend - http://localhost:5173/
- Backend - http://localhost:8000/api/users/login/


# Features

## AI Coach
- Powered by Gemini
- AI Chatbot that assists user and gives tips about project management

## Create and Manage Projects
- Allows users to create and manage projects and assign a team


## Create and Manage Tasks
- Allows users to create and manage tasks inside a project
- gives user points upon finishing

## Achievements (Not Fully Implemented)
- Gives users target achievements and awards to motivate them to achieve their goals
