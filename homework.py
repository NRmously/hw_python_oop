from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAINING_INFO: str = ('Тип тренировки: {training_type}; '
                          'Длительность: {duration:.3f} ч.; '
                          'Дистанция: {distance:.3f} км; '
                          'Ср. скорость: {speed:.3f} км/ч; '
                          'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.TRAINING_INFO.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    MIN_IN_HOUR = 60
    SEC_IN_HOUR = 3600
    LEN_STEP = 0.65

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
        raise NotImplementedError('Необходимо переопределить метод')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.M_IN_KM * self.duration
                          * self.MIN_IN_HOUR)
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: int
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    SM_IN_M = 100

    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                           + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                               / (self.height / self.SM_IN_M))
                           * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                           * self.weight) * self.duration
                          * self.MIN_IN_HOUR)
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER = 2

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.weight * self.duration)
        return spent_calories

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed


TYPE_OF_TRAININGS: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    return TYPE_OF_TRAININGS[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print_info = print(info.get_message())
    return print_info


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
