# Meal Management System

A comprehensive meal management system for confinement centers and healthcare facilities.

## Features

- **User Management**: Role-based access control with multiple user types
- **Menu Management**: Create and manage meal menus
- **Dish Management**: Manage individual dishes with nutritional information
- **Customer Management**: Track customer information and preferences
- **Order Management**: Process and track meal orders
- **Mother-Baby Care**: Specialized features for confinement meal management
- **Health Monitoring**: Track health metrics and nutritional needs
- **Appointment System**: Schedule and manage appointments
- **Nutrition Planning**: Create personalized nutrition plans

## Technology Stack

### Backend
- **Framework**: Flask
- **Database**: MySQL
- **Authentication**: JWT
- **API**: RESTful API

### Frontend
- **Framework**: Vue 3
- **UI Library**: Element Plus
- **Build Tool**: Vite
- **Styling**: CSS with custom themes

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
copy .env.example .env
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python app.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## User Roles

The system supports the following user roles:

| Role | Description | Color Theme |
|------|-------------|------------|
| admin | System administrator | Blue #3498db |
| nutritionist | Nutrition specialist | Blue #3498db |
| chef | Kitchen staff | Green #27ae60 |
| admin_staff | Administrative staff | Green #27ae60 |
| head_nurse | Head nurse | Green #27ae60 |
| nurse | Nursing staff | Green #27ae60 |
| caregiver | Caregiver | Green #27ae60 |
| customer | Customer/Patient | Light Pink #FF99A8 |
| guest | Guest user | Light Pink #FF99A8 |

## Default Users

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| nutritionist | nutr123 | nutritionist |
| chef | chef123 | chef |
| admin_staff | admin | admin_staff |
| head_nurse | nurse | head_nurse |
| nurse | nurse | nurse |
| caregiver | care | caregiver |
| customer | cust123 | customer |
| guest | guest123 | guest |

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Menu Management
- `GET /api/menus` - Get all menus
- `POST /api/menus` - Create new menu
- `PUT /api/menus/<id>` - Update menu
- `DELETE /api/menus/<id>` - Delete menu

### Dish Management
- `GET /api/dishes` - Get all dishes
- `POST /api/dishes` - Create new dish
- `PUT /api/dishes/<id>` - Update dish
- `DELETE /api/dishes/<id>` - Delete dish

### Customer Management
- `GET /api/customers` - Get all customers
- `POST /api/customers` - Create new customer
- `PUT /api/customers/<id>` - Update customer
- `DELETE /api/customers/<id>` - Delete customer

### Order Management
- `GET /api/orders` - Get all orders
- `POST /api/orders` - Create new order
- `PUT /api/orders/<id>` - Update order
- `DELETE /api/orders/<id>` - Delete order

## Database

The system uses MySQL as the database. The database schema includes tables for:

- Users and authentication
- Menus and dishes
- Customers and orders
- Health and nutrition data
- Appointments and schedules

## Docker Support

The system includes Docker support for easy deployment:

```bash
docker-compose up -d
```

## Security

- JWT-based authentication
- Role-based access control
- Input validation and sanitization
- Secure file upload handling
- Environment variable management

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact the development team.