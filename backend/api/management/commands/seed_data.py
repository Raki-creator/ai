from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Chat, ChatMessage, Memory, Reminder

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with test users and dummy data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 1. Create a Superuser
        if not User.objects.filter(username='admin@example.com').exists():
            User.objects.create_superuser(
                username='admin@example.com',
                email='admin@example.com',
                password='password',
                first_name='Admin',
                title='System Architect'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin@example.com / password'))

        # 2. Create Regular Users
        users_data = [
            {
                'email': 'jane@example.com',
                'name': 'Jane Doe',
                'title': 'Creative Director',
                'location': 'New York, NY',
                'bio': 'Passionate about design and AI orchestration.'
            },
            {
                'email': 'bob@example.com',
                'name': 'Bob Smith',
                'title': 'Software Engineer',
                'location': 'Austin, TX',
                'bio': 'Loves building scalable systems and drinking coffee.'
            }
        ]

        for u in users_data:
            if not User.objects.filter(username=u['email']).exists():
                user = User.objects.create_user(
                    username=u['email'],
                    email=u['email'],
                    password='password',
                    first_name=u['name'],
                    title=u['title'],
                    location=u['location'],
                    bio=u['bio']
                )
                self.stdout.write(self.style.SUCCESS(f'Created user: {u["email"]} / password'))

                # 3. Add Some Dummy Data for each user
                # Reminders
                Reminder.objects.create(user=user, text='Review project documentation', tag='work', due_date='Tomorrow')
                Reminder.objects.create(user=user, text='Buy groceries', tag='personal', due_date='Today, 6pm')
                
                # Memories
                Memory.objects.create(
                    user=user, 
                    title='Deep Seek AI Architecture', 
                    snippet='The architecture relies heavily on Mixture-of-Experts (MoE) for efficiency...',
                    type='Article',
                    category='important'
                )
                
                # Chats
                chat = Chat.objects.create(user=user, title='AI Project Brainstorm')
                ChatMessage.objects.create(chat=chat, role='ai', content='Hello! How can I help with your project today?')
                ChatMessage.objects.create(chat=chat, role='user', content='I want to build a unified orchestrator.')

        self.stdout.write(self.style.SUCCESS('Data seeding complete!'))
