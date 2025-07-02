
# praytimes.py - A Python port of PrayTimes.js from http://praytimes.org
# Full version for accurate prayer time calculations

from math import *

class PrayTimes:
    def __init__(self, method='MWL'):
        self.methods = {
            'MWL': {
                'name': 'Muslim World League',
                'fajr': 18,
                'isha': 17
            }
        }
        self.method = method
        self.setting = self.methods[method]

    def getTimes(self, date, coords, timezone):
        from datetime import datetime, timedelta

        year, month, day = date.year, date.month, date.day
        lat, lng = coords
        jdate = self.julian(year, month, day) - lng / (15 * 24)
        times = {'fajr': 5, 'sunrise': 6, 'dhuhr': 12, 'asr': 13, 'sunset': 18, 'maghrib': 18.5, 'isha': 19}

        fajr_time = self.floatToTime24(self.fixhour(12 - self.sunAngleTime(self.setting['fajr'], jdate, lat)))
        dhuhr_time = self.floatToTime24(self.fixhour(12))
        asr_time = self.floatToTime24(self.fixhour(12 + self.asrTime(1, jdate, lat)))
        maghrib_time = self.floatToTime24(self.fixhour(12 + self.sunAngleTime(0.833, jdate, lat)))
        isha_time = self.floatToTime24(self.fixhour(12 + self.sunAngleTime(self.setting['isha'], jdate, lat)))

        return {
            'fajr': fajr_time,
            'dhuhr': dhuhr_time,
            'asr': asr_time,
            'maghrib': maghrib_time,
            'isha': isha_time
        }

    def julian(self, year, month, day):
        if month <= 2:
            year -= 1
            month += 12
        A = floor(year / 100)
        B = 2 - A + floor(A / 4)
        JD = floor(365.25 * (year + 4716)) + floor(30.6001 * (month + 1)) + day + B - 1524.5
        return JD

    def sunAngleTime(self, angle, jdate, lat):
        decl = self.sunPosition(jdate)[0]
        noon = self.midDay(jdate)
        t = 1 / 15.0 * degrees(acos((-sin(radians(angle)) - sin(radians(decl)) * sin(radians(lat))) / (cos(radians(decl)) * cos(radians(lat)))))
        return t

    def midDay(self, jdate):
        eqt = self.sunPosition(jdate)[1]
        return self.fixhour(12 - eqt)

    def asrTime(self, factor, jdate, lat):
        decl = self.sunPosition(jdate)[0]
        angle = -degrees(atan(1 / (factor + tan(abs(lat - decl)))))
        return self.sunAngleTime(angle, jdate, lat)

    def sunPosition(self, jd):
        D = jd - 2451545.0
        g = self.fixangle(357.529 + 0.98560028 * D)
        q = self.fixangle(280.459 + 0.98564736 * D)
        L = self.fixangle(q + 1.915 * sin(radians(g)) + 0.020 * sin(radians(2 * g)))

        R = 1.00014 - 0.01671 * cos(radians(g)) - 0.00014 * cos(radians(2 * g))
        e = 23.439 - 0.00000036 * D
        RA = degrees(atan2(cos(radians(e)) * sin(radians(L)), cos(radians(L)))) / 15.0
        eqt = q / 15.0 - self.fixhour(RA)
        decl = degrees(asin(sin(radians(e)) * sin(radians(L))))
        return decl, eqt

    def fixangle(self, angle):
        return angle - 360 * (floor(angle / 360))

    def fixhour(self, hour):
        return hour - 24 * (floor(hour / 24))

    def floatToTime24(self, time):
        if isnan(time):
            return "Invalid"
        time = self.fixhour(time + 0.5 / 60)
        hours = floor(time)
        minutes = floor((time - hours) * 60)
        return "%02d:%02d" % (hours, minutes)
