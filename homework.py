from abc import abstractmethod
from typing import Type, List


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Необходимо переопределить метод")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CONST_RUN_MULTIPLIER: int = 18
    CONST_RUN_DEDUCTIBLE: int = 20

    def get_spent_calories(self) -> float:
        running_calories = ((self.CONST_RUN_MULTIPLIER * self.get_mean_speed()
                             - self.CONST_RUN_DEDUCTIBLE) * self.weight
                            / self.M_IN_KM
                            * self.duration * self.HOUR_MIN)
        return running_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CONST_WALK_MULTIPLIER_X: float = 0.035
    CONST_WALK_MULTIPLIER_Y: float = 0.029
    HOUR_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        walking_calories = ((self.CONST_WALK_MULTIPLIER_X * self.weight
                             + (self.get_mean_speed() ** 2 // self.height)
                             * self.CONST_WALK_MULTIPLIER_Y * self.weight)
                            * self.duration * self.HOUR_MIN)
        return walking_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CONST_SWIM_TERM: float = 1.1
    CONST_SWIM_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        swimming_speed = (self.length_pool * self.count_pool
                          / self.M_IN_KM / self.duration)
        return swimming_speed

    def get_spent_calories(self) -> float:
        swimming_calories = ((self.get_mean_speed() + self.CONST_SWIM_TERM)
                             * self.CONST_SWIM_MULTIPLIER * self.weight)
        return swimming_calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_vocabulary: dict[str, Type[Training]] = dict(SWM=Swimming,
                                                          RUN=Running,
                                                          WLK=SportsWalking)

    if workout_type in training_vocabulary:
        training_name = training_vocabulary[workout_type](*data)
        return training_name
    else:
        raise ValueError("Введено неверное значение")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
