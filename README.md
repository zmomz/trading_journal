# Trading Journal API

## Overview
A FastAPI-powered trading journal for tracking trades, performance metrics, and analytics.

## Features
- Trade Entry & Tracking
- Performance Metrics (P/L, Win Rate, Risk-Reward, Drawdown)
- DCA Tracking
- Notes & Strategy Analysis
- JWT Authentication
- PostgreSQL + SQLAlchemy
- Automated Migrations with Alembic

## Installation
```bash
git clone https://github.com/yourusername/trading-journal.git
cd trading-journal
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Running the App
```bash
uvicorn app.main:app --reload
```

## Environment Variables
Create a `.env` file and add:
```
DATABASE_URL=sqlite:///./trading_journal.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running Tests
```bash
pytest
```

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST   | /users/ | Register a new user |
| GET    | /users/{id} | Get user details |
| POST   | /trades/ | Create a new trade |
| GET    | /trades/{id} | Get trade details |
| GET    | /trades/user/{user_id} | Get all trades for a user |
| POST   | /notes/ | Add a trade note |
| GET    | /notes/{id} | Get trade note |

## Docker Setup (Optional)
```bash
docker-compose up --build
```

## License
MIT
