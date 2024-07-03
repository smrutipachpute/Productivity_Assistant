# Productivity Assistant
#### Description:
  ### Overview:
    Productivity Assistant is a web application designed to help users manage their tasks, appointments, and deadlines effectively. The application provides a user-friendly interface for creating, viewing, editing, and deleting tasks, helping users stay organized and focused on their daily activities. With features like user authentication, a detailed dashboard, and visual productivity metrics, Productivity Assistant aims to streamline task management and enhance user productivity.
  
  ### Features:
    - User Authentication: Secure user registration and login functionality.
    - Dashboard: Displays a table of all tasks, allowing users to quickly overview their tasks.
    - Task Details: Click on a task title in the dashboard to view detailed information about the task.
    - Edit and Delete Tasks: Easily update task details or remove tasks from your list.
    - Update Task Status: Mark tasks as completed directly from the task details page.
    - Productivity Scale: A 3D pie chart visualizes the ratio of completed to pending tasks, providing a quick snapshot of user productivity.
    - Change Password: Users can securely change their password.
  
  ### Technology Stack:
    - Frontend: HTML, CSS, JavaScript
    - Backend: Python, Flask
    - Database: SQLite
    - Styling: Custom CSS for a clean and intuitive interface

  ### Project Structure:
    productivity-assistant/
    │
    ├── app/
    │   ├── __init__.py:  Initializes the Flask application and sets up configurations.
    │   ├── models.py: Defines the database models for users and tasks.
    │   ├── database.py: Handles database initialization and migrations.
    │   ├── routes.py: Contains the routes for handling user interactions, task management, and rendering templates.
    ├── templates/ : Contains HTML templates for rendering different pages(responsive)
    │   ├── base_login.html : Base template for login-related pages.
    │   ├── base.html : Base template for all other pages, includes common layout elements.
    │   ├── changepw.html : Template for changing the user password.
    │   ├── completion_base.html : Base template for completion-related pages.
    │   ├── completion_rates.html : Template for form for getting details required for displaying the 3D pie chart for monthly task completion rates.
    │   ├── create_task.html : Template for creating new tasks.
    │   ├── dashboard.html : Main dashboard displaying all tasks in form of a HTML table.
    │   ├── edit_task.html : User-friendly template for editing the existing tasks.
    │   ├── login.html : Template for user login by secure user authentication.
    │   ├── pie_chart.html : Template for displaying the 3D pie chart for monthly task completion rates.
    │   ├── signup.html : Template for new user registration and secure account creation.
    │   ├── view_task.html : Template for viewing task details.
    ├── static/
    │   ├── css/
    │   │   ├── background.css : Stylizes the responsive background of Productivity Assistant.
    │   │   ├── create_task.css : Stylizes the Task Creation page and create task form.
    │   │   ├── dashboard.css : Stylizes the tasks dashboard (responsive table).
    │   │   ├── dropdown.css : Stylizes the dropdown menu that shows the list of features for the user.
    │   │   ├── login.css : Stylizes the login, signup and change password form.
    │   │   ├── view_task.css : Stylizes the View Task page.
    │   └── img/
    │       ├── planning.png : Icon for Productivity Assistant(after login)
    │       ├── settings.png : Icon for Productivity Assistant's Login and Signup Page.
    ├── instance/
    │   ├── database.db : The SQLite database file with user and task table(details of the table provided in database.sql file).
    ├── config.py : Configuration file for the Flask Application.
    ├── run.py : Entry Point for the Flask Application.
    ├── database.sql : SQL file having detailed database schema.
    └── README.md : Documentation for the Productivity Assistant

  ### Features Detail:
  
    ## User Authentication
    The application ensures secure user authentication with encrypted passwords and session management.
    
    ## Dashboard
    The dashboard provides an overview of all tasks, allowing users to easily manage their daily, weekly, and monthly responsibilities.
    
    ## Task Management
    Users can create, edit, and delete tasks. Each task can have a title, description, deadline, and status.
    
    ## Task Details
    Clicking on a task title redirects to a detailed view of the task, where users can also edit or delete the task.
    
    ## Change Password
    Users can update their passwords securely through the change password feature.
    
    ## Productivity Scale
    A 3D pie chart visualizes the ratio of completed to pending tasks, providing a quick snapshot of user productivity.

### Design Choices:
    When designing the Productivity Assistant, several key decisions were made to enhance user experience and functionality:
      #  Modular Structure: The application is divided into modules, each responsible for specific functionality, ensuring better organization and maintainability.
      #  Database Models: The choice to use SQLAlchemy for ORM (Object-Relational Mapping) simplifies database interactions and allows for easy database migrations.
      #  Responsive Design: Custom CSS ensures that the application is visually appealing and functional across different devices and screen sizes.
      #  User Experience: The inclusion of feature like the productivity scale provides users with valuable insights into their task management habits.
      #  Security: Implementing secure password hashing and session management to protect user data.

### Future Enhancements:
    # Google Calendar Integration: Sync tasks with Google Calendar for better task management across platforms.
    # Analytics Dashboard: Provide insights and analytics on task completion rates and productivity trends.
    # Task Categories and Priorities: Allow users to categorize tasks and set priorities to better manage their workload.
    # Notifications: Implement email or push notifications to remind users of upcoming deadlines.
