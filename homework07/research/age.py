import datetime as dt
import typing as tp

from dateutil.parser import parse

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    friends = get_friends(user_id, fields=["bdate"])
    bdates_str = [age["bdate"] for age in friends.items if  age is not int and age["bdate"] is not None and age["bdate"].count(".") == 2]
    bdates = [parse(date) for date in bdates_str]
    ages = [dt.datetime.now() - age for age in bdates]
    ages_years = [age.days // 365 for age in ages]
    return sum(ages_years) / len(ages_years) if ages_years else None
