"""
Demo data seed for PharmaTrack.

Creates:
  - 1 demo pharmacy (Afya Bora Pharmacy, Nairobi)
  - 1 demo user  (username: demo / password: demo1234, role: owner)
  - 60 medicines: 43 healthy, 10 low-stock, 5 expiring in <30 days, 2 expired
  - 30 days of stock-movement history (IN / OUT records per medicine)

Usage:
  python manage.py seed_demo            # skip if demo data already exists
  python manage.py seed_demo --clear    # wipe existing demo data first
"""

import random
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import Pharmacy
from apps.inventory.models import Medicine, StockMovement

User = get_user_model()

DEMO_USERNAME = 'demo'
DEMO_PASSWORD = 'demo1234'
DEMO_PHARMACY_NAME = 'Afya Bora Pharmacy'

# (name, dosage, generic_name, category, unit, manufacturer, buying_price, selling_price, min_qty)
CATALOGUE = [
    # Antibiotics
    ('Amoxicillin',           '500mg',        'Amoxicillin trihydrate',            'Antibiotics',           'caps',    'Dawa Ltd',       8,   15,  20),
    ('Azithromycin',          '250mg',        'Azithromycin dihydrate',            'Antibiotics',           'tabs',    'Cosmos Ltd',    25,   45,  15),
    ('Ciprofloxacin',         '500mg',        'Ciprofloxacin HCl',                 'Antibiotics',           'tabs',    'Dawa Ltd',      18,   30,  20),
    ('Metronidazole',         '400mg',        'Metronidazole',                     'Antibiotics',           'tabs',    'Regal Pharm',    5,   10,  25),
    ('Doxycycline',           '100mg',        'Doxycycline hyclate',               'Antibiotics',           'caps',    'Cosmos Ltd',    12,   22,  20),
    ('Co-trimoxazole',        '480mg',        'Sulfamethoxazole + Trimethoprim',   'Antibiotics',           'tabs',    'Dawa Ltd',       4,    8,  30),
    ('Erythromycin',          '250mg',        'Erythromycin stearate',             'Antibiotics',           'tabs',    'Regal Pharm',   10,   18,  20),
    # Analgesics
    ('Paracetamol',           '500mg',        'Acetaminophen',                     'Analgesics',            'tabs',    'Cosmos Ltd',     1,    3,  50),
    ('Ibuprofen',             '400mg',        'Ibuprofen',                         'Analgesics',            'tabs',    'Dawa Ltd',       5,   10,  30),
    ('Diclofenac',            '50mg',         'Diclofenac sodium',                 'Analgesics',            'tabs',    'Regal Pharm',    8,   15,  25),
    ('Aspirin',               '300mg',        'Acetylsalicylic acid',              'Analgesics',            'tabs',    'Cosmos Ltd',     3,    6,  30),
    ('Tramadol',              '50mg',         'Tramadol HCl',                      'Analgesics',            'caps',    'Dawa Ltd',      20,   35,  15),
    # Antihypertensives
    ('Amlodipine',            '5mg',          'Amlodipine besylate',               'Antihypertensives',     'tabs',    'Cosmos Ltd',    12,   22,  20),
    ('Lisinopril',            '10mg',         'Lisinopril',                        'Antihypertensives',     'tabs',    'Dawa Ltd',      15,   28,  20),
    ('Atenolol',              '50mg',         'Atenolol',                          'Antihypertensives',     'tabs',    'Regal Pharm',    8,   15,  20),
    ('Nifedipine',            '10mg',         'Nifedipine',                        'Antihypertensives',     'tabs',    'Cosmos Ltd',    10,   18,  20),
    ('Hydrochlorothiazide',   '25mg',         'Hydrochlorothiazide',               'Antihypertensives',     'tabs',    'Dawa Ltd',       6,   12,  25),
    ('Losartan',              '50mg',         'Losartan potassium',                'Antihypertensives',     'tabs',    'Regal Pharm',   20,   35,  15),
    # Antidiabetics
    ('Metformin',             '500mg',        'Metformin HCl',                     'Antidiabetics',         'tabs',    'Dawa Ltd',       8,   15,  25),
    ('Glibenclamide',         '5mg',          'Glibenclamide',                     'Antidiabetics',         'tabs',    'Cosmos Ltd',     6,   12,  20),
    ('Insulin Actrapid',      '100IU/ml',     'Human Insulin',                     'Antidiabetics',         'vial',    'Novo Nordisk', 350,  500,   5),
    # Antimalarials
    ('Artemether/Lumefantrine', '20/120mg',   'Artemether + Lumefantrine',         'Antimalarials',         'tabs',    'Dawa Ltd',      80,  150,  10),
    ('Quinine Sulphate',      '300mg',        'Quinine sulphate',                  'Antimalarials',         'tabs',    'Cosmos Ltd',    20,   38,  15),
    # Antiparasitics
    ('Albendazole',           '400mg',        'Albendazole',                       'Antiparasitics',        'tabs',    'Regal Pharm',   15,   28,  20),
    ('Mebendazole',           '100mg',        'Mebendazole',                       'Antiparasitics',        'tabs',    'Dawa Ltd',       8,   15,  20),
    ('Permethrin Cream',      '5%',           'Permethrin',                        'Antiparasitics',        'tube',    'Cosmos Ltd',   120,  200,  10),
    # Vitamins & Supplements
    ('Vitamin C',             '500mg',        'Ascorbic acid',                     'Vitamins & Supplements','tabs',    'Regal Pharm',    3,    6,  40),
    ('Zinc Sulphate',         '20mg',         'Zinc sulphate',                     'Vitamins & Supplements','tabs',    'Dawa Ltd',       4,    8,  30),
    ('Folic Acid',            '5mg',          'Folic acid',                        'Vitamins & Supplements','tabs',    'Cosmos Ltd',     2,    5,  40),
    ('Ferrous Sulphate',      '200mg',        'Ferrous sulphate',                  'Vitamins & Supplements','tabs',    'Regal Pharm',    3,    6,  35),
    ('Multivitamin',          '',             'Multivitamin complex',              'Vitamins & Supplements','tabs',    'Dawa Ltd',       5,   10,  30),
    # Respiratory
    ('Salbutamol Inhaler',    '100mcg',       'Salbutamol sulphate',               'Respiratory',           'inhaler', 'GSK',          280,  450,   8),
    ('Prednisolone',          '5mg',          'Prednisolone',                      'Respiratory',           'tabs',    'Cosmos Ltd',     5,   10,  20),
    ('Cetirizine',            '10mg',         'Cetirizine HCl',                    'Respiratory',           'tabs',    'Regal Pharm',    6,   12,  25),
    ('Loratadine',            '10mg',         'Loratadine',                        'Respiratory',           'tabs',    'Dawa Ltd',       7,   13,  25),
    ('Bromhexine',            '8mg',          'Bromhexine HCl',                    'Respiratory',           'tabs',    'Cosmos Ltd',     5,   10,  20),
    # Gastrointestinal
    ('Omeprazole',            '20mg',         'Omeprazole',                        'Gastrointestinal',      'caps',    'Dawa Ltd',      15,   28,  20),
    ('Oral Rehydration Salts','',             'ORS',                               'Gastrointestinal',      'sachet',  'Regal Pharm',   10,   20,  30),
    ('Loperamide',            '2mg',          'Loperamide HCl',                    'Gastrointestinal',      'caps',    'Dawa Ltd',       8,   15,  20),
    ('Domperidone',           '10mg',         'Domperidone',                       'Gastrointestinal',      'tabs',    'Cosmos Ltd',    10,   18,  20),
    ('Lactulose Syrup',       '3.35g/5ml',    'Lactulose',                         'Gastrointestinal',      'bottle',  'Regal Pharm',   80,  140,   8),
    # Antifungals
    ('Fluconazole',           '150mg',        'Fluconazole',                       'Antifungals',           'caps',    'Regal Pharm',   25,   45,  15),
    ('Clotrimazole Cream',    '1%',           'Clotrimazole',                      'Antifungals',           'tube',    'Dawa Ltd',      80,  140,  10),
    ('Griseofulvin',          '500mg',        'Griseofulvin',                      'Antifungals',           'tabs',    'Cosmos Ltd',    20,   35,  15),
    # Eye & Ear
    ('Chloramphenicol Eye Drops', '0.5%',     'Chloramphenicol',                   'Eye & Ear',             'bottle',  'Dawa Ltd',      90,  160,   8),
    ('Gentamicin Eye Drops',  '0.3%',         'Gentamicin sulphate',               'Eye & Ear',             'bottle',  'Cosmos Ltd',   100,  180,   8),
    # Contraceptives
    ('Postinor-2',            '0.75mg',       'Levonorgestrel',                    'Contraceptives',        'tabs',    'Gedeon Richter',120, 200,  10),
    ('Microgynon',            '30mcg/150mcg', 'Ethinylestradiol + Levonorgestrel', 'Contraceptives',        'tabs',    'Bayer',         80,  140,  12),
    # Dermatology
    ('Hydrocortisone Cream',  '1%',           'Hydrocortisone acetate',            'Dermatology',           'tube',    'Regal Pharm',   60,  110,  10),
    ('Betamethasone Cream',   '0.1%',         'Betamethasone valerate',            'Dermatology',           'tube',    'Cosmos Ltd',    80,  145,   8),
    ('Calamine Lotion',       '',             'Calamine',                          'Dermatology',           'bottle',  'Dawa Ltd',      70,  120,  10),
    # Cardiovascular
    ('Digoxin',               '0.25mg',       'Digoxin',                           'Cardiovascular',        'tabs',    'Cosmos Ltd',    15,   28,  15),
    ('Furosemide',            '40mg',         'Furosemide',                        'Cardiovascular',        'tabs',    'Dawa Ltd',       6,   12,  20),
    ('Warfarin',              '5mg',          'Warfarin sodium',                   'Cardiovascular',        'tabs',    'Regal Pharm',   12,   22,  15),
    # Neurology / CNS
    ('Phenobarbitone',        '30mg',         'Phenobarbital',                     'Neurology',             'tabs',    'Dawa Ltd',       5,   10,  20),
    ('Carbamazepine',         '200mg',        'Carbamazepine',                     'Neurology',             'tabs',    'Cosmos Ltd',    12,   22,  15),
    ('Diazepam',              '5mg',          'Diazepam',                          'Neurology',             'tabs',    'Regal Pharm',    8,   15,  10),
    # Ophthalmology
    ('Timolol Eye Drops',     '0.5%',         'Timolol maleate',                   'Eye & Ear',             'bottle',  'Cosmos Ltd',   150,  260,   6),
    # Misc
    ('Normal Saline',         '0.9%',         'Sodium chloride',                   'IV Fluids',             'bottle',  'Regal Pharm',   80,  130,  10),
    ('Dextrose 5%',           '5%',           'Dextrose',                          'IV Fluids',             'bottle',  'Dawa Ltd',      85,  140,  10),
]


