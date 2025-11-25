# -*- coding: utf-8 -*-
import pytest
import json
from src.Types import DataType
from src.DebtCalculation import DebtCalculation


class TestDebtCalculation:

    @pytest.fixture
    def sample_data_with_debts(self) -> DataType:
        """Фикстура с данными студентов, включая задолженности"""
        return {
            "Иванов Иван Иванович": [
                ("математика", 67),
                ("литература", 100),
                ("программирование", 91)
            ],
            "Петров Петр Петрович": [
                ("математика", 78),
                ("химия", 87),
                ("социология", 61)
            ],
            "Сидоров Алексей Викторович": [
                ("физика", 45),
                ("математика", 59),
                ("информатика", 75)
            ],
            "Козлова Мария Сергеевна": [
                ("химия", 60),
                ("биология", 82)
            ]
        }

    @pytest.fixture
    def sample_data_no_debts(self) -> DataType:
        """Фикстура с данными студентов без задолженностей"""
        return {
            "Иванов Иван Иванович": [
                ("математика", 67),
                ("литература", 100),
                ("программирование", 91)
            ],
            "Петров Петр Петрович": [
                ("математика", 78),
                ("химия", 87),
                ("социология", 61)
            ]
        }

    def test_count_students_with_debts_with_debts(
            self, sample_data_with_debts):
        """Тест подсчета студентов с задолженностями"""
        calculator = DebtCalculation(sample_data_with_debts)
        count = calculator.count_students_with_debts()
        assert count == 2

    def test_count_students_with_debts_no_debts(self, sample_data_no_debts):
        """Тест подсчета студентов с задолженностями"""
        calculator = DebtCalculation(sample_data_no_debts)
        count = calculator.count_students_with_debts()
        assert count == 0

    def test_has_debt_with_debt(self):
        """Тест проверки наличия задолженности (когда есть)"""
        calculator = DebtCalculation({})
        subjects = [("математика", 75), ("физика", 45), ("химия", 80)]
        assert calculator._has_debt(subjects) is True

    def test_has_debt_without_debt(self):
        """Тест проверки наличия задолженности (когда нет)"""
        calculator = DebtCalculation({})
        subjects = [("математика", 75), ("физика", 61), ("химия", 80)]
        assert calculator._has_debt(subjects) is False

    def test_integration_with_json_reader(self, tmpdir):
        """Интеграционный тест с JsonDataReader"""
        from src.JsonDataReader import JsonDataReader

        data_with_debts = {
            "Иванов Иван": {
                "математика": 75,
                "физика": 80
            },
            "Сидоров Алексей": {
                "химия": 45,
                "биология": 70
            }
        }

        p = tmpdir.join("students_with_debts.json")
        with open(str(p), "w", encoding="utf-8") as f:
            json.dump(data_with_debts, f, ensure_ascii=False, indent=2)

        reader = JsonDataReader()
        students = reader.read(str(p))

        calculator = DebtCalculation(students)
        debt_count = calculator.count_students_with_debts()

        assert debt_count == 1
