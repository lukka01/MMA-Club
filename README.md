Django REST Framework-ზე დაფუძნებული სრული მართვის
სისტემა MMA სპორტული კლუბისთვის, რომელიც მოიცავს მომხმარებლების მართვას,
ვარჯიშების ორგანიზებას, ჩაწერების სისტემას და საწევროს პაკეტების მენეჯმენტს.

 სარჩევი:
ფუნქციონალი
ტექნოლოგიები
დაყენება
პროექტის გაშვება
API ტესტირება
Admin Panel
Docker-ით გაშვება
API Endpoints
ავტორიზაცია

 ფუნქციონალი:
 მომხმარებლების მართვა:

✅ რეგისტრაცია და ავტორიზაცია (JWT)
✅ 3 როლი: Admin, Coach, Member
✅ პროფილის მართვა
✅ პაროლის აღდგენა Email-ით
✅ პაროლის შეცვლა

 სპორტები და ვარჯიშები 🥊

✅ სპორტების CRUD (MMA, BJJ, ბოქსი და ა.შ.)
✅ ვარჯიშების შექმნა და მართვა
✅ სირთულის დონეები (დამწყები, საშუალო, მოწინავე)
✅ მონაწილეთა ლიმიტი
✅ მომავალი ვარჯიშების სია

 ჩაწერების სისტემა 📝:

✅ ვარჯიშებზე ჩაწერა/გაუქმება
✅ ადგილების ხელმისაწვდომობის შემოწმება
✅ ჩაწერების ისტორია
✅ დასწრების აღრიცხვა

  საწევროს მართვა 💳: 

✅ საწევროს პაკეტები (ბრინჯაო, ვერცხლი, ოქრო)
✅ საწევროს პერიოდი და ავტომატური განახლება
✅ ვარჯიშების რაოდენობის კონტროლი

 უსაფრთხოება 🔐:

✅ JWT Token Authentication
✅ Role-based Access Control
✅ Permission-ები თითო endpoint-ზე
✅ Token Blacklist (logout)


 ტექნოლოგიები:

Backend: Django 4.2.7, Django REST Framework 3.14.0
Authentication: Simple JWT 5.3.0
Database: SQLite (Development), PostgreSQL (Production)
Documentation: drf-yasg (Swagger/OpenAPI)
Filtering: django-filter 23.3
Image Processing: Pillow 10.1.0
Configuration: python-decouple 3.8
Containerization: Docker, Docker Compose


  დაყენება:

წინაპირობები
გქონდეთ დაინსტალირებული:

Python 3.11+
pip
Git
Docker და Docker Compose 

1. Repository-ის კლონირება
bashgit clone https://github.com/your-username/mma-club.git
cd mma-club
2. Virtual Environment
bash# Virtual Environment-ის შექმნა
python -m venv venv

# გააქტიურება (Windows)
venv\Scripts\activate

# გააქტიურება (Mac/Linux)
source venv/bin/activate
3. Dependencies-ის ინსტალაცია
bashpip install -r requirements.txt
4. Environment Variables
შექმენით .env ფაილი პროექტის root-ში:
envSECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@mmaclub.ge
5. Database Migration
bashpython manage.py makemigrations
python manage.py migrate
6. Superuser-ის შექმნა
bashpython manage.py createsuperuser
შეიყვანეთ:

Username: admin
Email: admin@mmaclub.ge
Password: admin123 (ან რაც გინდათ)


🚀 პროექტის გაშვება
Local გაშვება
bashpython manage.py runserver
პროექტი ხელმისაწვდომი იქნება:

🌐 API Documentation: http://localhost:8000/
📚 Swagger UI: http://localhost:8000/swagger/
📖 ReDoc: http://localhost:8000/redoc/
🎨 Admin Panel: http://localhost:8000/admin/


🧪 API ტესტირება
Swagger UI-ით ტესტირება
Swagger-ი საუკეთესო ხერხია API-ს სატესტად. გახსენით:
http://localhost:8000/swagger/

📍 ნაბიჯ-ნაბიჯ ტესტირება
1️⃣ რეგისტრაცია
Endpoint: POST /api/auth/register/

Swagger-ში იპოვეთ /api/auth/register/
დააჭირეთ "Try it out"
შეიყვანეთ JSON:

json{
  "username": "giorgi",
  "email": "giorgi@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "გიორგი",
  "last_name": "მელაძე",
  "phone": "555123456",
  "birth_date": "1995-05-15",
  "address": "თბილისი, ვაკე"
}

დააჭირეთ "Execute"
Response-ში მიიღებთ:

