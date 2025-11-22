# -*- coding: utf-8 -*-
import pytest
import json
import tempfile
import os
from src.Types import DataType
from src.JsonDataReader import JsonDataReader


class TestJsonDataReader:
    
    @pytest.fixture
    def sample_data(self) -> DataType:
        """Фикстура с примерными данными для тестирования"""
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
    def valid_json_data(self) -> dict:
        """Фикстура с валидными JSON данными в требуемом формате"""
        return {
            "Иванов Иван Иванович": {
                "математика": 67,
                "литература": 100,
                "программирование": 91
            },
            "Петров Петр Петрович": {
                "математика": 78,
                "химия": 87,
                "социология": 61
            }
        }
    
    @pytest.fixture
    def json_file_path(self, valid_json_data, tmpdir) -> str:
        """Фикстура создает временный JSON файл и возвращает путь к нему"""
        p = tmpdir.join("students.json")
        p.write(json.dumps(valid_json_data, ensure_ascii=False, indent=2))
        return str(p)
    
    def test_read_valid_json_file(self, json_file_path, sample_data):
        """Тест чтения валидного JSON файла"""
        reader = JsonDataReader()
        result = reader.read(json_file_path)
        
        assert result == sample_data
        assert len(result) == 2
        assert "Иванов Иван Иванович" in result
        assert "Петров Петр Петрович" in result
    
    def test_read_student_data_structure(self, json_file_path):
        """Тест структуры данных студента"""
        reader = JsonDataReader()
        result = reader.read(json_file_path)
        
        # Проверяем данные первого студента
        ivanov_data = result["Иванов Иван Иванович"]
        assert len(ivanov_data) == 3
        assert isinstance(ivanov_data, list)
        
        # Проверяем что каждый предмет - это кортеж (название, оценка)
        for subject in ivanov_data:
            assert isinstance(subject, tuple)
            assert len(subject) == 2
            assert isinstance(subject[0], str)  # название предмета
            assert isinstance(subject[1], int)  # оценка
        
        # Проверяем конкретные предметы
        subjects_dict = dict(ivanov_data)
        assert subjects_dict["математика"] == 67
        assert subjects_dict["литература"] == 100
        assert subjects_dict["программирование"] == 91
    
    def test_read_nonexistent_file(self):
        """Тест обработки несуществующего файла"""
        reader = JsonDataReader()
        
        with pytest.raises(FileNotFoundError):
            reader.read("nonexistent_file.json")
    
    def test_read_invalid_json(self, tmpdir):
        """Тест обработки невалидного JSON"""
        p = tmpdir.join("invalid.json")
        p.write("{ invalid json content }")
        
        reader = JsonDataReader()
        
        with pytest.raises(json.JSONDecodeError):
            reader.read(str(p))
    
    def test_read_json_with_list_structure(self, tmpdir):
        """Тест обработки JSON с неправильной структурой (список вместо словаря)"""
        invalid_data = [
            {
                "name": "Студент",
                "subjects": {"математика": 90}
            }
        ]
        
        p = tmpdir.join("list_structure.json")
        p.write(json.dumps(invalid_data, ensure_ascii=False, indent=2))
        
        reader = JsonDataReader()
        
        with pytest.raises(ValueError, match="JSON должен быть объектом"):
            reader.read(str(p))
    
    def test_read_json_with_invalid_score_type(self, tmpdir):
        """Тест обработки JSON с неверным типом оценки"""
        invalid_data = {
            "Иванов Иван": {
                "математика": "сто"  # Строка вместо числа
            }
        }
        
        p = tmpdir.join("invalid_score.json")
        p.write(json.dumps(invalid_data, ensure_ascii=False, indent=2))
        
        reader = JsonDataReader()
        
        with pytest.raises(ValueError, match="Оценка должна быть числом"):
            reader.read(str(p))
    
    def test_read_json_with_invalid_subject_type(self, tmpdir):
        """Тест обработки JSON с неверным типом предметов"""
        invalid_data = {
            "Иванов Иван": [
                {"математика": 90}  # Список вместо словаря
            ]
        }
        
        p = tmpdir.join("invalid_subjects.json")
        p.write(json.dumps(invalid_data, ensure_ascii=False, indent=2))
        
        reader = JsonDataReader()
        
        with pytest.raises(ValueError, match="Предметы для студента"):
            reader.read(str(p))
    
    def test_read_empty_json(self, tmpdir):
        """Тест чтения пустого JSON файла"""
        p = tmpdir.join("empty.json")
        p.write("{}")
        
        reader = JsonDataReader()
        result = reader.read(str(p))
        
        assert result == {}
    
    def test_read_single_student(self, tmpdir):
        """Тест чтения JSON с одним студентом"""
        single_student_data = {
            "Сидоров Алексей": {
                "физика": 95,
                "математика": 88
            }
        }
        
        p = tmpdir.join("single_student.json")
        p.write(json.dumps(single_student_data, ensure_ascii=False, indent=2))
        
        reader = JsonDataReader()
        result = reader.read(str(p))
        
        assert len(result) == 1
        assert "Сидоров Алексей" in result
        assert len(result["Сидоров Алексей"]) == 2
        assert ("физика", 95) in result["Сидоров Алексей"]
        assert ("математика", 88) in result["Сидоров Алексей"]
    
    def test_read_json_with_special_characters(self, tmpdir):
        """Тест чтения JSON с специальными символами в именах"""
        special_chars_data = {
            "Иванов-Петров Иван Иванович": {
                "C++ программирование": 85,
                "Web-разработка": 90,
                "SQL/Базы данных": 78
            }
        }
        
        p = tmpdir.join("special_chars.json")
        p.write(json.dumps(special_chars_data, ensure_ascii=False, indent=2))
        
        reader = JsonDataReader()
        result = reader.read(str(p))
        
        assert "Иванов-Петров Иван Иванович" in result
        subjects_dict = dict(result["Иванов-Петров Иван Иванович"])
        assert subjects_dict["C++ программирование"] == 85
        assert subjects_dict["Web-разработка"] == 90
        assert subjects_dict["SQL/Базы данных"] == 78
    
    def test_read_json_with_float_scores(self, tmpdir):
        """Тест чтения JSON с дробными оценками"""
        float_scores_data = {
            "Петров Петр": {
                "математика": 85.5,
                "физика": 90.0,
                "химия": 78.7
            }
        }
        
        p = tmpdir.join("float_scores.json")
        p.write(json.dumps(float_scores_data, ensure_ascii=False, indent=2))
        
        reader = JsonDataReader()
        result = reader.read(str(p))
        
        subjects = result["Петров Петр"]
        assert any(subject[0] == "математика" and subject[1] == 85.5 for subject in subjects)
        assert any(subject[0] == "физика" and subject[1] == 90.0 for subject in subjects)
    
    def test_integration_with_calc_rating(self, json_file_path):
        """Интеграционный тест с CalcRating"""
        reader = JsonDataReader()
        students = reader.read(json_file_path)
        
        from src.CalcRating import CalcRating
        rating_calculator = CalcRating(students)
        ratings = rating_calculator.calc()
        
        # Проверяем что рейтинги рассчитаны корректно
        assert "Иванов Иван Иванович" in ratings
        assert "Петров Петр Петрович" in ratings
        
        # Проверяем расчет среднего рейтинга
        ivanov_avg = ratings["Иванов Иван Иванович"]
        expected_ivanov_avg = (67 + 100 + 91) / 3
        assert ivanov_avg == pytest.approx(expected_ivanov_avg, 0.001)
        
        petrov_avg = ratings["Петров Петр Петрович"] 
        expected_petrov_avg = (78 + 87 + 61) / 3
        assert petrov_avg == pytest.approx(expected_petrov_avg, 0.001)
    
    def test_file_encoding_handling(self, tmpdir):
        """Тест обработки разных кодировок файла"""
        unicode_data = {
            "Ковальчук Анна Михайловна": {
                "математика": 95,
                "русский язык": 88,
                "английский язык": 92
            }
        }
        
        p = tmpdir.join("unicode.json")
        # Явно указываем UTF-8 кодировку при записи
        with open(str(p), 'w', encoding='utf-8') as f:
            json.dump(unicode_data, f, ensure_ascii=False, indent=2)
        
        reader = JsonDataReader()
        result = reader.read(str(p))
        
        assert "Ковальчук Анна Михайловна" in result
        assert any("русский язык" in subject for subject in result["Ковальчук Анна Михайловна"])