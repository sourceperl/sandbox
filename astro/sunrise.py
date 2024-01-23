"""
A class to compute sunset and sunrise time at a specific location.

origin: https://github.com/SatAgro/suntime/blob/master/suntime/suntime.py
"""

from math import degrees, radians, atan, tan, asin, sin, acos, cos, floor
from datetime import date, datetime, time, timedelta, timezone


class Sun:
    def __init__(self, lat: float, lon: float, day: date=None) -> None:
        self.lat = lat
        self.lon = lon
        self.day = day if day else date.today()

    @property
    def daylight_td(self) -> timedelta:
        return self.sunset_utc_dt - self.sunrise_utc_dt

    @property
    def sunrise_utc_dt(self) -> datetime:
        return self._calc_sun_time(is_rise=True)

    @property
    def sunset_utc_dt(self) -> datetime:
        return self._calc_sun_time(is_rise=False)

    @property
    def sunrise_local_dt(self) -> datetime:
        return self.sunrise_utc_dt.astimezone()

    @property
    def sunset_local_dt(self) -> datetime:
        return self.sunset_utc_dt.astimezone()

    def _calc_sun_time(self, is_rise: bool=True, zenith: float=90.8) -> datetime:
        """
        Calculate sunrise or sunset time.
        :param is_rise: True if you want to calculate sunrise time
        :param zenith: Sun reference zenith
        :return: UTC sunset or sunrise as SunTime instance
        """
        # extract year day
        yday = self.day.timetuple().tm_yday
        # convert the longitude to hour value and calculate an approximate time
        lon_hour = self.lon / 15
        if is_rise:
            # sunrise
            t = yday + ((6 - lon_hour) / 24)
        else:  
            # sunset
            t = yday + ((18 - lon_hour) / 24)
        # calculate the Sun's mean anomaly
        m = (0.9856 * t) - 3.289
        # calculate the Sun's true longitude
        ll = m + (1.916 * sin(radians(m))) + (0.020 * sin(radians(2 * m))) + 282.634
        # L adjusted into the range [0,360)
        ll = ll % 360
        # calculate the Sun's right ascension
        ra = degrees(atan(0.91764 * tan(radians(ll))))
        # RA adjusted into the range [0,360)
        ra = ra % 360
        # right ascension value needs to be in the same quadrant as L
        l_quadrant = (floor(ll / 90)) * 90
        ra_quadrant = (floor(ra / 90)) * 90
        ra = ra + (l_quadrant - ra_quadrant)
        # right ascension value needs to be converted into hours
        ra /= 15
        # calculate the Sun's declination
        sin_dec = 0.39782 * sin(radians(ll))
        cos_dec = cos(asin(sin_dec))
        # calculate the Sun's local hour angle
        cos_h = cos(radians(zenith)) - (sin_dec * sin(radians(self.lat)))
        cos_h /= cos_dec * cos(radians(self.lat))
        # if sun never rises or sets on this location (on the specified date)
        if not -1 < cos_h < 1:
            raise ValueError('no value for this location (no sunrise or sunset for this day)') 
        # finish calculating H and convert into hours
        if is_rise:
            # sunrise
            h = 360 - degrees(acos(cos_h))
        else:  
            # sunset
            h = degrees(acos(cos_h))
        h /= 15
        # calculate local mean time of rising/setting
        t = h + ra - (0.06571 * t) - 6.622
        # adjust back to UTC
        t_utc = t - lon_hour
        # UTC time in decimal format (e.g. 23.23)
        t_utc %= 24
        # convert 2.5 to 02:30:00
        hours, remain = divmod(round(t_utc* 3600), 3600)
        minutes, remain = divmod(remain, 60)
        seconds = remain
        return datetime.combine(date=self.day, time=time(hours, minutes, seconds), tzinfo=timezone.utc)
  

if __name__ == '__main__':
    # show today sunrise/sunset at Lille
    sun_lille = Sun(lat=50.6333, lon=3.0666, day=date.today())
    print(f'{sun_lille.sunrise_local_dt} -> {sun_lille.sunset_local_dt} [{sun_lille.daylight_td}]')
