# Premium Home CRM

## Description
Premium Home CRM is a robust customer relationship management application tailored for businesses dealing with high-end audio and appliance packages. The app helps manage sales pipelines, leads, and marketing campaigns. It streamlines workflows, improves customer satisfaction, and boosts sales efficiency.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Python, Django, PostgreSQL

## Features
- Client management (CRUD)
- Sales pipeline tracking
- Lead management system
- Marketing campaign management
- Responsive frontend templates

## Setup and Installation
1. Clone the repository
   ```zsh
   git clone https://github.com/jensen-dong/premium-home-crm.git
   ```
2. Set up virtual environment
   ```zsh
   cd premium-home-crm
   brew install pipenv
   pipenv shell
   ```
3. Set up PostgreSQL
   - Create new PostgreSQL database
   - Update DATABASES config in settings.py
4. Run migrations
   ```zsh
   python manage.py migrate
   ```
5. Create superuser
   ```zsh
   python manage.py createsuperuser
   ```
6. Start dev server
   ```zsh
   python manage.py runserver
   ```
## Usage
1. Navigate to http://127.0.0.1:8000/ in your browser.
2. Log in with your superuser account.
3. Start managing clients, interactions, leads, pipelines, and marketing campaigns.

## ERD
![Screenshot 2024-08-06 at 7 33 34 PM](https://github.com/user-attachments/assets/e6525f11-9995-4a4d-ae4d-9f00053b2879)

## Wireframes

- Dashboard (MVP)
  
![Screenshot 2024-08-06 at 8 02 51 PM](https://github.com/user-attachments/assets/b50f1523-dbbe-4ad2-8623-d1d9395ac815)

- Book of Business

![Screenshot 2024-08-06 at 8 02 57 PM](https://github.com/user-attachments/assets/94272471-1efc-4a39-8e55-41fb4e27070d)

- Leads

![Screenshot 2024-08-06 at 8 03 12 PM](https://github.com/user-attachments/assets/207fb209-99ec-4964-bf65-26ca8c241928)

- Pipeline (MVP)
  
![Screenshot 2024-08-06 at 8 03 07 PM](https://github.com/user-attachments/assets/6fe969b3-76f2-4281-930f-7309149221a5)

- Marketing Campaign

![Screenshot 2024-08-06 at 8 03 01 PM](https://github.com/user-attachments/assets/706b6fd4-bd07-432a-b65e-5b013577ac80)

