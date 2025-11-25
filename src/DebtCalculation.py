# -*- coding: utf-8 -*-
from .Types import DataType


class DebtCalculation:
    """Класс для расчета количества студентов с академическими задолженностями"""

    def __init__(self, data: DataType) -> None:
        """
        Инициализация класса с данными студентов

        Args:
            data: данные о студентах и их оценках в формате DataType
        """
        self.data = data

    def count_students_with_debts(self) -> int:
        """
        Подсчитывает количество студентов с академическими задолженностями

        Returns:
            int: количество студентов с хотя бы одной оценкой < 61
        """
        count = 0
        for student, subjects in self.data.items():
            if self._has_debt(subjects):
                count += 1
        return count

    def _has_debt(self, subjects: list) -> bool:
        """
        Проверяет, есть ли у студента академические задолженности

        Args:
            subjects: список предметов студента

        Returns:
            bool: True если есть хотя бы одна оценка < 61, иначе False
        """
        for subject, score in subjects:
            if score < 61:
                return True
        return False