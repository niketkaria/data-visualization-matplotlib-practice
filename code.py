# --------------
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# Load the dataset and create column `year` which stores the year in which match was played
data_ipl = pd.read_csv(path)
data_ipl['year'] = data_ipl['date'].str[:4]

# Plot the wins gained by teams across all seasons
match_wise_data = data_ipl.drop_duplicates(subset = 'match_code')
total_wins = match_wise_data['winner'].value_counts().sort_values()
total_wins.plot(kind='barh',title = 'The No. of Wins accross all Seasons')
plt.show()
# Plot Number of matches played by each team through all seasons
temp_data = pd.melt(match_wise_data, id_vars=['match_code', 'year'], value_vars= ['team1', 'team2'])
matches_played = temp_data['value'].value_counts().sort_values()
matches_played.plot(kind = 'barh',title = 'The Total No of Matches Played by Each in all Seasons are')
plt.show()
# Top bowlers through all seasons
wickets = data_ipl[(data_ipl['wicket_kind']=='bowled')|(data_ipl['wicket_kind']=='caught')|(data_ipl['wicket_kind']=='lbw')|(data_ipl['wicket_kind']=='caught and bowled')]
bowlers_wickets = wickets.groupby(['bowler'])['wicket_kind'].count().sort_values(ascending=False)
bowlers_wickets[:10].plot(kind='barh',title = 'The Total No of Wickets per bowler is')
plt.show()
# How did the different pitches behave? What was the average score for each stadium?
score_per_venue = data_ipl.loc[:,['match_code','inning','venue','total']]
average_score_per_venue = score_per_venue.groupby(['match_code','venue','inning'])[['total']].sum()
average_score_per_venue = average_score_per_venue.groupby(['venue'])[['total']].mean().sort_values(by='total',ascending=False)
average_score_per_venue[:10].plot(kind = 'barh',title = 'Average Score Per Venue ')
plt.show()

# Types of Dismissal and how often they occur
dismissed = data_ipl.groupby(['wicket_kind']).count().reset_index()
dismissed = dismissed[['wicket_kind','delivery']]
dismissed = dismissed.rename(columns = {'delivery':'counts'})
dismissed = dismissed.sort_values(by='counts',ascending=False)
dismissed = dismissed.set_index('wicket_kind')
dismissed[:5].plot(kind='barh',title = 'Top 5 Dismissal')
plt.show()
# Plot no. of boundaries across IPL seasons
boundaries_data = data_ipl.loc[:,['runs','year']]
boundaries_four = boundaries_data[boundaries_data['runs']==4]
fours = boundaries_four.groupby(['year'])[['runs']].count().sort_values(by='runs',ascending=False)
fours.plot(kind='barh',title = 'No of Boundaries Across all Seasons')
plt.show()
# Average statistics across all seasons
per_match_data = data_ipl.drop_duplicates(subset='match_code', keep='first').reset_index(drop=True)

total_runs_per_season = data_ipl.groupby('year')['total'].sum()
balls_delivered_per_season = data_ipl.groupby('year')['delivery'].count()
no_of_match_played_per_season = per_match_data.groupby('year')['match_code'].count()
avg_balls_per_match = balls_delivered_per_season/no_of_match_played_per_season
avg_runs_per_match = total_runs_per_season/no_of_match_played_per_season
avg_runs_per_ball = total_runs_per_season/balls_delivered_per_season
avg_data = pd.DataFrame([no_of_match_played_per_season, avg_runs_per_match, avg_balls_per_match, avg_runs_per_ball])
avg_data.index =['No.of Matches', 'Average Runs per Match', 'Average balls bowled per match', 'Average runs per ball']
avg_data.T.plot(kind='bar', figsize = (12,10), colormap = 'coolwarm')
plt.xlabel('Season')
plt.ylabel('Average')
plt.legend(loc=9,ncol=4);



