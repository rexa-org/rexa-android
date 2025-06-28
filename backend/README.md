# reX Backend API

This is the backend API for the reX (Reward Exchange) platform, built with FastAPI and PostgreSQL.

## Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### Running the Application

1. **Clone and navigate to the project root:**
   ```bash
   cd /path/to/rexa-android
   ```

2. **Start the services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Health check: http://localhost:8000/health
   - API documentation: http://localhost:8000/docs

### Environment Variables

The application uses the following environment variables (configured in docker-compose.yml):

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT tokens
- `SECRET_KEY`: Application secret key
- `DEBUG`: Debug mode (true/false)

### Database

The application automatically:
- Creates the PostgreSQL database
- Runs Alembic migrations on startup
- Sets up the initial schema

### Development

For local development without Docker:

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `/auth` - Authentication endpoints
- `/users` - User management
- `/rewards` - Reward management
- `/marketplace` - Marketplace operations
- `/wallet` - Wallet operations
- `/payments` - Payment processing
- `/admin` - Admin operations

## Stopping the Application

```bash
docker-compose down
```

To remove volumes (database data):
```bash
docker-compose down -v
``` 