✅ User ინფორმაციას
✅ access_token - ავტორიზაციისთვის
✅ refresh_token - token-ის განახლებისთვის



მაგალითი Response:
json{
  "message": "რეგისტრაცია წარმატებით დასრულდა",
  "user": {
    "id": 1,
    "username": "giorgi",
    "email": "giorgi@example.com",
    "full_name": "გიორგი მელაძე",
    "role": "member"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGci..."
  }
}

2️⃣ ავტორიზაცია (Authorization)

დააკოპირეთ access_token რომელიც მიიღეთ რეგისტრაციისას
Swagger-ის ზემოთ მარჯვნივ დააჭირეთ 🔒 "Authorize" ღილაკს
შეიყვანეთ:

   Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
(დააკოპირეთ თქვენი access_token)
4. დააჭირეთ "Authorize"
5. დააჭირეთ "Close"
✅ ახლა ავტორიზებული ხართ! ყველა endpoint ხელმისაწვდომია.

3️⃣ ალტერნატიული Login
თუ უკვე გაქვთ ანგარიში:
Endpoint: POST /api/auth/login/
json{
  "username": "giorgi",
  "password": "SecurePass123!"
}

4️⃣ პროფილის ნახვა
Endpoint: GET /api/auth/users/me/

დააჭირეთ "Try it out"
დააჭირეთ "Execute"
დაინახავთ თქვენს პროფილს


5️⃣ სპორტების სია
Endpoint: GET /api/sports/
თუ ცარიელია, Admin Panel-ში დაამატეთ:

  Admin Panel-ში მონაცემების დამატება:
გადადით: http://localhost:8000/admin/
Login:

Username: admin
Password: admin123

სპორტების დამატება:

Sports → Add
შეიყვანეთ:

Name: MMA
Description: Mixed Martial Arts
Is active: ✓


Save

დაამატეთ კიდევ:

BJJ (Brazilian Jiu-Jitsu)
Boxing (ბოქსი)
Kickboxing (კიკბოქსინგი)
Muay Thai (ტაილანდური ბოქსი)


Coach როლის მინიჭება:

Users → თქვენი user
Role → აირჩიეთ Coach
Save


6️⃣ ვარჯიშის შექმნა
Endpoint: POST /api/trainings/
🔒 საჭიროა: Coach ან Admin როლი
json{
  "sport": 1,
  "title": "MMA საწყისი დონე",
  "description": "დამწყებთათვის MMA ძირითადი ტექნიკა და ფიზიკური მომზადება",
  "difficulty": "beginner",
  "date": "2024-12-28",
  "start_time": "18:00",
  "duration": 90,
  "max_participants": 15
}
Response:
json{
  "id": 1,
  "sport_name": "MMA",
  "coach_name": "გიორგი მელაძე",
  "title": "MMA საწყისი დონე",
  "date": "2024-12-28",
  "start_time": "18:00:00",
  "enrolled_count": 0,
  "available_spots": 15,
  "is_full": false,
  "is_enrolled": false
}

7️⃣ ვარჯიშებზე ჩაწერა
Endpoint: POST /api/trainings/{training_id}/enroll/

აირჩიეთ training ID (მაგ: 1)
Try it out
შეიყვანეთ training_id: 1
Execute

Response:
json{
  "message": "წარმატებით ჩაიწერეთ ვარჯიშზე",
  "enrollment": {
    "id": 1,
    "user_name": "გიორგი მელაძე",
    "training_title": "MMA საწყისი დონე",
    "training_date": "2024-12-28",
    "training_time": "18:00:00",
    "status": "confirmed"
  }
}

8️⃣ ჩემი ჩაწერების ნახვა
Endpoint: GET /api/enrollments/my-enrollments/
დაინახავთ ყველა ვარჯიშს რომელზეც ჩაწერილი ხართ.

9️⃣ მომავალი ვარჯიშები
Endpoint: GET /api/trainings/upcoming/
დაინახავთ მხოლოდ მომავალ ვარჯიშებს.

🔟 ჩაწერის გაუქმება
Endpoint: POST /api/trainings/{training_id}/cancel-enrollment/
training_id: 1
Response:
json{
  "message": "ჩაწერა გაუქმდა"
}

1️⃣1️⃣ საწევროს პაკეტების დამატება (Admin Panel)

Membership plans → Add
შეიყვანეთ:

Name: ბრინჯაო
Description: საწყისი პაკეტი დამწყებთათვის
Price: 100.00
Duration days: 30
Max trainings per week: 3


Save

დაამატეთ კიდევ:

ვერცხლი (150₾, 30 დღე, 5 ვარჯიში)
ოქრო (200₾, 30 დღე, უსაზღვრო)


