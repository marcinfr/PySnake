from datetime import datetime

class Timer:
    timers = {}
    is_paused = False
    paused_time = 0
    paused_on = 0

    @staticmethod
    def get_timestamp():
        dt = datetime.now()
        return datetime.timestamp(dt)

    @staticmethod
    def start_game():
        Timer.set_time("game")

    @staticmethod
    def tick():
        if Timer.is_paused:
            Timer.is_paused = False
            paused_time = Timer.get_timestamp() - Timer.paused_on
            for code in Timer.timers.keys():
                Timer.timers[code] += paused_time

    @staticmethod
    def pause():
        if not Timer.is_paused:
            Timer.is_paused = True
            Timer.paused_on = Timer.get_timestamp()

    @staticmethod
    def set_time(code):
        Timer.timers[code] = Timer.get_timestamp()

    @staticmethod
    def has_elapsed(code, seconds, reset_if_elapsed = True):
        elapsed_time = Timer.get_elapsed_time(code)
        if elapsed_time is not False and elapsed_time < seconds:
            return False
        if reset_if_elapsed:
            Timer.set_time(code)
        return True

    @staticmethod
    def get_elapsed_time(code):
        time = Timer.timers.get(code)
        if not time:
            return False
        return Timer.get_timestamp() - time
