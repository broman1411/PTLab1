# -*- coding: utf-8 -*-
import json
from typing import Any, Dict
from .Types import DataType
from .DataReader import DataReader


class JsonDataReader(DataReader):
    def read(self, path: str) -> DataType:
        """
        Читает данные из JSON файла в формате словаря и преобразует в DataType
        
        Ожидаемый формат JSON:
        {
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
        
        Args:
            path: путь к JSON файлу
            
        Returns:
            DataType: словарь с данными студентов и их оценок
            
        Raises:
            FileNotFoundError: если файл не найден
            json.JSONDecodeError: если файл содержит невалидный JSON
            ValueError: если структура JSON не соответствует ожидаемой
        """
        students: DataType = {}
        
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            self._validate_json_structure(data)
            students = self._convert_to_datatype(data)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {path} не найден")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Ошибка декодирования JSON: {e}", e.doc, e.pos)
        except ValueError as e:
            raise ValueError(f"Неверная структура JSON: {e}")
                
        return students
    
    def _validate_json_structure(self, data: Any) -> None:
        """
        Проверяет структуру JSON данных
        
        Args:
            data: загруженные JSON данные
            
        Raises:
            ValueError: если структура не соответствует ожидаемой
        """
        if not isinstance(data, dict):
            raise ValueError("JSON должен быть объектом (словарем)")
        
        for student_name, subjects in data.items():
            if not isinstance(student_name, str):
                raise ValueError(f"Имя студента должно быть строкой: {student_name}")
            
            if not isinstance(subjects, dict):
                raise ValueError(f"Предметы для студента {student_name} должны быть объектом")
            
            for subject_name, score in subjects.items():
                if not isinstance(subject_name, str):
                    raise ValueError(f"Название предмета должно быть строкой: {subject_name}")
                
                if not isinstance(score, (int, float)):
                    raise ValueError(f"Оценка должна быть числом: {score} для предмета {subject_name}")
    
    def _convert_to_datatype(self, data: Dict[str, Dict[str, int]]) -> DataType:
        """
        Конвертирует JSON данные в DataType
        
        Args:
            data: JSON данные в формате словаря
            
        Returns:
            DataType: конвертированные данные
        """
        students: DataType = {}
        
        for student_name, subjects_dict in data.items():
            subjects_list = []
            for subject_name, score in subjects_dict.items():
                subjects_list.append((subject_name, score))
            students[student_name] = subjects_list
            
        return students