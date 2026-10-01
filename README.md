Siwiti Business Automation

An AI-assisted business automation web application built with Python, Flask, and SQLite. The project demonstrates how customer information and messages can be captured, analyzed, categorized, and managed through a simple web-based system.

Project Overview

Siwiti Business Automation is a portfolio project designed to demonstrate practical skills in:

Business process automation
Web application development
Customer data management
Message classification
Role-based access
Database management
Python and Flask development

The application allows customers to submit their information and messages, while authorized staff can access and manage customer records through an administrative dashboard.

Key Features
Customer Registration

Customers can register by providing:

First name
Middle name
Last name
Email
Password
Message

Passwords are securely stored using password hashing.

Automated Message Analysis

Customer messages are analyzed and assigned:

Category
Priority

For example:

Customer Message	Category	Priority
Problem with my payment	Payment	Normal
Information about investment opportunities	Investment	Normal

This demonstrates how automation can reduce manual processing of customer requests.

Role-Based Access

The system is designed to separate customer and staff access.

Authorized staff can access customer records through the business dashboard, while customers use their own account.

Business Dashboard

The dashboard provides an overview of customer requests, including:

Customer information
Email
Message
Category
Priority
Status
Database

The application uses SQLite to store application data locally.

Technologies Used
Python
Flask
SQLite
HTML
Jinja2
Werkzeug
Git & GitHub
Project Structure
Siwiti-Business-Automation/
│
├── app.py
├── automation.py
├── database.py
├── requirements.txt
├── README.md
│
├── database/
│   └── ...
│
├── templates/
│   ├── ...
│   └── ...
│
└── static/
    └── ...
How It Works

The basic workflow is:

Customer
   ↓
Registration / Login
   ↓
Submit Message
   ↓
Automated Message Analysis
   ↓
Category + Priority
   ↓
Database
   ↓
Staff Dashboard
Installation
1. Clone the repository
git clone https://github.com/yoelysiwiti/Siwiti-Business-Automation.git
2. Open the project
cd Siwiti-Business-Automation
3. Install dependencies
pip install -r requirements.txt
4. Run the application
python app.py

The application will normally be available at:

http://127.0.0.1:5000
Example Use Case

A customer submits:

"I have a problem with my payment."

The system processes the message and can classify it as:

Category: Payment
Priority: Normal
Status: Pending

The request can then be viewed and managed by authorized staff.

Purpose of the Project

This project was developed as a practical demonstration of how software development and automation can be applied to business operations.

It focuses on automating repetitive customer-request processing while maintaining structured records that can be accessed through a web-based dashboard.

Future Improvements

Possible future improvements include:

AI/LLM-powered message classification
Email notifications
Advanced analytics and reporting
Customer-specific dashboards
Cloud database integration
Production deployment
Improved user interface
API integration
Automated workflow notifications
Author

Yoeli Siwiti

GitHub:
https://github.com/yoelysiwiti

This project is a portfolio demonstration of Python, Flask, database management, and business automation concepts.