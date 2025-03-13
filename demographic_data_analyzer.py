import pandas as pd
import numpy as np

def get_percentage(value: float) -> float:
    return np.round(100 * value, 1)

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.value_counts('race')

    # What is the average age of men?
    average_age_men = np.round(df.query(f'`sex` == "Male"').loc[:, 'age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = len(df[df['education'] == 'Bachelors']) / df.shape[0]
    percentage_bachelors = get_percentage(percentage_bachelors)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    advanced_education = ['Bachelors', 'Masters', 'Doctorate']

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(advanced_education)]
    lower_education = df[~df['education'].isin(advanced_education)]

    # percentage with salary >50K
    higher_education_rich = len(higher_education[higher_education['salary'] == '>50K']) / higher_education.shape[0]
    higher_education_rich = get_percentage(higher_education_rich)

    lower_education_rich = len(lower_education[lower_education['salary'] == '>50K']) / lower_education.shape[0]
    lower_education_rich = get_percentage(lower_education_rich)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df.query(f'`hours-per-week` == {min_work_hours}')
    rich_percentage = len(num_min_workers.query(f'`salary` == ">50K"')) / num_min_workers.shape[0]
    rich_percentage = get_percentage(rich_percentage)

    # What country has the highest percentage of people that earn >50K?
    count_people = df.value_counts("native-country")
    count_people_high_earn = df.query(f'`salary` == ">50K"').value_counts("native-country")
    aux_df = pd.DataFrame({'total': count_people, 'high-salary': count_people_high_earn}).fillna(0)

    # put the native-country as a column
    aux_df = aux_df.reset_index().rename(columns={'index': 'native-country'})
    aux_df['percentage'] = aux_df['high-salary'] / aux_df['total']

    # get the highest percentage row
    highest_earning_row = aux_df[aux_df['percentage'] == aux_df['percentage'].max()]
    
    highest_earning_country = highest_earning_row.iloc[0, 0]

    highest_earning_country_percentage = highest_earning_row.iloc[0, 3]
    highest_earning_country_percentage = get_percentage(highest_earning_country_percentage)

    # Identify the most popular occupation for those who earn >50K in India.
    occupations_in_india = df.query(f'`native-country` == "India" and `salary` == ">50K"').value_counts("occupation")
    top_IN_occupation = occupations_in_india.index.tolist()[0]

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


calculate_demographic_data()