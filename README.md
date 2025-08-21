# 🚨 Emergency Services Simulation Platform

A comprehensive full-stack web application that simulates emergency services operations for Richmond, VA. This project demonstrates advanced Python development, database design, and real-time web application skills.

## 🎯 Project Overview

This emergency services simulation platform generates realistic incident data, stores it in both SQL Server and MongoDB databases, and provides a real-time web dashboard for monitoring and analysis. Perfect for portfolio demonstration of full-stack development capabilities.

## 🏗️ Architecture

### Technology Stack
- **Backend:** Python 3.10+, Flask
- **Databases:** SQL Server Express, MongoDB Community
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Data Generation:** Faker library for realistic data
- **Real-time Updates:** Auto-refresh with RESTful APIs

### Database Strategy
- **SQL Server:** Structured data (incidents, units, hospitals, metrics)
- **MongoDB:** Flexible document storage (detailed notes, real-time streams)

## 🚀 Features

### Core Functionality
- ✅ **Realistic Data Generation:** Medical emergencies, non-medical incidents, Richmond-specific addresses
- ✅ **Dual Database Storage:** SQL Server for structured data, MongoDB for flexible documents
- ✅ **Real-time Dashboard:** Auto-refreshing incident display with interactive features
- ✅ **Professional UI:** Responsive design with proper separation of concerns
- ✅ **API Endpoints:** RESTful APIs for data retrieval and management

### Data Simulation
- **Incident Types:** Medical emergencies, car accidents, shootings, mass casualty events
- **Priority Levels:** 1-5 scale based on medical severity and patient condition
- **Geographic Accuracy:** Richmond, VA addresses and coordinates
- **Realistic Patterns:** Age-based vital signs, emergency-specific symptoms

## 📁 Project Structure

```
emergency-sim-platform/
├── dashboard.py              # Flask web server
├── incident_generator.py     # Core data generation logic
├── incident_data.py          # Data definitions and constants
├── database_setup.py         # Database creation and setup
├── database_schemas.py       # Schema definitions
├── data_saver.py            # Database persistence layer
├── templates/
│   └── dashboard.html       # Main dashboard template
├── static/
│   ├── css/
│   │   └── dashboard.css    # Styling with separation of concerns
│   └── js/
│       └── dashboard.js     # Interactive functionality
├── data/
│   └── rva-cityboundary.geojson  # Richmond city boundaries
└── docs/                    # Documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- SQL Server Express
- MongoDB Community
- Git

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/sfh1980/PostCodingBootcampProjects.git
   cd emergency-sim-platform
   ```

2. **Install Python dependencies:**
   ```bash
   pip install flask faker pyodbc pymongo
   ```

3. **Set up databases:**
   ```bash
   python database_setup.py
   ```

4. **Generate sample data:**
   ```bash
   python incident_generator.py
   ```

5. **Run the dashboard:**
   ```bash
   python dashboard.py
   ```

6. **Access the application:**
   Open your browser to `http://localhost:5000`

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

### Real-world Application
- Emergency services domain knowledge
- Geographic data integration
- Real-time data handling
- Professional UI/UX design

## 🔧 Technical Highlights

### Data Generation Strategy
- **Faker Library:** Realistic fake data generation
- **Richmond-Specific:** Geographic accuracy for Virginia capital
- **Medical Realism:** Age-appropriate vital signs and symptoms
- **Priority Logic:** Multi-factor decision making for incident severity

### Database Architecture
- **Hybrid Approach:** SQL for structured data, MongoDB for flexibility
- **Performance Optimization:** Strategic indexing for query efficiency
- **Data Integrity:** Proper relationships and constraints
- **Scalability:** Designed for future analytics and reporting

### Web Application Design
- **Separation of Concerns:** Clean file organization
- **Security:** XSS prevention with HTML escaping
- **Performance:** Efficient API endpoints and caching
- **User Experience:** Intuitive interface with real-time updates

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
- **Domain Knowledge:** Emergency services and healthcare systems
- **Professional Quality:** Production-ready code and documentation

## 🤝 Contributing

This is a portfolio project demonstrating individual development skills. For educational purposes, feel free to fork and experiment with the codebase.

## 📄 License

This project is created for educational and portfolio purposes.

---

**Built with ❤️ for portfolio demonstration and learning**

*Demonstrating Python, SQL Server, MongoDB, Flask, and modern web development skills*
