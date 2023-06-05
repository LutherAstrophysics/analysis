import datetime
import decimal
import math

dec = decimal.Decimal

# Most of this code was taken from
# https://gist.github.com/miklb/ed145757971096565723


class MoonPositions:
    NewMoon = "New Moon"
    WaxingCrescent = "Waxing Crescent"
    FirstQuarter = "First Quarter"
    WaxingGibbous = "Waxing Gibbous"
    FullMoon = "Full Moon"
    WaningGibbous = "Waning Gibbous"
    LastQuarter = "Last Quarter"
    WaningCresce = "Waning Crescent"


def position(now=None):
    if now is None:
        now = datetime.datetime.now()

    diff = now - datetime.datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))

    return lunations % dec(1)


def phase(pos):
    index = (pos * dec(8)) + dec("0.5")
    index = math.floor(index)
    return {
        0: MoonPositions.NewMoon,
        1: MoonPositions.WaxingCrescent,
        2: MoonPositions.FirstQuarter,
        3: MoonPositions.WaxingGibbous,
        4: MoonPositions.FullMoon,
        5: MoonPositions.WaningGibbous,
        6: MoonPositions.LastQuarter,
        7: MoonPositions.WaningCresce,
    }[int(index) & 7]