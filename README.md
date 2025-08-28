git add# 🚨 Emergency Services Simulation Platform

A comprehensive full-stack web application that simulates emergency services operations for Richmond, VA. This project demonstrates advanced Python development, database design, real-time web application skills, and comprehensive testing practices.

## 🎯 Project Overview

This emergency services simulation platform generates realistic incident data, stores it in both SQL Server and MongoDB databases, and provides a real-time web dashboard for monitoring and analysis. The project includes a complete testing suite and demonstrates modern software development practices.

## 🏗️ Architecture

### Technology Stack
- **Backend:** Python 3.10+, Flask
- **Databases:** SQL Server Express, MongoDB Community
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Data Generation:** Faker library for realistic data
- **Testing:** Comprehensive test suite with 100% success rate
- **Real-time Updates:** Auto-refresh with RESTful APIs

### Database Strategy
- **SQL Server:** Structured data (incidents, units, hospitals, metrics)
- **MongoDB:** Flexible document storage (detailed notes, real-time streams)

## 🚀 Features

### Core Functionality
- ✅ **Realistic Data Generation:** 6 specialized generators for comprehensive simulation
- ✅ **Dual Database Storage:** SQL Server for structured data, MongoDB for flexible documents
- ✅ **Real-time Dashboard:** Auto-refreshing incident display with interactive features
- ✅ **Professional UI:** Responsive design with proper separation of concerns
- ✅ **API Endpoints:** RESTful APIs for data retrieval and management
- ✅ **Comprehensive Testing:** 100% test coverage with automated validation

### Data Simulation Components
- **Incident Generator:** Medical emergencies, car accidents, shootings, mass casualty events
- **Crew Generator:** EMS personnel with realistic certifications and experience
- **Unit Generator:** EMS vehicles with status tracking and crew assignments
- **Hospital Generator:** Medical facilities with specialties and capacity management
- **Provider Notes Generator:** Real-time field updates and medical documentation
- **Master Generator:** Coordinates all components for complete simulation

### Priority System
- **Priority 1:** Cardiac arrest, DOA, unconscious/unresponsive
- **Priority 2:** Heart attack symptoms, stroke, severe bleeding, diabetic emergencies
- **Priority 3:** Respiratory symptoms, falls, minor injuries
- **Priority 4:** Non-emergency medical calls
- **Priority 5:** Administrative calls, information requests

## 📁 Project Structure

```
emergency-sim-project/
├── backend/
│   ├── data_generators/
│   │   ├── __init__.py
│   │   ├── base_generator.py
│   │   ├── incident_generator.py
│   │   ├── crew_generator.py
│   │   ├── unit_generator.py
│   │   ├── hospital_generator.py
│   │   ├── provider_notes_generator.py
│   │   └── master_generator.py
│   ├── api/
│   │   └── dashboard.py
│   ├── database_schemas.py
│   ├── unified_data_saver.py
│   ├── data_adapter.py
│   └── final_system_test.py
├── tests/
│   ├── test_faker.py
│   ├── test_data_generators.py
│   ├── test_database_connections.py
│   └── run_all_tests.py
├── frontend/
│   ├── emergency-dashboard/          # React TypeScript application
│   │   ├── src/
│   │   ├── public/
│   │   └── package.json
│   ├── static/
│   │   ├── css/
│   │   │   └── dashboard.css
│   │   └── js/
│   │       └── dashboard.js
│   └── templates/
│       └── dashboard.html
├── data/
│   └── rva-cityboundary.geojson
├── docs/
│   └── PROJECT_DIARY.md
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- SQL Server Express
- MongoDB Community
- Node.js (for React frontend)
- Git

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sfh1980/PostCodingBootcampProjects.git
   cd emergency-sim-project
   ```

2. **Install Python dependencies:**
   ```bash
   pip install flask faker pyodbc pymongo
   ```

3. **Set up databases:**
   ```bash
   python backend/database_schemas.py
   ```

4. **Run comprehensive tests:**
   ```bash
   cd tests
   python run_all_tests.py
   ```

5. **Generate sample data:**
   ```bash
   cd backend
   python -c "from data_generators.master_generator import MasterGenerator; mg = MasterGenerator(); mg.generate_complete_simulation()"
   ```

