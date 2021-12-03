from datetime import datetime, timedelta, time

WIDTH_DCI = 10
HEIGHT_DCI = 6.25
AGE_DCI = 5
MALE_DCI = 5
FEMALE_DCI = -165

FATS_PERCENTAGE_FROM_DCI = 0.1
PROTEIN_PERCENTAGE_FROM_DCI = 0.35


def get_sex_dci(profile_sex) -> int:
    if profile_sex == "male":
        return MALE_DCI
    return FEMALE_DCI


def calculate_dci(profile) -> float:
    return (
        (profile.weight * WIDTH_DCI + profile.height * HEIGHT_DCI - profile.age * 5)
        - get_sex_dci(profile.sex)
    ) * float(profile.physical_activity.coef)


def calculate_water_norm(profile) -> float:
    if profile.sex == "male":
        return profile.weight * 40
    return profile.weight * 30


def get_dates_for_today_filtering():
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    return today_start, today_end


def get_dates_for_week_filtering():
    today = datetime.now().date()
    week_ago = today - timedelta(7)
    tomorrow = today + timedelta(1)
    week_ago = datetime.combine(week_ago, time())
    today_end = datetime.combine(tomorrow, time())
    return week_ago, today_end
