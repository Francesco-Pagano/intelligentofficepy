import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_quadrant_occupancy(self, mock_distance_sensor: Mock):
        system = IntelligentOffice()
        mock_distance_sensor.return_value = True
        occupied = system.check_quadrant_occupancy(system.INFRARED_PIN1)
        self.assertTrue(occupied)

    def test_check_quadrant_occupancy_raises_error(self):
        system = IntelligentOffice()
        self.assertRaises(IntelligentOfficeError, system.check_quadrant_occupancy, -1)

    @patch.object(SDL_DS3231, "read_datetime")
    @patch.object(IntelligentOffice, "change_servo_angle")
    def test_should_open_the_blinds(self, mock_servo: Mock, mock_time: Mock):
        system = IntelligentOffice()
        mock_time.return_value = datetime(2024, 11, 27, 8, 0)
        system.manage_blinds_based_on_time()
        mock_servo.assert_called_with(12)
        self.assertTrue(system.blinds_open)

    @patch.object(SDL_DS3231, "read_datetime")
    @patch.object(IntelligentOffice, "change_servo_angle")
    def test_should_open_the_blinds(self, mock_servo: Mock, mock_time: Mock):
        system = IntelligentOffice()
        mock_time.return_value = datetime(2024, 11, 27, 20, 0)
        system.manage_blinds_based_on_time()
        mock_servo.assert_called_with(2)
        self.assertFalse(system.blinds_open)

    @patch.object(SDL_DS3231, "read_datetime")
    @patch.object(IntelligentOffice, "change_servo_angle")
    def test_should_not_open_the_blinds_saturday(self, mock_servo: Mock, mock_time: Mock):
        system = IntelligentOffice()
        mock_time.return_value = datetime(2024, 11, 23, 8, 0)
        system.manage_blinds_based_on_time()
        mock_servo.assert_called_with(2)
        self.assertFalse(system.blinds_open)

    @patch.object(SDL_DS3231, "read_datetime")
    @patch.object(IntelligentOffice, "change_servo_angle")
    def test_should_not_open_the_blinds_saturday(self, mock_servo: Mock, mock_time: Mock):
        system = IntelligentOffice()
        mock_time.return_value = datetime(2024, 11, 24, 8, 0)
        system.manage_blinds_based_on_time()
        mock_servo.assert_called_with(2)
        self.assertFalse(system.blinds_open)