1️⃣2️⃣ საწევროს პაკეტების ნახვა
Endpoint: GET /api/membership-plans/
json[
  {
    "id": 1,
    "name": "ბრინჯაო",
    "description": "საწყისი პაკეტი",
    "price": "100.00",
    "duration_days": 30,
    "max_trainings_per_week": 3,
    "members_count": 5
  },
  {
    "id": 2,
    "name": "ვერცხლი",
    "price": "150.00",
    "duration_days": 30,
    "max_trainings_per_week": 5,
    "members_count": 3
  }
]

1️⃣3️⃣ საწევროს მინიჭება (Admin Panel)

Memberships → Add
აირჩიეთ:

User: giorgi
Plan: ოქრო
Start date: 2024-12-01
End date: 2024-12-31
Is active: ✓


Save


1️⃣4️⃣ ჩემი საწევროს ნახვა
Endpoint: GET /api/memberships/my-membership/
json{
  "id": 1,
  "user_name": "გიორგი მელაძე",
  "plan_name": "ოქრო",
  "plan_details": {
    "name": "ოქრო",
    "price": "200.00",
    "max_trainings_per_week": 999
  },
  "start_date": "2024-12-01",
  "end_date": "2024-12-31",
  "is_active": true,
  "is_expired": false,
  "days_remaining": 10
}

1️⃣5️⃣ პაროლის აღდგენა
ნაბიჯი 1: პაროლის აღდგენის მოთხოვნა
Endpoint: POST /api/auth/password-reset/
json{
  "email": "giorgi@example.com"
}
Response:
json{
  "message": "პაროლის აღდგენის ინსტრუქცია გაიგზავნა თქვენს ელ-ფოსტაზე"
}
💡 Console-ში დაინახავთ email-ს reset token-ით

ნაბიჯი 2: პაროლის შეცვლა
Endpoint: POST /api/auth/password-reset-confirm/
json{
  "token": "aq2K3m4n5p6q7r8s9t0u1v2w3x4y5z",
  "password": "NewPass123!",
  "password_confirm": "NewPass123!"
}

1️⃣6️⃣ პაროლის შეცვლა (ავტორიზებულს)
Endpoint: POST /api/auth/change-password/
json{
  "old_password": "SecurePass123!",
  "new_password": "NewSecurePass123!",
  "new_password_confirm": "NewSecurePass123!"
}

1️⃣7️⃣ Token-ის განახლება
როცა access_token ვადაგასული იქნება (1 საათის შემდეგ):
Endpoint: POST /api/auth/token/refresh/
json{
  "refresh": "your_refresh_token_here"
}
Response:
json{
  "access": "new_access_token_here"
}

1️⃣8️⃣ Logout
Endpoint: POST /api/auth/logout/
json{
  "refresh": "your_refresh_token_here"
}
✅ Token blacklist-ში ჩაიწერება და გაუქმდება.

🔍 Filtering და Search
ვარჯიშების ფილტრაცია:
GET /api/trainings/?sport=1
GET /api/trainings/?difficulty=beginner
GET /api/trainings/?coach=1
GET /api/trainings/?date=2024-12-28
ძებნა:
GET /api/trainings/?search=MMA
GET /api/sports/?search=boxing
დალაგება:
GET /api/trainings/?ordering=date
GET /api/trainings/?ordering=-date  (დაბლოსკენ)
კომბინირებული:
GET /api/trainings/?sport=1&difficulty=beginner&ordering=date

🐳 Docker-ით გაშვება
Development Mode
bash# Container-ების აწყობა
docker-compose build

# გაშვება
docker-compose up -d

# Superuser შექმნა
docker-compose exec web python manage.py createsuperuser

# Logsნახვა
docker-compose logs -f

# გაჩერება
docker-compose down
პროექტი ხელმისაწვდომი იქნება: http://localhost:8000/

Production Mode
bash# Production setup (PostgreSQL + NGINX + Gunicorn)
docker-compose -f docker-compose.prod.yml up -d --build

# Superuser შექმნა
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Logs
docker-compose -f docker-compose.prod.yml logs -f

# გაჩერება
docker-compose -f docker-compose.prod.yml down

სასარგებლო Docker ბრძანებები
bash# Container-ების სტატუსი
docker-compose ps

# Django Shell
docker-compose exec web python manage.py shell

# Database Shell
docker-compose exec db psql -U mma_user -d mma_club_db

# Migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Static files
docker-compose exec web python manage.py collectstatic --noinput

# Container-ში შესვლა
docker-compose exec web bash

