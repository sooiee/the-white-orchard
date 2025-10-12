from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from .models import TimeSlot, Reservation, MenuItem

class TimeSlotModelTest(TestCase):
    """Test TimeSlot model"""
    
    def test_timeslot_creation(self):
        slot = TimeSlot.objects.create(time='13:00', is_active=True)
        self.assertEqual(slot.time, '13:00')
        self.assertTrue(slot.is_active)


class ReservationModelTest(TestCase):
    """Test Reservation model"""
    
    def setUp(self):
        self.time_slot = TimeSlot.objects.create(time='13:00')
        self.tomorrow = date.today() + timedelta(days=1)
    
    def test_reservation_creation(self):
        res = Reservation.objects.create(
            customer_name='Test User',
            customer_email='test@test.com',
            customer_phone='123456789',
            date=self.tomorrow,
            time_slot=self.time_slot,
            number_of_guests=2
        )
        self.assertEqual(res.customer_name, 'Test User')
        self.assertEqual(res.status, 'pending')
    
    def test_reservation_string_representation(self):
        res = Reservation.objects.create(
            customer_name='Jane Doe',
            customer_email='jane@test.com',
            customer_phone='123456789',
            date=self.tomorrow,
            time_slot=self.time_slot,
            number_of_guests=4
        )
        self.assertIn('Jane Doe', str(res))


class MenuItemModelTest(TestCase):
    """Test MenuItem model"""
    
    def test_menu_item_creation(self):
        item = MenuItem.objects.create(
            name='Scone',
            description='Fresh scone with jam',
            category='Pastries',
            is_available=True
        )
        self.assertEqual(item.name, 'Scone')
        self.assertTrue(item.is_available)


class ViewTest(TestCase):
    """Test views load correctly"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The White Orchard')
    
    def test_menu_page_loads(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_page_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_reservation_page_loads(self):
        response = self.client.get(reverse('create_reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book Your Afternoon Tea')


class FormTest(TestCase):
    """Test reservation form validation"""
    
    def setUp(self):
        self.time_slot = TimeSlot.objects.create(time='13:00')
        self.tomorrow = date.today() + timedelta(days=1)
        self.yesterday = date.today() - timedelta(days=1)
    
    def test_valid_reservation_creation(self):
        form_data = {
            'customer_name': 'Test User',
            'customer_email': 'test@example.com',
            'customer_phone': '07123456789',
            'date': self.tomorrow,
            'time_slot': self.time_slot.pk,
            'number_of_guests': 2,
        }
        response = self.client.post(reverse('create_reservation'), data=form_data)
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        # Check reservation was created
        self.assertEqual(Reservation.objects.count(), 1)
    
    def test_past_date_validation(self):
        form_data = {
            'customer_name': 'Test User',
            'customer_email': 'test@example.com',
            'customer_phone': '07123456789',
            'date': self.yesterday,
            'time_slot': self.time_slot.pk,
            'number_of_guests': 2,
        }
        response = self.client.post(reverse('create_reservation'), data=form_data)
        # Should not redirect (stays on form page)
        self.assertEqual(response.status_code, 200)
        # Should show error
        self.assertContains(response, 'Cannot book a date in the past')