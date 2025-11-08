# 🚗 RentCar System

A **Car Rental Management System** built using **Django** and **Django REST Framework (DRF)**.
The system enables customers to browse available vehicles, make bookings, and manage rental operations, while admins can control and monitor all system data.

---

## 👥 Team Members

| Role | Name |
|------|------|
| Developer | **Anas Daraghmeh** |
| Developer | **Hamza Alkhateeb** |
| Developer | **Qasem Qareish** |
| Mentor | **Abed Zalloom** |

---

## 💡 Project Overview

The **RentCar System** is a web-based backend platform that provides RESTful APIs for a car rental business.
It allows **customers** to register, view cars, and make or manage bookings — and allows **admins** to manage vehicles and review reservations.

This project is part of an **introductory Django REST Framework training project** under the mentorship of **Abed Zalloom**.

---

---

## 🎯 Main Features & Requirements

### ➤ Customer APIs
| Feature | Description | # of APIs |
|----------|--------------|------------|
| **Login / Register** | Customers can register and log in using DRF authentication. | 2 |
| **Edit Profile** | Customers can update their personal info (phone, address, etc). | 1 |
| **List Available Cars** | View all cars with filter options (e.g., available / rented). Uses **filterset** for state filtering. | 1 |
| **Rent a Car** | Customer can rent a specific car via a form API containing customer info, car info, and payment method. | 1 |
| **Edit / Delete Reservation** | Customer can send requests to edit or delete an existing reservation. | 2 |

✅ **Total Customer APIs:** 7

### ➤ System Admin APIs
| Feature | Description | # of APIs |
|----------|--------------|------------|
| **Add Car** | Create a new car record. | 1 |
| **Edit Car** | Update existing car information. | 1 |
| **Delete Car** | Remove a car record. | 1 |
| **List Cars** | View all cars (available & unavailable). | 1 |
| **Review Reservations** | Review all customer reservations. | 1 |

✅ **Total Admin APIs:** 5

---

## 🧩 Project Structure

The system consists of three main Django apps:

| App | Description | Working on it
|-----|--------------|-------
| **Customer** | Handles registration, authentication, and profile management. | `Anas`
| **Vehicle** | Manages car information such as brand, model, year, daily rate, and availability. | `Hamza`
| **Booking** | Handles reservations, booking status, and total cost calculations. | `Qasem`

---

## 🧠 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/hamza7alkhateeb/rentCarSystem.git
```

### 2. Navigate to the project folder

```bash
cd rentCarSystem
```

### 3. Create your virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**On Windows:**

```bash
venv\Scripts\activate
```

**On Mac/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
### 7. Run server

```bash
python manage.py runserver
```

Then visit:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 👨🏻‍💻 Development Guidelines

* Each developer should **create a new branch** before starting work:

  ```bash
  git checkout -b your-branch-name
  git push -u origin your-branch-name
  ```
* Use your **own virtual environment** and **local database**.
* Always install the latest dependencies from `requirements.txt`.

use :
```bash
pip install -r requirements.txt
```
---

## 🌟 Future Enhancements (Roadmap)

To elevate the system toward a fully integrated car rental management platform, our future plans include the development of intelligent and advanced operational features:

### A. Artificial Intelligence & Machine Learning (AI)

These features will optimize revenue and minimize operational risk by leveraging data-driven decisions:

* **Dynamic Pricing:** Use machine learning algorithms to automatically adjust rental prices based on **real-time demand**, **seasonality**, and fleet availability to maximize yield.
* **Predictive Maintenance:** Analyze vehicle usage data, mileage, and historical failure patterns to **forecast potential breakdowns** and schedule maintenance proactively.
* **Automated Damage Detection:** Apply **Computer Vision** techniques to inspect vehicle conditions through uploaded images/videos at check-in/out, ensuring transparency and minimizing customer disputes.
* **Fraud Prevention & Identity Verification:** Implement AI models to enhance accuracy in **verifying customer documents** (e.g., driving licenses) and detecting suspicious booking behaviors to mitigate financial risk.

---

### B. Fleet Management & Operations

These enhancements focus on securing and optimizing the physical assets and administrative workflow:

* **GPS Tracking:** Integrate **real-time GPS tracking** for vehicles to monitor fleet movement, security, and optimize logistics.
* **Comprehensive Maintenance Management:** Implement modules to manage detailed **maintenance schedules**, renewal dates, and digital vehicle licensing records.
* **Customer Eligibility Management:** Digitally verify driving licenses and required legal documents to **ensure renter eligibility** and compliance before confirming a booking.

---

### C. User Experience & Technology

These items ensure a modern, secure, and user-friendly platform:

* **Improved Security & Authentication:** Strengthen user session management by adopting **JWT Authentication** and enhanced security protocols.
* **Integrated Online Payments:** Add reliable electronic payment options (e.g., Stripe/PayPal integration) to **simplify the booking and payment process**.
* **Front-End Development:** Build a clean and responsive user interface (using **React/Vue** for the customer side and **Bootstrap** for the Admin dashboard).
* **Advanced Dashboards & Reports:** Provide management dashboards with **deep analytics** and insights on rentals, revenue, fleet utilization, and performance metrics.

### ⚙️ Background Tasks with Celery

The **RentCar System** uses **Celery** to handle background tasks such as automatically updating booking statuses and running scheduled operations without affecting the user experience or system performance.

Celery is connected to **Redis** as a message broker and managed via **Celery Beat** to trigger scheduled tasks automatically.  
In this project, a scheduled task called `update_status` runs every **24 hours**, checks all confirmed bookings that have ended, and automatically updates their status to **"Completed"** ✅.

---

#### 💡 How It Works:

- **Celery Worker:** Executes background tasks.
- **Celery Beat:** Triggers scheduled jobs automatically.
- **Redis:** Acts as a message broker between Django and Celery.
- **Task Logic:** Defined inside `tasks.py` in the `Booking` app.

---

#### 🚀 To Run Celery:

1. Make sure **Redis** is running on your machine.
2. Open **Terminal 1** to run the Worker:
```bash
celery -A rentCarSystem worker -l info
```
3. Open Terminal 2 to run the Beat:
```bash
celery -A rentCarSystem beat -l info
```


**🔶NOTE :** This project is for **educational and training purposes only under the `Sitech` company program**.

Developed by **Anas Daraghmeh**, **Hamza Alkhateeb**, and **Qasem Qareish** under the mentorship of **Abed Zalloom**.