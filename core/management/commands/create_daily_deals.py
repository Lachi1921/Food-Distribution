from django.core.management.base import BaseCommand
from core.models import Deal
from django.utils.text import slugify
import random


class Command(BaseCommand):
    help = 'Create 10 Daily Deals with sample data'

    def handle(self, *args, **kwargs):
        for i in range(10):
            name = f"Deal {i + 1}"
            description = f"This is the description for Deal {i + 1}. A great deal at a great price!"
            price = random.randint(10, 100)
            frozen = random.choice([True, False])
            free_delivery = random.choice([True, False])

            slug = slugify(name)

            deal = Deal.objects.create(
                image='deals/kari-pakora_i1azpr_mcrVBas.webp',
                name=name,
                desc=description,
                price=price,
                frozen=frozen,
                free_delivery=free_delivery,
                slug=slug
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created deal: {deal.name}'))
