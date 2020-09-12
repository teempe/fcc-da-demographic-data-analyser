import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby("race").race.count().sort_values(ascending=False)

    # What is the average age of men?
    average_age_men = round(df.groupby("sex").age.mean().loc["Male"], 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(df.groupby("education").education.count().loc["Bachelors"] / len(df) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    mask_hi_ed = df.education.isin(["Bachelors", "Masters", "Doctorate"])
    hi_ed = df.loc[mask_hi_ed].groupby(["salary", "education"]).salary.count()
    hi_ed_all = hi_ed.sum()
    hi_ed_m_50 = hi_ed.loc[">50K"].sum()
    higher_education_rich = round(hi_ed_m_50 / hi_ed_all * 100, 1)

    # What percentage of people without advanced education make more than 50K?
    lo_ed = df.loc[~mask_hi_ed].groupby(["salary", "education"]).salary.count()
    lo_ed_all = lo_ed.sum()
    lo_ed_m_50 = lo_ed.loc[">50K"].sum()
    lower_education_rich = round(lo_ed_m_50 / lo_ed_all * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df.loc[:, "hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    mask_min_hours = df["hours-per-week"] == min_work_hours
    min_hours_sal = df.loc[mask_min_hours].groupby("salary").salary.count()
    rich_percentage = round(min_hours_sal.loc[">50K"] / min_hours_sal.sum() * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    country_salary = df.groupby(["native-country", "salary"]).salary.count().unstack(level=-1)
    country_salary["rich_perc"] = country_salary.loc[:, ">50K"].div(country_salary.sum(axis=1)).mul(100)
    highest_earning_country = country_salary.rich_perc.idxmax()
    highest_earning_country_percentage = round(country_salary.rich_perc.max(), 1)

    # Identify the most popular occupation for those who earn >50K in India.
    mask_country = df["native-country"]=="India"
    top_IN_occupation = df.loc[mask_country].groupby(["salary", "occupation"]).salary.count().loc[">50K"].idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

