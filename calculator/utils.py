WIDTH_DCI = 10
HEIGHT_DCI = 6.25
AGE_DCI = 5
MALE_DCI = 5
FEMALE_DCI = -165


def get_sex_dci(profile_sex) -> int:
	if profile_sex == "male":
		return MALE_DCI
	return FEMALE_DCI


def calculate_dci(profile) -> float:
	return ((profile.width * WIDTH_DCI + profile.height * HEIGHT_DCI - profile.age * 5) - get_sex_dci(profile.sex)) * profile.physical_activity.coef
