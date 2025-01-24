from django.core.management.base import BaseCommand
from core.models import MonthlyMenu, WeeklySchedule
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Create 10 sample Monthly Menus with associated Weekly Schedules'

    def handle(self, *args, **kwargs):
        # Sample data for menus
        menu_names = [
            "Healthy Meals Package",
            "Family Feast",
            "Veggie Delight",
            "Protein Power",
            "Budget Bites",
            "Luxury Experience",
            "Quick Meals",
            "Gourmet Special",
            "Comfort Foods",
            "Ultimate Feast"
        ]

        for i, name in enumerate(menu_names):
            # Generate random values for the MonthlyMenu fields
            description = f"This is a delicious and healthy {name}. Perfect for everyone!"
            price = random.randint(50, 200)  # Random price between 50 and 200
            persons = random.randint(1, 6)  # Random number of persons (1 to 6)
            days = random.randint(1, 7)  # Random days (1 to 7)
            meals = random.randint(3, 7)  # Random meals per day
            popular = False
            nav_link = random.choice([True, False])  # Randomly choose if it should have a nav link
            slug = slugify(name)  # Generate a slug from the name

            # Create the MonthlyMenu instance
            menu = MonthlyMenu.objects.create(
                name=name,
                desc=description,
                breif_desc=f"{name[:50]}",
                price=price,
                persons=persons,
                days=days,
                meals=meals,
                popular=popular,
                nav_link=nav_link,
                slug=slug
            )

            # Create a WeeklySchedule for the menu
            week_items = ['Chicken', 'Fish', 'Salad', 'Pasta', 'Pizza', 'Rice', 'Soup', 'Veggies', 'Beef', 'Tofu']

            schedule = WeeklySchedule.objects.create(menu=menu)

            # Assign random items for each week and day
            for week in range(1, 5):  # 4 weeks
                for day in range(1, 8):  # 7 days
                    day_field = f'week{week}_{"mon tue wed thu fri sat sun".split()[day-1]}_item'
                    setattr(schedule, day_field, random.choice(week_items))
            
            # Save the weekly schedule
            schedule.save()

            # Output the success message for each menu created
            self.stdout.write(self.style.SUCCESS(f'Successfully created menu: {menu.name} with Weekly Schedule'))
