# -*- coding: utf-8 -*-
import pytest
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
                ("социология", 61)  # Граничный случай - 61 не считается задолженностью
            ],
            "Сидоров Алексей Викторович": [
                ("физика", 45),  # Задолженность
                ("математика", 59),  # Задолженность
                ("информатика", 75)
            ],
            "Козлова Мария Сергеевна": [
                ("химия", 60),  # Граничный случай - 60 считается задолженностью
                ("биология", 82)
            ],
            "Никитин Дмитрий Олегович": [
                ("история", 85),
                ("философия", 90),
                ("экономика", 88)
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

    @pytest.fixture
    def sample_data_all_debts(self) -> DataType:
        """Фикстура с данными студентов, у всех есть задолженности"""
        return {
            "Студент 1": [("предмет1", 50)],
            "Студент 2": [("предмет2", 40)],
            "Студент 3": [("предмет3", 30)]
        }

    @pytest.fixture
    def empty_data(self) -> DataType:
        """Фикстура с пустыми данными"""
        return {}

    def test_init_debt_calculation(self, sample_data_with_debts):
        """Тест инициализации класса DebtCalculation"""
        calculator = DebtCalculation(sample_data_with_debts)
        assert calculator.data == sample_data_with_debts

    def test_count_students_with_debts_with_debts(self, sample_data_with_debts):
        """Тест подсчета студентов с задолженностями (когда они есть)"""
        calculator = DebtCalculation(sample_data_with_debts)
        count = calculator.count_students_with_debts()
        assert count == 2  # Сидоров и Козлова

    def test_count_students_with_debts_no_debts(self, sample_data_no_debts):
        """Тест подсчета студентов с задолженностями (когда их нет)"""
        calculator = DebtCalculation(sample_data_no_debts)
        count = calculator.count_students_with_debts()
        assert count == 0

    def test_count_students_with_debts_all_debts(self, sample_data_all_debts):
        """Тест подсчета студентов с задолженностями (когда у всех есть)"""
        calculator = DebtCalculation(sample_data_all_debts)
        count = calculator.count_students_with_debts()
        assert count == 3

    def test_count_students_with_debts_empty_data(self, empty_data):
        """Тест подсчета студентов с задолженностями (пустые данные)"""
        calculator = DebtCalculation(empty_data)
        count = calculator.count_students_with_debts()
        assert count == 0

    def test_has_debt_with_debt(self):
        """Тест проверки наличия задолженности (когда есть)"""
        calculator = DebtCalculation({})
        subjects = [("математика", 75), ("физика", 45), ("химия", 80)]
        assert calculator._has_debt(subjects) == True

    def test_has_debt_without_debt(self):
        """Тест проверки наличия задолженности (когда нет)"""
        calculator = DebtCalculation({})
        subjects = [("математика", 75), ("физика", 61), ("химия", 80)]
        assert calculator._has_debt(subjects) == False

    def test_has_debt_boundary_cases(self):
        """Тест граничных случаев проверки задолженности"""
        calculator = DebtCalculation({})

        # Граничный случай: 60 - задолженность
        assert calculator._has_debt([("предмет", 60)]) == True

        # Граничный случай: 61 - не задолженность
        assert calculator._has_debt([("предмет", 61)]) == False

        # Граничный случай: 0 - задолженность
        assert calculator._has_debt([("предмет", 0)]) == True

        # Граничный случай: 100 - не задолженность
        assert calculator._has_debt([("предмет", 100)]) == False

    def test_has_debt_empty_subjects(self):
        """Тест проверки наличия задолженности (пустой список предметов)"""
        calculator = DebtCalculation({})
        assert calculator._has_debt([]) == False

    def test_integration_with_json_reader(self, json_file_path_with_debts):
        """Интеграционный тест с JsonDataReader"""
        from src.JsonDataReader import JsonDataReader
        from src.DebtCalculation import DebtCalculation

        reader = JsonDataReader()
        students = reader.read(json_file_path_with_debts)

        calculator = DebtCalculation(students)
        debt_count = calculator.count_students_with_debts()

        assert debt_count == 1

    @pytest.fixture
    def json_file_path_with_debts(self, tmpdir):
        """Фикстура создает временный JSON файл с задолженностями"""
        import json
        
        data_with_debts = {
            "Иванов Иван": {
                "математика": 75,
                "физика": 80
            },
            "Сидоров Алексей": {
                "химия": 45,  # Задолженность
                "биология": 70
            },
            "Петрова Анна": {
                "история": 85,
                "литература": 90
            }
        }

        p = tmpdir.join("students_with_debts.json")
        with open(str(p), "w", encoding="utf-8") as f:
            json.dump(data_with_debts, f, ensure_ascii=False, indent=2)
        return str(p)