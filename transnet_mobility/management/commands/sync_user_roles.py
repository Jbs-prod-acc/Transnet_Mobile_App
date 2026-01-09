from django.core.management.base import BaseCommand
from transnet_mobility.models import CustomUser


class Command(BaseCommand):
    help = 'Sync all user roles with their account_type'

    def handle(self, *args, **options):
        # Find all users where role doesn't match account_type
        all_users = CustomUser.objects.all()
        
        updated = 0
        for user in all_users:
            if user.account_type and user.account_type != 'OTHER':
                if user.role != user.account_type:
                    old_role = user.role
                    user.role = user.account_type
                    user.save(update_fields=['role'])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated {user.email}: role changed from {old_role} to {user.account_type}'
                        )
                    )
                    updated += 1
        
        if updated == 0:
            self.stdout.write(self.style.SUCCESS('All user roles are already synced with account_type'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully synced {updated} user role(s) with account_type')
            )