# ყველაფრის წაშლა და თავიდან დაწყება
docker-compose down -v
docker-compose build --no-cache
docker-compose up

📚 API Endpoints
🔐 Authentication
MethodEndpointDescriptionAuthPOST/api/auth/register/რეგისტრაცია❌POST/api/auth/login/ავტორიზაცია❌POST/api/auth/logout/გასვლა✅POST/api/auth/token/refresh/Token განახლება❌POST/api/auth/password-reset/პაროლის აღდგენა❌POST/api/auth/password-reset-confirm/პაროლის შეცვლა❌POST/api/auth/change-password/პაროლის შეცვლა✅
👥 Users
MethodEndpointDescriptionRoleGET/api/auth/users/მომხმარებლების სიაAdminGET/api/auth/users/me/ჩემი პროფილიAnyPUT/api/auth/users/me/პროფილის რედაქტირებაAnyGET/api/auth/users/{id}/მომხმარებლის დეტალებიOwner/AdminPUT/api/auth/users/{id}/მომხმარებლის რედაქტირებაOwner/AdminDELETE/api/auth/users/{id}/მომხმარებლის წაშლაAdmin
🥋 Sports
MethodEndpointDescriptionRoleGET/api/sports/სპორტების სიაAnyPOST/api/sports/სპორტის დამატებაAdminGET/api/sports/{id}/სპორტის დეტალებიAnyPUT/api/sports/{id}/სპორტის განახლებაAdminDELETE/api/sports/{id}/სპორტის წაშლაAdmin
💪 Trainings
MethodEndpointDescriptionRoleGET/api/trainings/ვარჯიშების სიაAnyPOST/api/trainings/ვარჯიშის შექმნაAdmin/CoachGET/api/trainings/upcoming/მომავალი ვარჯიშებიAnyGET/api/trainings/my-trainings/ჩემი ვარჯიშები (coach)CoachGET/api/trainings/{id}/ვარჯიშის დეტალებიAnyPUT/api/trainings/{id}/ვარჯიშის განახლებაAdmin/CoachDELETE/api/trainings/{id}/ვარჯიშის წაშლაAdmin/Coach
📝 Enrollments
MethodEndpointDescriptionRolePOST/api/trainings/{id}/enroll/ვარჯიშზე ჩაწერაMemberPOST/api/trainings/{id}/cancel-enrollment/ჩაწერის გაუქმებაMemberGET/api/enrollments/my-enrollments/ჩემი ჩაწერებიMemberGET/api/trainings/{id}/enrollments/ვარჯიშის ჩაწერებიAdmin/Coach
💳 Memberships
MethodEndpointDescriptionRoleGET/api/membership-plans/პაკეტების სიაAnyPOST/api/membership-plans/პაკეტის დამატებაAdminGET/api/membership-plans/{id}/პაკეტის დეტალებიAnyPUT/api/membership-plans/{id}/პაკეტის განახლებაAdminDELETE/api/membership-plans/{id}/პაკეტის წაშლაAdminGET/api/memberships/საწევროების სიაAdminPOST/api/memberships/საწევროს შექმნაAdminGET/api/memberships/my-membership/ჩემი საწევროMember

🔑 ავტორიზაცია
JWT Token-ები
პროექტში გამოიყენება JWT (JSON Web Token) ავტორიზაციისთვის.
Token ტიპები:

Access Token - API-სთან სამუშაოდ (ვადა: 1 საათი)
Refresh Token - Access Token-ის განახლებისთვის (ვადა: 7 დღე)

როგორ გამოვიყენო?

რეგისტრაცია/Login → მიიღე tokens
Header-ში დაამატე:

   Authorization: Bearer <access_token>

Token-ის განახლება (1 საათის შემდეგ):

   POST /api/auth/token/refresh/
   Body: {"refresh": "your_refresh_token"}
Postman-ში:

Authorization → Type: Bearer Token
Token: დაამატეთ access_token

cURL-ით:
bashcurl -H "Authorization: Bearer your_access_token" \
  http://localhost:8000/api/sports/

👤 როლები და უფლებები
🔴 Admin

სრული წვდომა ყველაფერზე
მომხმარებლების მართვა
სპორტების, ვარჯიშების, საწევროების მართვა

🟡 Coach

ვარჯიშების შექმნა და მართვა
საკუთარი ვარჯიშების ჩაწერების ნახვა
მონაწილეთა დასწრების აღრიცხვა

🟢 Member

ვარჯიშებზე ჩაწერა/გაუქმება
საკუთარი ჩაწერების ნახვა
საკუთარი საწევროს ნახვა
პროფილის რედაქტირება