def batch_number(idx: int) -> str:
    today = date.today()
    return f"BN-{today.strftime('%Y%m')}-{idx:03d}"


class Command(BaseCommand):
    help = 'Seed demo pharmacy data for PharmaTrack'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Delete existing demo pharmacy and user before seeding',
        )

    def handle(self, *args, **options):
        random.seed(42)
        today = date.today()

        if options['clear']:
            deleted, _ = Pharmacy.objects.filter(name=DEMO_PHARMACY_NAME).delete()
            User.objects.filter(username=DEMO_USERNAME).delete()
            self.stdout.write(self.style.WARNING(f'Cleared existing demo data ({deleted} pharmacy records).'))

        # ── Pharmacy ──────────────────────────────────────────────────────
        pharmacy, created = Pharmacy.objects.get_or_create(
            name=DEMO_PHARMACY_NAME,
            defaults={
                'owner_name': 'Carol Gitonga',
                'phone': '+254712345678',
                'email': 'afyabora@example.co.ke',
                'location': 'Westlands, Nairobi',
                'plan': 'standard',
            },
        )
        if not created:
            self.stdout.write(self.style.WARNING('Demo pharmacy already exists — skipping (use --clear to reset).'))
            return

        # ── User ──────────────────────────────────────────────────────────
        user = User.objects.create_user(
            username=DEMO_USERNAME,
            password=DEMO_PASSWORD,
            first_name='Carol',
            last_name='Gitonga',
            email='demo@afyabora.co.ke',
            pharmacy=pharmacy,
            role='owner',
        )

        # ── Medicines ─────────────────────────────────────────────────────
        # Assign expiry / quantity profiles to each catalogue entry.
        # Slots: indices 0-42 → healthy, 43-52 → low stock,
        #        53-57 → expiring soon (<30 d), 58-59 → expired.
        medicines = []
        for idx, row in enumerate(CATALOGUE):
            name, dosage, generic_name, category, unit, manufacturer, bp, sp, min_qty = row

            if idx < 43:                          # healthy
                qty = random.randint(min_qty + 15, min_qty + 120)
                expiry = today + timedelta(days=random.randint(180, 730))
            elif idx < 53:                        # low stock (10)
                qty = random.randint(1, min_qty)
                expiry = today + timedelta(days=random.randint(180, 365))
            elif idx < 58:                        # expiring soon (5)
                qty = random.randint(min_qty + 5, min_qty + 40)
                expiry = today + timedelta(days=random.randint(5, 28))
            else:                                 # expired (2)
                qty = random.randint(min_qty + 2, min_qty + 20)
                expiry = today - timedelta(days=random.randint(10, 90))

            medicines.append(Medicine(
                pharmacy=pharmacy,
                name=name,
                dosage=dosage,
                generic_name=generic_name,
                category=category,
                unit=unit,
                manufacturer=manufacturer,
                batch_number=batch_number(idx + 1),
                quantity=qty,
                minimum_quantity=min_qty,
                buying_price=Decimal(str(bp)),
                selling_price=Decimal(str(sp)),
                expiry_date=expiry,
                supplier=f'{manufacturer} Distributors Kenya',
                is_active=True,
            ))

        Medicine.objects.bulk_create(medicines)
        created_medicines = list(Medicine.objects.filter(pharmacy=pharmacy).order_by('id'))

        # ── Stock Movements (30 days of history) ─────────────────────────
        movements_to_create = []
        for med in created_medicines:
            # 2-4 IN movements spread across the last 30 days
            for _ in range(random.randint(2, 4)):
                movements_to_create.append((
                    StockMovement(
                        pharmacy=pharmacy,
                        medicine=med,
                        movement_type='IN',
                        quantity=random.randint(10, 100),
                        notes='Routine restocking',
                        performed_by=user,
                    ),
                    random.randint(1, 30),   # days ago
                ))
            # 1-3 OUT movements
            for _ in range(random.randint(1, 3)):
                movements_to_create.append((
                    StockMovement(
                        pharmacy=pharmacy,
                        medicine=med,
                        movement_type='OUT',
                        quantity=random.randint(1, 20),
                        notes='Dispensed to patient',
                        performed_by=user,
                    ),
                    random.randint(1, 30),
                ))

        random.shuffle(movements_to_create)

        # Bulk create then back-date via queryset update (bypasses auto_now_add)
        objs = StockMovement.objects.bulk_create([m for m, _ in movements_to_create])
        now = timezone.now()
        for obj, days_ago in zip(objs, [d for _, d in movements_to_create]):
            StockMovement.objects.filter(pk=obj.pk).update(
                date=now - timedelta(days=days_ago, hours=random.randint(0, 23))
            )

        # ── Summary ───────────────────────────────────────────────────────
        total = len(created_medicines)
        low  = sum(1 for m in created_medicines if m.is_low_stock)
        exp_soon = sum(1 for m in created_medicines if m.is_expiring_soon)
        expired  = sum(1 for m in created_medicines if m.is_expired)
        mvt_count = len(movements_to_create)

        self.stdout.write(self.style.SUCCESS(
            f'\nDemo data seeded successfully\n'
            f'  Pharmacy : {DEMO_PHARMACY_NAME}\n'
            f'  Login    : username={DEMO_USERNAME}  password={DEMO_PASSWORD}\n'
            f'  Medicines: {total} total  |  {low} low stock  |  {exp_soon} expiring soon  |  {expired} expired\n'
            f'  Movements: {mvt_count} records over the last 30 days\n'
        ))
