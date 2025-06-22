# Multi-Level Referral & Earnings System API

A backend API built with **FastAPI** implementing a multi-level referral system with real-time earnings tracking and WebSocket notifications.  
Supports up to 8 direct referrals per user and distributes profits across referral levels.

---

## Features

- User registration and login with JWT authentication  
- Create referrals with validation rules (max 8 direct referrals)  
- Record transactions and distribute earnings across 2 referral levels  
- Real-time notifications using WebSocket connections  
- MongoDB for NoSQL data storage (users, referrals, earnings)  
- Password hashing with bcrypt for secure authentication  
- Pydantic schemas with robust validation  
- Async functions for efficient I/O operations  

---

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)  
- [MongoDB](https://www.mongodb.com/)  
- [Pydantic](https://pydantic.dev/)  
- [JWT (python-jose)](https://python-jose.readthedocs.io/)  
- [Passlib](https://passlib.readthedocs.io/) for password hashing  
- WebSocket for real-time communication  

---

## Getting Started

### Prerequisites

- Python 3.10+  
- MongoDB instance (local or cloud, e.g. MongoDB Atlas)  
- Git  
