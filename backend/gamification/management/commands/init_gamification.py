from django.core.management.base import BaseCommand
from gamification.models import Category, Achievement, GamificationConfig, WebhookConfig
from gamification.signals import initialize_default_achievements, initialize_default_config


class Command(BaseCommand):
    help = 'Initialize default gamification data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing gamification data...'))
        
        # Default Categories
        categories_data = [
            {
                'name': 'classroom',
                'display_name': 'Classroom Team',
                'description': 'Educational teams and academic projects',
                'icon': '📚',
                'color': '#3B82F6'
            },
            {
                'name': 'software',
                'display_name': 'Software Development Team',
                'description': 'Software development and engineering teams',
                'icon': '💻',
                'color': '#10B981'
            },
            {
                'name': 'sales',
                'display_name': 'Sales Team',
                'description': 'Sales and business development teams',
                'icon': '💼',
                'color': '#F59E0B'
            }
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.display_name}')
            else:
                self.stdout.write(f'Category already exists: {category.display_name}')
        
        self.stdout.write('Creating default achievements...')
        initialize_default_achievements()
        
        self.stdout.write('Creating default configuration...')
        initialize_default_config()
        
        webhook_configs = [
            {
                'name': 'Discord Webhook',
                'platform': 'discord',
                'webhook_url': 'https://discord.com/api/webhooks/1393539491607740476/1C4OpEHJUISP_rIP98M6gDp-cZpBkkHERwpeeV1izx_0rey8IS4pvzff7DWA0XpcE_kg',
                'team': None
            },
            {
                'name': 'Microsoft Teams Webhook',
                'platform': 'teams',
                'webhook_url': 'https://mseufeduph.webhook.office.com/webhookb2/1d1a0208-f69a-47ed-9c1b-8c29c5fc9769@ddedb3cc-596d-482b-8e8c-6cc149a7a7b7/IncomingWebhook/09b5955c636a46688922a4e106304fd9/d8352f48-e96e-4321-800f-f998f9af400a/V21F7JNsmKeqN21d_HSU9mFN4tJ8jkpGlYB4mL892I1P01',
                'team': None
            }
        ]
        
        for webhook_data in webhook_configs:
            webhook, created = WebhookConfig.objects.get_or_create(
                name=webhook_data['name'],
                defaults=webhook_data
            )
            if created:
                self.stdout.write(f'Created webhook: {webhook.name}')
            else:
                self.stdout.write(f'Webhook already exists: {webhook.name}')
        
        self.stdout.write(self.style.SUCCESS('Gamification initialization complete!'))
        
        # Display summary
        self.stdout.write('\n=== Summary ===')
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Achievements: {Achievement.objects.count()}')
        self.stdout.write(f'Configurations: {GamificationConfig.objects.count()}')
        self.stdout.write(f'Webhooks: {WebhookConfig.objects.count()}')
        
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Create teams: python manage.py shell')
        self.stdout.write('2. Assign projects to categories')
        self.stdout.write('3. Configure webhook teams')
        self.stdout.write('4. Test task completion for points and achievements')
