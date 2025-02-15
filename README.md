# DPMS backend

## Prerequisites

- Docker
- Docker Compose

## Local Development Setup

### 1. Create .env from .env.example file and update the environment variables accordingly
```bash
cp .env.example .env
```

### 2. Start the Development Server

```bash
docker compose up
```

### 3. Initialize the Database

Open a new terminal and run the following commands:

```bash
# Enter the web container
docker compose exec web bash

# Run database migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Load initial data
python manage.py loaddata users
```

## Development Workflow

- The application will be available at `http://localhost:8000`
- Admin interface can be accessed at `http://localhost:8000/admin`

## Additional Setup Notes

- Ensure Docker and Docker Compose are installed on your system
- Make sure no other services are running on the ports used by this project
- For any issues, check the `docker-compose.yml` and `.env` configuration

## Troubleshooting

- If you encounter permission issues, you may need to run Docker commands with `sudo`
- Check Docker logs for any startup or runtime errors
- Verify that all required environment variables are set correctly
