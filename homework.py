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
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # длина шага в метрах
    M_IN_KM: int = 1000  # для перевода значений из м в км

    def __init__(self,
                 action: int,  # основное действие во время тренировки
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
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

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return self.__init__(self.__class__.__name__,
                             self.duration,
                             self.get_distance(),
                             self.get_mean_speed(),
                             self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CONST_RUN_18: int = 18  # константы для расчета потраченных ккал
    CONST_RUN_20: int = 20
    HOUR_MIN: int = 60

    def get_spent_calories(self) -> float:
        running_calories = ((self.CONST_RUN_18 * self.get_mean_speed()
                             - self.CONST_RUN_20) * self.weight / self.M_IN_KM
                            * self.duration * self.HOUR_MIN)
        return running_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CONST_WALK_035: float = 0.035  # константы для расчета потраченных ккал
    CONST_WALK_029: float = 0.029
    HOUR_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        walking_calories = ((self.CONST_WALK_035 * self.weight
                             + (self.get_mean_speed() ** 2 // self.height)
                             * self.CONST_WALK_029 * self.weight)
                            * self.duration * self.HOUR_MIN)
        return walking_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # длина гребка при плавании в м
    CONST_SWIM_1_1: float = 1.1  # константы для расчета потраченных ккал
    CONST_SWIM_2: float = 2

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
        swimming_calories = ((self.get_mean_speed() + self.CONST_SWIM_1_1)
                             * self.CONST_SWIM_2 * self.weight)
        return swimming_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # словарь, в котором сопоставляются коды тренировок и классы

    training_dict: dict[str, Training] = dict(SWM=Swimming,
                                              RUN=Running,
                                              WLK=SportsWalking)

    if workout_type in training_dict:
        training_name = training_dict[workout_type](*data)
        return training_name


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
