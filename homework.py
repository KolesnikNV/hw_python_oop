from dataclasses import dataclass
from typing import ClassVar, List, Type, Dict
from typing_extensions import Final
from abc import abstractmethod


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE = (
        "Тип тренировки: {};"
        " Длительность: {:.3f} ч.;"
        " Дистанция: {:.3f} км;"
        " Ср. скорость: {:.3f} км/ч;"
        " Потрачено ккал: {:.3f}."
    )

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return self.MESSAGE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories,
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: Final = 1000
    LEN_STEP: ClassVar = 0.65
    MIN_IN_H: Final = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        training_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return training_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "Определите get_spent_calories в дочернем классе"
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar = 1.79

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )

        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: ClassVar = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar = 0.029
    KMH_IN_MSEC: ClassVar = 0.278
    CM_IN_M: Final = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (
                    (super().get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_SHIFT: ClassVar = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar = 2
    LEN_STEP: ClassVar = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )
        return calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_training_cls_map: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    if workout_type not in workout_type_training_cls_map:
        raise ValueError(
            f"Тренировка - {workout_type} не найдена. Попробуйте снова"
        )
    return workout_type_training_cls_map[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