6. **Run the dashboard:**
   ```bash
   python api/dashboard.py
   ```

7. **Access the application:**
   Open your browser to `http://localhost:5000`

## 🧪 Testing Suite

### Test Coverage
- **Data Generator Tests:** Validates all 6 generators create realistic data
- **Database Connection Tests:** Verifies SQL Server and MongoDB connectivity
- **API Endpoint Tests:** Ensures Flask endpoints respond correctly
- **System Integration Tests:** End-to-end validation of complete data flow

### Running Tests
```bash
cd tests
python run_all_tests.py
```

**Current Status:** ✅ **100% Test Success Rate**

## 📊 Dashboard Features

### Real-time Incident Display
- **Live Updates:** Auto-refresh every 30 seconds
- **Priority Color Coding:** Visual priority indicators
- **Interactive Details:** Click to view full incident information
- **Responsive Design:** Works on desktop, tablet, and mobile

### Data Visualization
- **Recent Incidents Table:** Latest emergency calls
- **Detailed View:** Complete incident information including:
  - Caller demographics and medical history
  - Location data and coordinates
  - Emergency type and priority level
  - Vital signs and patient condition
  - Operator and provider notes

## 🎓 Learning Objectives Achieved

This project demonstrates proficiency in:

### Python Development
- Object-oriented programming with classes and methods
- Data generation and manipulation
- Web framework development with Flask
- Database connectivity and operations
- Comprehensive testing practices

### Database Design
- SQL Server schema design and implementation
- MongoDB document modeling
- Dual-database architecture strategies
- Indexing and performance optimization

### Web Development
- HTML5 semantic markup
- CSS3 responsive design
- JavaScript DOM manipulation
- RESTful API design and implementation
- Separation of concerns (HTML/CSS/JS)
- React TypeScript frontend development

### Software Engineering
- Test-driven development principles
- Comprehensive validation strategies
- Automated quality assurance
- Pre-deployment testing best practices

## 🔧 Technical Highlights

### Data Generation Strategy
- **6 Specialized Generators:** Each focused on specific data types
- **Faker Library:** Realistic fake data generation
- **Richmond-Specific:** Geographic accuracy for Virginia capital
- **Medical Realism:** Age-appropriate vital signs and symptoms
- **Priority Logic:** Multi-factor decision making for incident severity

### Database Architecture
- **Hybrid Approach:** SQL for structured data, MongoDB for flexibility
- **Performance Optimization:** Strategic indexing for query efficiency
- **Data Integrity:** Proper relationships and constraints
- **Scalability:** Designed for future analytics and reporting

### Testing Infrastructure
- **Comprehensive Coverage:** All components tested and validated
- **Automated Validation:** Data integrity and functionality checks
- **Pre-commit Testing:** Ensures quality before deployment
- **Performance Metrics:** Execution time and success rate tracking

## 🚀 Future Enhancements

### Planned Features
- **Map Integration:** Leaflet.js for geographic visualization
- **Real-time Updates:** WebSocket connections for live data
- **Analytics Dashboard:** Charts and graphs for incident analysis
- **User Authentication:** Role-based access (dispatcher, EMT, supervisor)
- **Mobile Application:** React Native for field use

### Scalability Considerations
- **Microservices Architecture:** Service-oriented design
- **Cloud Deployment:** AWS/Azure integration
- **Advanced Analytics:** Machine learning for incident prediction
- **Integration APIs:** Hospital and emergency services connectivity

## 📈 Portfolio Value

This project showcases:

- **Full-Stack Development:** Complete application from data to UI
- **Database Expertise:** Both SQL and NoSQL technologies
- **Real-time Applications:** Modern web development practices
- **Testing Excellence:** Comprehensive test coverage and validation
- **Domain Knowledge:** Emergency services and healthcare systems
- **Professional Quality:** Production-ready code and documentation

## 🤝 Contributing

This is a portfolio project demonstrating individual development skills. For educational purposes, feel free to fork and experiment with the codebase.

## 📄 License

This project is created for educational and portfolio purposes.

---

**Built with ❤️ for portfolio demonstration and learning**

*Demonstrating Python, SQL Server, MongoDB, Flask, React, and modern software development practices*
