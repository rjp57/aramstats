from riotwatcher import RiotWatcher
import csv
api_key = input('Enter your Riot Games API Key. (https://developer.riotgames.com/)\n')
watcher = RiotWatcher(api_key) 
my_region = 'na1'
version = watcher.data_dragon.versions_for_region(my_region)['v']
dragon = watcher.data_dragon.champions(version)
champ_data = dragon['data']
begin = 0
end = 100
champs_played = []
game_ids = []
champion_ids = {}
champion_wins = {}
champion_losses = {}
champion_kills = {}
champion_deaths = {}
champion_assists = {}
win_counter = 0
loss_counter = 0
kill_counter = 0
death_counter = 0
assist_counter = 0
double_counter = 0
triple_counter = 0
quadra_counter = 0
penta_counter = 0
damage_dealt = 0
#************** End Initial Setup ******************************************************

summoner_name = input('What is your summoner name?\n')
me = watcher.summoner.by_name(my_region, summoner_name)
account_id = me['accountId']
games_to_check = input('How many games to look at? Max of 1000 and anything more than 100 will take a while\n')

#************** End Input **************************************************************************************


while end <= 1000: # Grabs all of the Match objects for the given player within the given range
	my_aram_stats = watcher.match.matchlist_by_account(my_region, account_id, begin_index = begin, end_index = end, queue = 450)
	matches = my_aram_stats['matches']
	for game in matches:
		champs_played.append(game['champion'])
		game_ids.append(game['gameId'])
	begin += 100
	end += 100


for champion in champ_data: # Sets up the per-champion stats arrays to contain all of the current champions in LoL. Should mean the program is patch-proof.
	name = champ_data[champion]['id']
	id = champ_data[champion]['key']
	champion_ids[id] = name
	champion_wins[name] = 0
	champion_losses[name] = 0
	champion_kills[name] = 0
	champion_deaths[name] = 0
	champion_assists[name] = 0



for index, x in enumerate(game_ids[:int(games_to_check)]): # Loop that iterates through all of the match objects and stores stats both per champion and overall
	match_info = watcher.match.by_id(my_region, x)	

	participants = match_info['participants']
	print("Game " + str(index + 1))
	for player in participants:
		if player['championId'] == champs_played[index]:
			print('You played: ' + champion_ids[str(champs_played[index])])
			if player['stats']['win']:
				win_counter += 1
				champion_wins[champion_ids[str(champs_played[index])]] += 1
				print ('Win!')
			else:
				loss_counter += 1
				champion_losses[champion_ids[str(champs_played[index])]] += 1
				print ('Loss!')
				
			print ('Kills ' + str(player['stats']['kills']))
			kill_counter += player['stats']['kills']
			champion_kills[champion_ids[str(champs_played[index])]] += player['stats']['kills']
			print ('Deaths ' + str(player['stats']['deaths']))
			death_counter += player['stats']['deaths']
			champion_deaths[champion_ids[str(champs_played[index])]] += player['stats']['deaths']
			print ('Assists ' + str(player['stats']['assists']))
			assist_counter += player['stats']['assists']
			champion_assists[champion_ids[str(champs_played[index])]] += player['stats']['assists']
			
			double_counter += player['stats']['doubleKills']
			triple_counter += player['stats']['tripleKills']
			quadra_counter += player['stats']['quadraKills']
			penta_counter += player['stats']['pentaKills']
			damage_dealt += player['stats']['totalDamageDealtToChampions']
	print('')

# Calculate overall stats 
KDA = (kill_counter + assist_counter)/death_counter
winrate = (win_counter/(win_counter+loss_counter)) * 100
total_damage = damage_dealt/(win_counter+loss_counter)

# Print summary
print('Total wins: ' + str(win_counter))
print('Total losses: ' + str(loss_counter))
print('Winrate: ' + str(round(winrate, 1)) + '%')
print('K/DA: ' + str(round(KDA, 1)))
print('Total Double Kills: ' + str(double_counter))
print('Total Triple Kills: ' + str(triple_counter))
print('Total Quadra Kills: ' + str(quadra_counter))
print('Total Penta Kills: ' + str(penta_counter))
print('Average Damage Dealt to Champions: ' + str(round(total_damage, 1)))
print('')

# Save the detailed per-champion stats as a CSV
with open('champion_stats.csv', 'w', newline= '') as csvfile:
	columnnames = ['Champion','Games Played', 'Wins', 'Losses', 'Winrate', 'KDA']
	outputwriter = csv.writer(csvfile, dialect='excel')
	outputwriter.writerow(columnnames)	
	for champion in champ_data:
		name = champ_data[champion]['id']
		if (champion_wins[name]+champion_losses[name] != 0):
			winrates = round(champion_wins[name]/(champion_wins[name]+champion_losses[name])*100, 1)
			kdac = (champion_kills[name]+champion_assists[name])/champion_deaths[name]
			output_list = [name, champion_wins[name]+champion_losses[name], champion_wins[name], champion_losses[name], winrates, kdac]
			outputwriter.writerow(output_list)
print('Champion Specific stats have been saved in champion_stats.csv')			
	
		