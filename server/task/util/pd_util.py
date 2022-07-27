import pandas as pd

dayweek_name_list = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

dayweek_24hr_blank_list = []
for week_day in range(7):
    for hour in range(24):
        dayweek_24hr_blank_list.append({'day_week': week_day, 'hour': hour})
dayweek_24hr_blank_df = pd.DataFrame(dayweek_24hr_blank_list)

strategy_24hr_blank_list = []
for strategy in range(5):
    for hour in range(24):
        strategy_24hr_blank_list.append({'strategy': strategy, 'hour': hour})
strategy_24hr_blank_df = pd.DataFrame(strategy_24hr_blank_list)

hr24_blank_list = []
for hour in range(24):
    hr24_blank_list.append({'hour': hour})
hr24_blank_df = pd.DataFrame(hr24_blank_list)
