import datetime

class ClockLogic:
    def __init__(self):
        # Initial values
        self.seconds = 0
        self.minutes = 0
        self.hour = 0

    def update_time(self):
        """Fetches current system time."""
        now = datetime.datetime.now()
        self.seconds = now.second
        self.minutes = now.minute
        self.hour = now.hour

    def calculate_angles(self):
        """
        Calculates rotation angles for Mickey's hands.
        Formula: (units / total_units) * 360 degrees.
        """
        # 6 degrees per second (360/60)
        sec_angle = self.seconds * 6
        
        # 6 degrees per minute + smooth offset based on seconds
        min_angle = (self.minutes * 6) + (self.seconds / 10)
        
        return sec_angle, min_angle

    def get_time_string(self):
        """Returns time formatted as HH:MM:SS for debugging or UI."""
        return f"{self.hour:02d}:{self.minutes:02d}:{self.seconds:02d}"