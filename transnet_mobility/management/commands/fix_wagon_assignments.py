from django.core.management.base import BaseCommand
from transnet_mobility.models import WagonSpec, LocomotiveWagonAssignment


class Command(BaseCommand):
    help = 'Fix wagon assignment status - sync with actual LocomotiveWagonAssignment records'

    def handle(self, *args, **options):
        # Find wagons marked as assigned but have no assignment record
        assigned_wagons = WagonSpec.objects.filter(is_assigned=True)
        orphaned_count = 0
        
        for wagon in assigned_wagons:
            has_assignment = LocomotiveWagonAssignment.objects.filter(wagon=wagon).exists()
            if not has_assignment:
                # Orphaned - marked as assigned but no actual assignment
                wagon.is_assigned = False
                wagon.status = 'AVAILABLE'
                wagon.save(update_fields=['is_assigned', 'status'])
                orphaned_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Fixed orphaned wagon {wagon.wagon_number}: marked as available'
                    )
                )
        
        # Find wagons with assignments but not marked as assigned
        assignments = LocomotiveWagonAssignment.objects.select_related('wagon')
        unsynced_count = 0
        
        for assignment in assignments:
            wagon = assignment.wagon
            if not wagon.is_assigned or wagon.status != 'IN_USE':
                wagon.is_assigned = True
                wagon.status = 'IN_USE'
                wagon.save(update_fields=['is_assigned', 'status'])
                unsynced_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Fixed unsynced wagon {wagon.wagon_number}: marked as IN_USE'
                    )
                )
        
        if orphaned_count == 0 and unsynced_count == 0:
            self.stdout.write(self.style.SUCCESS('All wagon assignments are already synced'))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Fixed {orphaned_count} orphaned wagon(s) and {unsynced_count} unsynced wagon(s)'
                )
            )
