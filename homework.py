from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    PHRASES_TO_RETURN: str = ('Тип тренировки: {0}; '
                              'Длительность: {1:.3f} ч.; '
                              'Дистанция: {2:.3f} км; '
                              'Ср. скорость: {3:.3f} км/ч; '
                              'Потрачено ккал: {4:.3f}.')

    def get_message(self):
        return self.PHRASES_TO_RETURN.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    H_IN_M: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.H_IN_M))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_ONE: float = 0.035
    CALORIES_WEIGHT_TWO: float = 0.029
    S_IN_M: int = 100
    KM_H_IN_M_H: float = round(1000 / 60 / 60, 3)

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_WEIGHT_ONE * self.weight
                + ((self.get_mean_speed() * self.KM_H_IN_M_H)
                 ** 2 / (self.height / self.S_IN_M))
                 * self.CALORIES_WEIGHT_TWO * self.weight)
                * (self.duration * self.H_IN_M))


class Swimming(Training):
    """Тренировка: плавание."""

    AVERAGE_SPEED_RATIO_1: float = 1.1
    AVERAGE_SPEED_RATIO_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.AVERAGE_SPEED_RATIO_1)
                * self.AVERAGE_SPEED_RATIO_2 * self.weight * self.duration)


TYPES_TRAINING: dict[str, type[Training]] = {'SWM': Swimming,
                                             'RUN': Running,
                                             'WLK': SportsWalking
                                             }


def read_package(workout_type: str, data: int) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TYPES_TRAINING:
        raise ValueError('Не корректный тип тренировки в переменной '
                         '[workout_type]')
    return TYPES_TRAINING[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(InfoMessage.get_message(training.show_training_info()))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
