from django.core.management.base import BaseCommand
from api.models import CustomUser, Service, Booking
from django.utils import timezone
import datetime
import random

class Command(BaseCommand):
    help = 'Seeds the database with a robust set of test users, services, and bookings for a demo.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing bookings and services...')
        Booking.objects.all().delete()
        Service.objects.all().delete()
        CustomUser.objects.exclude(is_superuser=True).delete()
        
        self.stdout.write('Seeding standard test users...')
        
        users_data = [
            # Homeowners
            {
                "email": "home@serbisure.com",
                "username": "home@serbisure.com",
                "full_name": "Maria Homeowner",
                "role": "homeowner",
                "password": "homepassword123"
            },
            {
                "email": "alex@serbisure.com",
                "username": "alex@serbisure.com",
                "full_name": "Alex Johnson",
                "role": "homeowner",
                "password": "homepassword123"
            },
            {
                "email": "cruz@serbisure.com",
                "username": "cruz@serbisure.com",
                "full_name": "Mrs. Cruz",
                "role": "homeowner",
                "password": "homepassword123"
            },
            # Workers
            {
                "email": "worker@serbisure.com",
                "username": "worker@serbisure.com",
                "full_name": "Pedro Worker",
                "role": "service_worker",
                "password": "workerpassword123"
            },
            {
                "email": "james@serbisure.com",
                "username": "james@serbisure.com",
                "full_name": "James Wilson",
                "role": "service_worker",
                "password": "workerpassword123"
            },
            {
                "email": "elena@serbisure.com",
                "username": "elena@serbisure.com",
                "full_name": "Elena Rodriguez",
                "role": "service_worker",
                "password": "workerpassword123"
            },
            {
                "email": "mike@serbisure.com",
                "username": "mike@serbisure.com",
                "full_name": "Mike Chen",
                "role": "service_worker",
                "password": "workerpassword123"
            }
        ]

        # 1. Create Users
        created_homeowners = []
        created_workers = []
        for data in users_data:
            password = data.pop('password')
            user = CustomUser.objects.create_user(
                email=data['email'],
                username=data['username'],
                full_name=data['full_name'],
                role=data['role'],
                password=password
            )
            if data['role'] == 'homeowner':
                created_homeowners.append(user)
            else:
                created_workers.append(user)

        self.stdout.write(f'Created {len(created_homeowners)} Homeowners and {len(created_workers)} Workers.')

        # 2. Assign services to workers
        services_data = [
            {"worker": "worker@serbisure.com", "name": "General House Cleaning", "description": "Professional cleaning service for your entire home.", "category": "Cleaning", "price": 500.00},
            {"worker": "worker@serbisure.com", "name": "Deep Cleaning", "description": "Move-in / Move-out deep cleaning.", "category": "Cleaning", "price": 1200.00},
            {"worker": "james@serbisure.com", "name": "Aircon Cleaning", "description": "Full chemical cleaning for split or window-type AC units.", "category": "HVAC", "price": 1200.00},
            {"worker": "james@serbisure.com", "name": "Aircon Repair", "description": "Freon charging and leaks repair.", "category": "HVAC", "price": 2000.00},
            {"worker": "elena@serbisure.com", "name": "Interior Painting", "description": "Room painting and touchups.", "category": "Carpentry", "price": 3000.00},
            {"worker": "mike@serbisure.com", "name": "Emergency Plumbing", "description": "Fixing leaks, toilets, and pipe burst repairs.", "category": "Plumbing", "price": 800.00},
            {"worker": "mike@serbisure.com", "name": "Electrical Repair", "description": "Fixing sockets, light fixtures, and breaker issues.", "category": "Electrical", "price": 750.00}
        ]

        created_services = []
        for s_data in services_data:
            worker = next(w for w in created_workers if w.email == s_data['worker'])
            service = Service.objects.create(
                name=s_data['name'],
                description=s_data['description'],
                category=s_data['category'],
                price=s_data['price'],
                provider=worker
            )
            created_services.append(service)

        self.stdout.write(f'Created {len(created_services)} services.')

        # 3. Create Bookings
        # Give Maria some specific bookings so it matches the demo properly
        maria = next(h for h in created_homeowners if h.email == 'home@serbisure.com')
        
        # Maria's bookings
        Booking.objects.create(
            homeowner=maria, 
            service=created_services[0], # General House Cleaning
            status="pending",
            scheduled_date=timezone.now().date() + datetime.timedelta(days=2)
        )
        Booking.objects.create(
            homeowner=maria, 
            service=created_services[2], # Aircon Cleaning
            status="confirmed",
            scheduled_date=timezone.now().date() + datetime.timedelta(days=4)
        )
        Booking.objects.create(
            homeowner=maria, 
            service=created_services[5], # Plumbing
            status="completed",
            scheduled_date=timezone.now().date() - datetime.timedelta(days=2)
        )
        
        # Give other homeowners some bookings distributed randomly
        for homeowner in [h for h in created_homeowners if h.email != 'home@serbisure.com']:
            for _ in range(3):
                service = random.choice(created_services)
                status = random.choice(["pending", "confirmed", "completed", "cancelled"])
                delta = random.randint(-5, 10)
                Booking.objects.create(
                    homeowner=homeowner,
                    service=service,
                    status=status,
                    scheduled_date=timezone.now().date() + datetime.timedelta(days=delta)
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with demo data!'))
