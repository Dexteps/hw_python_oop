
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')



class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action # Количество совершенных действий.
        self.duration: float = duration # Время тренировки в часах.
        self.weight: float = weight # Вес.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM 
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        dist = self.get_distance()
        mean_speed = dist / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    
    def get_spent_calories(self) -> float:
        dist = self.get_distance()
        mean_speed = self.get_mean_speed()
        time_m = self.duration * 60
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed 
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM * time_m)
        return spent_calories 
    


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_ONE = 0.035
    CALORIES_WEIGHT_TWO = 0.029
    
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height


    def get_spent_calories(self):
        dist = self.get_distance()
        mean_speed = self.get_mean_speed()
        mean_speed_m_s = mean_speed * 0.278
        height_m = self.height / 100
        duration_m = self.duration * 60
        spent_calories = ((self.CALORIES_WEIGHT_ONE * self.weight + (mean_speed_m_s ** 2 / height_m) 
                         * self.CALORIES_WEIGHT_TWO * self.weight) * duration_m)
        return spent_calories   
        


class Swimming(Training):
    """Тренировка: плавание."""
    
    COEFF_FORMUL_CALORIES_ONE = 1.1
    COEFF_FORMUL_CALORIES_TWO = 2
    LEN_STEP = 1.38
   
    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool # Длина бассейна.
        self.count_pool = count_pool # сколько раз переплыл.

    def get_mean_speed(self):
        mean_speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        spent_calories = ((mean_speed + self.COEFF_FORMUL_CALORIES_ONE) 
                               * self.COEFF_FORMUL_CALORIES_TWO * self.weight * self.duration)
        return spent_calories
            
            



def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training = {'SWM': Swimming, 
                     'RUN': Running, 
                     'WLK': SportsWalking}
    if workout_type in type_training:
        class_training: Training = type_training[workout_type](*data)
        return class_training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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

