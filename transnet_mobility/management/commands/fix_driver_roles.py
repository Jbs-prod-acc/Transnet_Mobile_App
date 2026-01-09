from django.core.management.base import BaseCommand
from transnet_mobility.models import CustomUser


class Command(BaseCommand):
    help = 'Fix driver roles - ensure all users with account_type=DRIVER also have role=DRIVER'

    def handle(self, *args, **options):
        # Find all drivers with incorrect role
        drivers_with_wrong_role = CustomUser.objects.filter(
            account_type='DRIVER'
        ).exclude(role='DRIVER')
        
        count = drivers_with_wrong_role.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('All drivers already have correct role=DRIVER'))
            return
        
        self.stdout.write(f'Found {count} driver(s) with incorrect role')
        
        # Update them
        for driver in drivers_with_wrong_role:
            old_role = driver.role
            driver.role = 'DRIVER'
            driver.save(update_fields=['role'])
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated {driver.email}: role changed from {old_role} to DRIVER'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {count} driver(s) to role=DRIVER')
        )
