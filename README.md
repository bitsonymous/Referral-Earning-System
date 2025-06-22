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

### Profit Distribution Logic:
1. **Direct Earnings:**  
   The parent user earns 5% of the profit from their direct referrals (Level 1 users).

2. **Indirect Earnings:**  
   The parent user earns 1% of the profit made by their direct referrals from second-level users (Level 2).

3. **Profit Conditions:**  
   Earnings apply only when a purchase exceeds ₹1000.  
   Profits are calculated and updated in real-time.

---

## Key Responsibilities & Features

### System Architecture:
- Design and implement a multi-level referral hierarchy with a limit of 8 direct referrals per user.
- Develop scalable logic for profit distribution across multiple levels.

### Profit Tracking and Distribution:
- Calculate earnings for:  
  - Direct Referrals: 5% of profits from Level 1 users.  
  - Indirect Referrals: 1% of profits from Level 2 transactions generated through Level 1 users.
- Exclude profits for purchases below the ₹1000 threshold.

### Database Design:
- **Users Database:**  
  Store user profiles, referral hierarchies, and levels.  
  Track relationships between users across multiple levels.

- **Earnings Database:**  
  Record transactions, percentages, and detailed earnings breakdowns per user and referral.

### Live Data Feed:
- Implement a real-time notification system to deliver live updates for earnings:  
  Parent users can see live earnings updates without refreshing the page or hitting the API.

### Reports and Analytics:
- Build APIs to fetch detailed reports:  
  - Real-time earnings reports for any user.  
  - Breakdown of earnings across levels and referrals.
- Provide visualizations to display:  
  - Referral-based earnings distribution.  
  - Earning sources from each leg of the referral tree.

---

## Additional Requirements:
1. **Purchase Validation:**  
   Ensure profit calculations are only applied when the purchase amount exceeds ₹1000.

2. **Edge Case Handling:**  
   Account for inactive users, invalid referrals, and scenarios where referral limits are exceeded.

3. **Data Privacy:**  
   Ensure secure handling of user data and compliance with relevant privacy regulations.

---

## Bonus Features:
1. **Notifications:**  
   Notify users in real-time when they earn from direct or indirect referrals using WebSockets.

---

## Expected Deliverables:
1. Fully functional referral system:  
   - Direct and indirect profit distribution logic.  
   - Real-time data updates via WebSockets for earnings notifications.

2. Database schemas:  
   - Users: Profile, hierarchy, and referral relationships.  
   - Earnings: Transaction history and breakdown of referral-based earnings.

3. APIs:  
   - Fetch profit reports and referral analytics.

4. Documentation:  
   - Detailed setup, API usage, and system architecture explanation.

---
