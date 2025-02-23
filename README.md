Here's an updated **README.md** with **Example API Requests** and **Docker Setup**.

---

# **Trading Journal API 📊**

A FastAPI-based **Trading Journal** that allows users to log trades, track performance, and add notes for insights. This project includes **user authentication, trade tracking, and note-taking**, with soft-delete functionality for data retention.

---

## 🚀 **Features**
✅ User authentication & management  
✅ Trade logging & performance tracking  
✅ Trade notes for insights & lessons  
✅ Soft-delete support for users, trades, and notes  
✅ Automated tests with **pytest**  
✅ Docker support for easy deployment  

---

## 🛠 **Setup & Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/zmomz/trading-journal.git
cd trading-journal
```

### **2. Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure the Database**
Ensure **PostgreSQL** is running and create a database:
```sql
CREATE DATABASE trading_journal;
```
Update **`app/config.py`** or **`.env`** with the correct database URL.

### **5. Apply Migrations**
```bash
alembic upgrade head
```

### **6. Run the API**
```bash
uvicorn app.main:app --reload
```
Visit: **http://127.0.0.1:8000/docs** for Swagger UI.

---

## 📦 **Docker Setup**
Run the project using **Docker**:

### **1. Build the Docker Image**
```bash
docker build -t trading-journal .
```

### **2. Run the Container**
```bash
docker run -d -p 8000:8000 --env-file .env trading-journal
```

### **3. Stop the Container**
```bash
docker ps  # Get container ID
docker stop <container_id>
```

### **Using Docker Compose**
If you have a **docker-compose.yml**, simply run:
```bash
docker-compose up -d
```

---

## ✅ **Running Tests**
Run all tests with **pytest**:
```bash
pytest
```
Run tests for a specific module:
```bash
pytest tests/test_trade.py
```

---

## 📂 **Project Structure**
```
📂 app
 ┣ 📂 crud         # Database operations (CRUD)
 ┣ 📂 models       # SQLAlchemy models
 ┣ 📂 schemas      # Pydantic schemas for validation
 ┣ 📂 routes       # API endpoints
 ┣ 📂 tests        # Unit tests
 ┗ main.py         # FastAPI entry point
```

---

## 🔗 **Example API Requests**

### **1️⃣ Register a User**
```bash
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{
  "username": "trader1",
  "email": "trader1@example.com",
  "password": "securepassword"
}'
```

### **2️⃣ Get a User**
```bash
curl -X GET "http://127.0.0.1:8000/users/1"
```

### **3️⃣ Create a Trade**
```bash
curl -X POST "http://127.0.0.1:8000/trades/" -H "Content-Type: application/json" -d '{
  "user_id": 1,
  "asset_symbol": "BTC",
  "market": "Crypto",
  "currency": "USD",
  "trade_type": "Buy",
  "entry_price": 45000,
  "position_size": 1.5
}'
```

### **4️⃣ Get a Trade**
```bash
curl -X GET "http://127.0.0.1:8000/trades/1"
```

### **5️⃣ Add a Trade Note**
```bash
curl -X POST "http://127.0.0.1:8000/trades/1/notes" -H "Content-Type: application/json" -d '{
  "trade_id": 1,
  "reason": "Entered after strong breakout"
}'
```

### **6️⃣ Soft Delete a User**
```bash
curl -X DELETE "http://127.0.0.1:8000/users/1"
```

---

## 🔧 **Recent Fixes & Updates**
- ✅ **Fixed IntegrityError in user deletions**  
- ✅ **Improved test cleanup for database consistency**  
- ✅ **Refactored soft-delete logic in notes & trades**  
- ✅ **Updated test fixtures for better isolation**  
- ✅ **Added Docker support for deployment**  

---

## 📌 **Contributing**
Contributions are welcome! Feel free to **fork the repo, open an issue, or submit a PR**.
