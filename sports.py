import urllib.error

from discord.ext import commands
from sportsipy.mlb.boxscore import Boxscore as MLB_Boxscore
from sportsipy.mlb.boxscore import Boxscores as MLB_Boxscores
from sportsipy.mlb.teams import Team as MLB_Team
from sportsipy.mlb.roster import Player as MLB_Player
from sportsipy.nfl.teams import Team as NFL_Team
from sportsipy.nfl.roster import Player as NFL_Player
from sportsipy.nfl.boxscore import Boxscore as NFL_Boxscore     # not working; creating a Boxscore object returns an empty document
from sportsipy.nfl.boxscore import Boxscores as NFL_Boxscores
from sportsipy.nba.teams import Team as NBA_Team
from sportsipy.nba.roster import Player as NBA_Player
from sportsipy.nba.boxscore import Boxscore as NBA_Boxscore
from sportsipy.nba.boxscore import Boxscores as NBA_Boxscores
from datetime import datetime
from typing import List, Optional


class Sports(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mlb_abbrevs = {
            "dodgers": "LAD", "yankees": "NYY", "mets": "NYM", "milwaukee": "MIL", "brewers": "MIL",
            "padres": "SDP", "houston": "HOU", "astros": "HOU", "minnesota": "MIN", "twins": "MIN",
            "giants": "SFG", "rays": "TBR", "cardinals": "STL", "st louis": "STL", "blue jays": "TOR",
            "toronto": "TOR", "arizona": "ARI", "diamondbacks": "ARI", "colorado": "COL",
            "rockies": "COL", "cleveland": "CLE", "indians": "CLE", "guardians": "CLE", "white sox": "CHW",
            "atlanta": "ATL", "braves": "ATL", "philadelphia": "PHI", "phillies": "PHI", "miami": "MIA",
            "marlins": "MIA", "seattle": "SEA", "mariners": "SEA", "baltimore": "BAL", "orioles": "BAL",
            "texas": "TEX", "rangers": "TEX", "oakland": "OAK", "athletics": "OAK", "pittsburgh": "PIT",
            "pirates": "PIT", "cubs": "CHC", "boston": "BOS", "royals": "KCR", "washington": "WSN",
            "nationals": "WSN", "detroit": "DET", "tigers": "DET", "cincinnati": "CIN", "reds": "CIN",
            "angels": "LAA", "san diego": "SDP", "san fransisco": "SFG", "tampa bay": "TBR",
            "red sox": "BOS", "kansas city": "KCR"
        }

        self.nfl_abbrevs = {
            "dallas": "DAL", "cowboys": "DAL", "tampa bay": "TAM", "buccaneers": "TAM", "buffalo": "BUF",
            "bills": "BUF", "kansas city": "KAN", "chiefs": "KAN", "chargers": "SDG", "new england": "NWE",
            "patriots": "NWE", "cincinnati": "CIN", "bengals": "CIN", "rams": "RAM", "cotls": "CLT",
            "indianapolis": "CLT", "green bay": "GNB", "packers": "GNB", "arizona": "CRD",
            "cardinals": "CRD", "philadelphia": "PHI", "eagles": "PHI", "san francisco": "SFO",
            "49ers": "SFO", "minnesota": "MIN", "vikings": "MIN", "tennessee": "OTI", "titans": "OTI",
            "seattle": "SEA", "seahawks": "SEA", "baltimore": "RAV", "ravens": "RAV", "las vegas": "RAI",
            "raiders": "RAI", "new orleans": "NOR", "saints": "NOR", "cleveland": "CLE", "browns": "CLE",
            "pittsburgh": "PIT", "steelers": "PIT", "miami": "MIA", "dolphins": "MIA", "denver": "DEN",
            "broncos": "DEN", "washington": "WAS", "redskins": "WAS", "commanders": "WAS", "detroit": "DET",
            "lions": "DET", "atlanta": "ATL", "falcons": "ATL", "chicago": "CHI", "bears": "CHI",
            "jets": "NYJ", "carolina": "CAR", "panthers": "CAR", "houston": "HTX", "texans": "HTX",
            "giants": "NYG", "jacksonville": "JAX", "jaguars": "JAX"
        }

        self.nba_abbrevs = {
            "minnesota": "MIN", "timberwolves": "MIN", "memphis": "MEM", "grizzlies": "MEM", "bucks": "MIL",
            "milwaukee": "MIL", "charlotte": "CHO", "hornets": "CHO", "phoenix": "PHO", "suns": "PHO",
            "atlanta": "ATL", "hawks": "ATL", "utah": "UTA", "jazz": "UTA", "san antonio": "SAS",
            "spurs": "SAS", "brooklyn": "BRK", "nets": "BRK", "denver": "DEN", "nuggets": "DEN",
            "lakers": "LAL", "boston": "BOS", "celtics": "BOS", "chicago": "CHI", "bulls": "CHI",
            "indiana": "IND", "pacers": "IND", "golden state": "GSW", "warriors": "GSW", "kings": "SAC",
            "sacramento": "SAC", "miami": "MIA", "heat": "MIA", "philadelphia": "PHI", "76ers": "PHI",
            "houston": "HOU", "rockets": "HOU", "toronto": "TOR", "raptors": "TOR", "pelicans": "NOP",
            "new orleans": "NOP", "washington": "WAS", "wizards": "WAS", "clippers": "LAC", "dallas": "DAL",
            "mavericks": "DAL", "cleveland": "CLE", "cavaliers": "CLE", "new york": "NYK", "knicks": "NYK",
            "portland": "POR", "trail blazers": "POR", "detroit": "DET", "pistons": "DET", "orlando": "ORL",
            "magic": "ORL", "oklahoma city": "OKC", "thunder": "OKC"
        }

    """--------------------------------------------HELPER FUNCTIONS-------------------------------------------"""

    # Takes the passed in name and converts it to an MLB player code. A single name may correspond to multiple codes, so
    # a list of players is returned. An invalid player name returns an empty list.
    @staticmethod
    def mlb_player_name_to_code(first_name: str, last_name: str) -> List[MLB_Player]:
        player_code = ""
        player_code += last_name[0:5]
        player_code += first_name[0:2]

        player_code = player_code.lower()
        number = 1
        ret_list = []

        # keep checking for multiple LLLLLFF codes corresponding to the passed in player name
        while True:
            if number < 10:
                player_code += "0" + str(number)
            else:
                player_code += str(number)

            try:
                player = MLB_Player(player_code)
            except TypeError:       # break out of the loop once the player code is not found
                break

            player("2022")
            ret_list.append(player)
            player_code = player_code[0:-2]
            number += 1

        return ret_list

    # takes in a player name and creates an NFL Player object from it. Multiple codes may br valid from the given name, so return
    # a list of Players. An invalid player name will return an empty list.
    @staticmethod
    def nfl_player_name_to_code(first_name: str, last_name: str) -> List[NFL_Player]:
        player_code = ""
        player_code += last_name[0:4]
        player_code += first_name[0:2]
        number = 0
        ret_list = []

        # keep checking for multiple LlllFf codes corresponding to the passed in player name
        while True:
            if number < 10:
                player_code += "0" + str(number)
            else:
                player_code += str(number)

            player = NFL_Player(player_code)
            if player.games is None:    # a bad code will still create a player, so check an arbitrary stat for None to determine a valid player
                break

            player("2021")
            ret_list.append(player)
            player_code = player_code[0:-2]     # remove the NN part of the code, so it can be used for the next player
            number += 1

        return ret_list

    # takes in a player name and creates an NBA Player object from it. Multiple codes may br valid from the given name, so return
    # a list of Players. An invalid player name will return an empty list.
    @staticmethod
    def nba_player_name_to_code(player_name: str) -> List[NBA_Player]:
        ret_list = []
        number = 1
        name = player_name.lower()
        name = name.split(" ")

        if len(name) != 2:
            return ret_list

        player_code = name[1][0:5]
        player_code += name[0][0:2]

        # keep checking for multiple LLLLLFFNN codes corresponding to the passed in player name
        while True:
            if number < 10:
                player_code += "0" + str(number)
            else:
                player_code += str(number)

            player = NBA_Player(player_code)
            if player.name is None:     # a bad code will still create a player, so check an arbitrary stat for None to determine a valid player
                break

            player("2021-22")
            ret_list.append(player)
            player_code = player_code[0:-2]
            number += 1

        return ret_list

    # takes in a team name and returns an MLB Team object
    async def get_mlb_team(self, ctx, team_name: str) -> Optional[MLB_Team]:
        name = team_name.lower()
        team_abbrev = self.mlb_abbrevs.get(name)
        if team_abbrev is None:
            await ctx.send("Invalid team name")
            return None

        team = MLB_Team(team_abbrev)
        if team is None:
            await ctx.send("There was an error getting the team")
            return None

        return team

    # takes in a team name and returns an NFL Team object
    async def get_nfl_team(self, ctx, team_name: str) -> Optional[NFL_Team]:
        name = team_name.lower()
        team_abbrev = self.nfl_abbrevs.get(name)
        if team_abbrev is None:
            await ctx.send("Invalid team name")
            return None

        team = NFL_Team(team_abbrev)
        if team is None:
            await ctx.send("There was an error getting the team")
            return None

        return team

    # takes in a team name and returns an NBA Team object
    async def get_nba_team(self, ctx, team_name: str) -> Optional[NBA_Team]:
        name = team_name.lower()
        team_abbrev = self.nba_abbrevs.get(name)
        if team_abbrev is None:
            await ctx.send("Invalid team name")
            return None

        team = NBA_Team(team_abbrev)
        if team is None:
            await ctx.send("There was an error getting the team")
            return

        return team

    """-----------------------------------------------COMMANDS------------------------------------------------"""

    # Get stats on a player
    @commands.group(name="mlbplayer", help="Parent command to get player stats")
    async def mlb_player(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid parameters")

    @mlb_player.command(name="homeruns")
    async def mlb_player_home_runs(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid player name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} hit {player.home_runs} home runs this season\n"

        await ctx.send(out_string)

    @mlb_player.command(name="walks")
    async def mlb_player_walks(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} drew {player.bases_on_balls} walks this season\n"

        await ctx.send(out_string)

    @mlb_player.command(name="average")
    async def mlb_player_batting_average(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} hit {player.batting_average} this season\n"

        await ctx.send(out_string)

    @mlb_player.command(name="era")
    async def mlb_player_era(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has an ERA of {player.era} this season\n"

        await ctx.send(out_string)

    @mlb_player.command(name="era+")
    async def mlb_player_era_plus(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has an ERA+ of {player.era_plus} this season\n"

        await ctx.send(out_string)

    @mlb_player.command(name="nationality")
    async def mlb_player_nationality(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} is from {player.nationality}\n"

        await ctx.send(out_string)

    @mlb_player.command(name="obp")
    async def mlb_player_on_base_percentage(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has an on base percentage of {player.on_base_percentage}\n"

        await ctx.send(out_string)

    @mlb_player.command(name="ops")
    async def mlb_player_on_base_percentage_plus_slugging(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has an OPS of {player.on_base_plus_slugging_percentage}\n"

        await ctx.send(out_string)

    @mlb_player.command(name="ops+")
    async def mlb_player_on_base_percentage_plus_slugging_plus(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has an OPS+ of {player.on_base_plus_slugging_percentage_plus}\n"

        await ctx.send(out_string)

    @mlb_player.command(name="rbi")
    async def mlb_player_runs_batted_in(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has hit {player.runs_batted_in} RBI\n"

        await ctx.send(out_string)

    @mlb_player.command(name="team")
    async def mlb_player_team(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} plays for {player.team_abbreviation}\n"

        await ctx.send(out_string)

    @mlb_player.command(name="whip")
    async def mlb_player_whip(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has a WHIP of {player.whip}\n"

        await ctx.send(out_string)

    @mlb_player.command(name="summary")
    async def mlb_player_summary(self, ctx, *, player_name: str):
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.mlb_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} plays for {player.team_abbreviation}\n" \
                          f"A slash line of {player.batting_average}/{player.on_base_percentage}/{player.slugging_percentage}\n" \
                          f"An OPS+ of {player.on_base_plus_slugging_percentage_plus}\n" \
                          f"An ERA of {player.era}\n" \
                          f"An ERA+ of {player.era_plus}\n"

        await ctx.send(out_string)

    # Get stats for a MLB team
    @commands.group(name="mlbteam", help="Parent command to get team stats")
    async def mlb_team(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid parameters")

    @mlb_team.command(name="walks", help="displays the number of times the team walked")
    async def mlb_team_walks(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have walked {team.bases_on_balls} times")

    @mlb_team.command(name="walkspernine", help="displays the number of walks per nine innings the team gives up")
    async def mlb_team_walks_per_nine_innings(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(
                f"The {team.name} give up {team.bases_on_walks_given_per_nine_innings} walks per nine innings")

    @mlb_team.command(name="balks", help="displays the number of balks the team committed")
    async def mlb_team_balks(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have balked {team.balks} times")

    @mlb_team.command(name="lastten", help="displays the team's record in their last 10 games")
    async def mlb_team_last_ten(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have gone {team.last_ten_games_record} in their last ten games")

    @mlb_team.command(name="awayrecord", help="displays the team's record away from home")
    async def mlb_team_away_record(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have gone {team.away_record} in away games")

    @mlb_team.command(name="homerecord", help="displays the team's record at home")
    async def mlb_team_home_record(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have gone {team.home_record} in home games")

    @mlb_team.command(name="strikeoutstaken", help="displays the number of times the team struck out")
    async def mlb_team_strikeouts_taken(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have struck out {team.times_struck_out} times")

    @mlb_team.command(name="strikeoutspernine", help="displays the number of times the team strikes out opponents per nine innings")
    async def mlb_team_strikeouts_per_nine_innings(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} strike out {team.strikeouts_per_nine_innings} batters per nine innings")

    @mlb_team.command(name="average", help="displays the team's batting average")
    async def mlb_team_average(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have a batting average of {team.batting_average}")

    @mlb_team.command(name="extrainningsrecord", help="displays the team's record in extra innings")
    async def mlb_team_extra_innings_record(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have gone {team.extra_inning_record} in extra innings")

    @mlb_team.command(name="homeruns", help="displays the number of home runs the team hit")
    async def mlb_team_home_runs(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have hit {team.home_runs} home runs")

    @mlb_team.command(name="homerunsagainst", help="displays the number of home runs the team has given up")
    async def mlb_team_home_runs_against(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have given up {team.home_runs_against} home runs")

    @mlb_team.command(name="obp", help="displays the on base percentage of a team")
    async def mlb_team_on_base_percentage(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have an OBP of {team.on_base_percentage}")

    @mlb_team.command(name="ops", help="displays the on base plus slugging percentage of a team")
    async def mlb_team_on_base_percentage_plus_slugging(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have an OPS of {team.on_base_plus_slugging_percentage}")

    @mlb_team.command(name="ops+", help="displays the OPS plus of a team")
    async def mlb_team_on_base_percentage_plus_slugging_plus(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have an OPS+ of {team.on_base_plus_slugging_percentage_plus}")

    @mlb_team.command(name="recordabove500", help="displays a team's record against opponents above .500")
    async def mlb_team_record_above_500(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have a record of {team.record_vs_teams_over_500} against teams above .500")

    @mlb_team.command(name="recordunder500", help="displays a team's record against opponents under .500")
    async def mlb_team_record_under_500(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have a record of {team.record_vs_teams_under_500} against teams under .500")

    @mlb_team.command(help="displays the team's record")
    async def mlb_team_record(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have a record of {team.wins}-{team.losses}")

    @mlb_team.command("whip", help="displays the team's walks and hits per inning pitched")
    async def mlb_team_whip(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have a record of {team.wins}-{team.losses}")

    @mlb_team.command(name="triples", help="displays the number of triples the team has hit")
    async def mlb_team_triples(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have hit {team.triples} triples this season")

    @mlb_team.command(name="stolenbases", help="displays the number of bases the team has stolen")
    async def mlb_team_stolen_bases(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have stolen {team.stolen_bases} bases this season")

    @mlb_team.command(name="summary", help="displays basic information about a team")
    async def mlb_team_summary(self, ctx, *, team_name: str):
        team = await self.get_mlb_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have a record of {team.wins}-{team.losses}\n"
                           f"with a batting average of {team.batting_average}, OPS+ of {team.on_base_plus_slugging_percentage_plus}, and a ERA+ of {team.earned_runs_against_plus}\n"
                           f"Runs scored per game: {team.runs}\tRuns allowed per game: {team.runs_against}\n"
                           f"{team.home_record} record at home\t{team.away_record} record on the road\n"
                           f"They currently have a rank of {team.rank} out of 30 teams")

    # Get the MLB schedule for a specific date in the past
    @commands.command(name="mlbscores", help="displays all MLB scores on the given date")
    async def mlb_scores(self, ctx, month=None, day=None, year=None):
        if month is None or day is None or year is None:
            await ctx.send("Invalid date parameters")
            return

        try:
            input_date = datetime(int(year), int(month), int(day))
        except ValueError:
            await ctx.send("Invalid date parameters")
            return

        if input_date > datetime.today():
            input_date = datetime.today()

        today_games = MLB_Boxscores(input_date)
        x = input_date.date()
        xFormat = f"{x.month}-{x.day}-{x.year}"
        games = today_games.games[xFormat]  # gets the value (list of games) for the passed in key (date)
        games_date = next(iter(today_games.games))  # gets the key (date) of the entire dict
        await ctx.send(f"Scores for: {games_date}")
        out_string = ""
        for game in games:
            # puts the teams' names and scores in the output string
            out_string += f"\n{game.get('away_name')} {game.get('away_score')} - {game.get('home_name')} {game.get('home_score')}"

        await ctx.send(out_string)

    # Get the details of the specified game
    @commands.group(name="mlbgame", help="Parent command to get stats for a game")
    async def mlb_game(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid parameters")

    # game_code is the part of the game URL that contains the game-specific info (e.g. BAL/BAL202009200)
    @mlb_game.command(name="summary", help="displays a summary of the game")
    async def mlb_game_summary(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:  # passing in a bad game code won't return a None game, so check a data member for None
            winner = game.winner
            final_output = ""       # contains the message to send to Discord
            inning_scores = list(game.summary.values())     # get the runs scored in each inning for each team
            if winner == "Home":
                final_output += game.losing_name + "\t" + str(inning_scores[0]) + f"     R: {game.away_runs}\tH: {game.away_hits}\n"
                final_output += game.winning_name + "\t" + str(inning_scores[1]) + f"    R: {game.home_runs}\tH: {game.home_hits}\n"
            elif winner == "Away":
                final_output += game.winning_name + "\t" + str(inning_scores[0]) + f"    R: {game.away_runs}\tH: {game.away_hits}\n"
                final_output += game.losing_name + "\t" + str(inning_scores[1]) + f"    R: {game.home_runs}\tH: {game.home_hits}\n"
            else:
                await ctx.send("Error retrieving game data")
                return

            final_output += f"Game played at {game.venue} with an attendance of {game.attendance}\n"
            final_output += f"Duration: {game.duration} on {game.date}"
            await ctx.send(final_output)
        else:
            await ctx.send("Invalid game code")

    @mlb_game.command(name="attendance", help="displays the attendance of the game")
    async def mlb_game_attendance(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:   # check valid game
            await ctx.send(f"Attendance: {game.attendance}")
        else:
            await ctx.send("Invalid game code")

    @mlb_game.command(name="venue", help="displays the venue of the game")
    async def mlb_game_venue(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:  # check valid game
            await ctx.send(f"The game was played at {game.venue}")
        else:
            await ctx.send("Invalid game code")

    @mlb_game.command(name="strikeouts", help="displays the number of strikeouts for each team")
    async def mlb_game_strikeouts(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:  # check valid game
            await ctx.send(f"The away team struck out {game.away_strikeouts} times, and the home team "
                           f"struck out {game.home_strikeouts} times")
        else:
            await ctx.send("Invalid game code")

    @mlb_game.command(name="homeruns", help="displays the number of home runs each team hit")
    async def mlb_game_home_runs(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:  # check valid game
            await ctx.send(f"The away team hit {game.away_home_runs} home runs, and the home team "
                           f"hit {game.home_home_runs} home runs")
        else:
            await ctx.send("Invalid game code")

    @mlb_game.command(name="slugging", help="displays the slugging percentage for each team in the game")
    async def mlb_game_slugging(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:  # check valid game
            await ctx.send(f"The away team slugged {game.away_slugging_percentage}, and the home team slugged {game.home_slugging_percentage}")
        else:
            await ctx.send("Invalid game code")

    @mlb_game.command(name="average", help="displays the batting average for each team in the game")
    async def mlb_game_average(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:  # check valid game
            await ctx.send(f"The away team hit {game.away_batting_average}, and the home team hit {game.home_batting_average}")
        else:
            await ctx.send("Invalid game code")

    @mlb_game.command(name="flyballs", help="displays the number of fly balls each team hit in the game")
    async def mlb_game_fly_balls(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:  # check valid game
            await ctx.send(
                f"The away team allowed {game.away_fly_balls} fly balls, and the home team allowed {game.home_fly_balls} fly balls")
        else:
            await ctx.send("Invalid game code")

    @mlb_game.command(name="groundballs", help="displays the number of ground balls each team hit in the game")
    async def mlb_game_ground_balls(self, ctx, game_code: str):
        game = MLB_Boxscore(game_code)
        if game.home_assists is not None:  # check valid game
            await ctx.send(
                f"The away team allowed {game.away_grounded_balls} ground balls, and the home team "
                f"allowed {game.home_grounded_balls} ground balls")
        else:
            await ctx.send("Invalid game code")

    # Get stats for an NFL team
    @commands.group(name="nflteam", help="Parent command to get team stats")
    async def nfl_team(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid parameters")

    @nfl_team.command(name="name", help="get the team's name")
    async def nfl_team_name(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The team is named the {team.name}")

    @nfl_team.command(name="firstdowns", help="get the number of a team's 1st downs for the season")
    async def nfl_team_first_downs(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have {team.first_downs} first downs this season")

    @nfl_team.command(name="firstdownspenalties", help="get the number of 1st downs from penalties conceded by the team")
    async def nfl_team_first_downs_from_penalties(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have conceded {team.first_downs_from_penalties} first downs from penalties this season")

    @nfl_team.command(name="fumbles", help="get the number of times the team fumbled the ball")
    async def nfl_team_fumbles(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have fumbled the ball {team.fumbles} times this season")

    @nfl_team.command(name="interceptions", help="get the number of interceptions a team has thrown")
    async def nfl_team_interceptions(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have thrown {team.interceptions} interception this season")

    @nfl_team.command(name="losses", help="get the number of team losses")
    async def nfl_team_losses(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have lost {team.losses} games this season")

    @nfl_team.command(name="passattempts", help="get the number of a team's pass attempts")
    async def nfl_team_pass_attempts(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have attempted {team.pass_attempts} passes this season")

    @nfl_team.command(name="passcompletions", help="get the number of a team's pass completions")
    async def nfl_team_pass_completions(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have completed {team.pass_completions} passes this season")

    @nfl_team.command(name="passtd", help="get the number of a team's pass touchdowns")
    async def nfl_team_pass_touchdowns(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have thrown {team.pass_touchdowns} touchdowns this season")

    @nfl_team.command(name="passyards", help="get the number of a team's pass yards")
    async def nfl_team_pass_yards(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have thrown for {team.pass_yards} yards this season")

    @nfl_team.command(name="penalties", help="get the number of penalties the team committed")
    async def nfl_team_penalties(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have committed {team.penalties} penalties this season")

    @nfl_team.command(name="pointsagainst", help="get the number of points a team has given up")
    async def nfl_team_points_against(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have given up {team.points_against} points this season")

    @nfl_team.command(name="points", help="get the number of points a team has scored")
    async def nfl_team_points(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have scored {team.points_for} points this season")

    @nfl_team.command(name="rushattempts", help="get the number of a team's rush attempts")
    async def nfl_team_rush_attempts(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} rushed {team.rush_attempts} times this season")

    @nfl_team.command(name="rushtd", help="get the number of a team's rush TD")
    async def nfl_team_rush_touchdowns(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have {team.rush_touchdowns} rushing touchdowns this season")

    @nfl_team.command(name="rushyards", help="get the number of a team's rush yards")
    async def nfl_team_rush_yards(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have rushed for {team.rush_yards} yards this season")

    @nfl_team.command(name="sos", help="get a team's strength of schedule")
    async def nfl_team_strength_of_schedule(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have a strength of schedule of {team.strength_of_schedule} (0 is average)")

    @nfl_team.command(name="turnovers", help="get the number of turnovers a team committed")
    async def nfl_team_turnovers_committed(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have committed {team.turnovers} turnovers this season")

    @nfl_team.command(name="wins", help="get the number of team wins")
    async def nfl_team_wins(self, ctx, *, team_name: str):
        team = await self.get_nfl_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have won {team.wins} games this season")

    # Get stats for an NFL player
    @commands.group(name="nflplayer", help="Parent command to get player stats for a season. Retired players will get career stats")
    async def nfl_player(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid parameters")

    @nfl_player.command(name="passattempts")
    async def nfl_player_attempted_passes(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} attempted {player.attempted_passes} passes this season\n"

        await ctx.send(out_string)

    @nfl_player.command(name="birthday")
    async def nfl_player_birthday(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} was born on {player.birth_date}\n"

        await ctx.send(out_string)

    @nfl_player.command(name="catchpercent")
    async def nfl_player_catch_percentage(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} caught {player.catch_percentage}% of passes thrown to him\n"

        await ctx.send(out_string)

    @nfl_player.command(name="completedpasses")
    async def nfl_player_completed_passes(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} completed {player.completed_passes} passes\n"

        await ctx.send(out_string)

    @nfl_player.command(name="fieldgoalattempts")
    async def nfl_player_field_goals_attempted(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} attempted {player.field_goals_attempted} field goals\n"

        await ctx.send(out_string)

    @nfl_player.command(name="fieldgoalsmade")
    async def nfl_player_field_goals_made(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} made {player.field_goals_made} field goals\n"

        await ctx.send(out_string)

    @nfl_player.command(name="comebacks")
    async def nfl_player_fourth_quarter_comebacks(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} came back from a deficit in the 4th quarter {player.fourth_quarter_comebacks} times\n"

        await ctx.send(out_string)

    @nfl_player.command(name="fumbles")
    async def nfl_player_fumbles(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} fumbled the ball {player.fumbles} times\n"

        await ctx.send(out_string)

    @nfl_player.command(name="forcedfumbles")
    async def nfl_player_fumbles_forced(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} forced {player.fumbles_forced} fumbles\n"

        await ctx.send(out_string)

    @nfl_player.command(name="recoveredfumbles")
    async def nfl_player_fumbles_recovered(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} recovered {player.fumbles_recovered} fumbles\n"

        await ctx.send(out_string)

    @nfl_player.command(name="height")
    async def nfl_player_height(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has a height of {player.height}\n"

        await ctx.send(out_string)

    @nfl_player.command(name="interceptions")
    async def nfl_player_interceptions(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} intercepted {player.interceptions} passes\n"

        await ctx.send(out_string)

    @nfl_player.command(name="interceptionsthrown")
    async def nfl_player_interceptions_thrown(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} threw {player.interceptions_thrown} interceptions\n"

        await ctx.send(out_string)

    @nfl_player.command(name="longestfg")
    async def nfl_player_longest_field_goal(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id}'s longest field goal is {player.longest_field_goal_made} yards\n"

        await ctx.send(out_string)

    @nfl_player.command(name="longestpass")
    async def nfl_player_longest_pass(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id}'s longest pass is {player.longest_pass} yards\n"

        await ctx.send(out_string)

    @nfl_player.command(name="passingtd")
    async def nfl_player_passing_touchdowns(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has thrown {player.passing_touchdowns} touchdowns\n"

        await ctx.send(out_string)

    @nfl_player.command(name="passingyards")
    async def nfl_player_passing_yards(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has thrown for {player.passing_yards} yards\n"

        await ctx.send(out_string)

    @nfl_player.command(name="position")
    async def nfl_player_position(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} plays {player.position}\n"

        await ctx.send(out_string)

    @nfl_player.command(name="qbrating")
    async def nfl_player_quarterback_rating(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has a QB rating of {player.quarterback_rating}\n"

        await ctx.send(out_string)

    @nfl_player.command(name="receivingyards")
    async def nfl_player_receiving_yards(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has {player.receiving_yards} receiving yards\n"

        await ctx.send(out_string)

    @nfl_player.command(name="receivingtd")
    async def nfl_player_receiving_touchdowns(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has {player.receiving_touchdowns} receiving touchdowns\n"

        await ctx.send(out_string)

    @nfl_player.command(name="receptions")
    async def nfl_player_receptions(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has {player.receptions} receptions\n"

        await ctx.send(out_string)

    @nfl_player.command(name="rushattempts")
    async def nfl_player_rush_attempts(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has {player.rush_attempts} rush attempts\n"

        await ctx.send(out_string)

    @nfl_player.command(name="rushtd")
    async def nfl_player_rush_touchdowns(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has {player.rush_touchdowns} rush touchdowns\n"

        await ctx.send(out_string)

    @nfl_player.command(name="rushyards")
    async def nfl_player_rush_yards(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has {player.rush_touchdowns} rush yards\n"

        await ctx.send(out_string)

    @nfl_player.command(name="sacks")
    async def nfl_player_sacks(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} sacked the quarterback {player.sacks} times\n"

        await ctx.send(out_string)

    @nfl_player.command(name="tackles")
    async def nfl_player_tackles(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} has {player.tackles} tackles\n"

        await ctx.send(out_string)

    @nfl_player.command(name="team")
    async def nfl_player_team_abbreviation(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} plays for {player.team_abbreviation}\n"

        await ctx.send(out_string)

    @nfl_player.command(name="timestargeted")
    async def nfl_player_times_targeted(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} was targeted {player.times_pass_target} times\n"

        await ctx.send(out_string)

    @nfl_player.command(name="timessacked")
    async def nfl_player_times_sacked(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} was sacked {player.times_sacked} times\n"

        await ctx.send(out_string)

    @nfl_player.command(name="yardslostsacks")
    async def nfl_player_yards_lost_to_sacks(self, ctx, *, player_name: str):
        player_name = player_name.title()
        name = player_name.split(" ")
        if len(name) != 2:
            await ctx.send("Invalid name")
            return

        players = self.nfl_player_name_to_code(name[0], name[1])
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.player_id} lost {player.yards_lost_to_sacks} yards to sacks\n"

        await ctx.send(out_string)

    # get NFL scores on a given date
    @commands.command(name="nflscores", help="displays all NFL scores on the given week number and year.")
    async def nfl_scores(self, ctx, week=None, year=None):
        bad_input_message = "Invalid week/year parameters"
        if week is None or year is None or not week.isdigit() or not year.isdigit():
            await ctx.send(bad_input_message)
            return

        try:
            nfl_games = NFL_Boxscores(int(week), int(year))
        except urllib.error.HTTPError:
            await ctx.send(bad_input_message)
            return

        week_format = f"{week}-{year}"
        games = nfl_games.games.get(week_format)
        out_string = ""
        for game in games:
            # puts the teams' names and scores in the output string
            out_string += f"\n{game.get('away_name')} {game.get('away_score')} - {game.get('home_name')} {game.get('home_score')}"
        # print(nfl_games.games)
        await ctx.send(out_string)

    # get stats for an NBA team
    @commands.group(name="nbateam", help="Parent command to get stats for an NBA team")
    async def nba_team(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid parameters")

    @nba_team.command(name="defensiverebounds", help="get a team's defensive rebounds")
    async def nba_team_def_rebounds(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have {team.defensive_rebounds} defensive rebounds")

    @nba_team.command(name="fieldgoalpercent", help="get a team's percentage of shots made to shots attempted")
    async def nba_team_field_goal_percentage(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have shot {round(team.field_goal_percentage * 100, 1)}%")

    @nba_team.command(name="freethrowpercent", help="get a team's percentage of free throws made to free throws attempted")
    async def nba_team_free_throw_percentage(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have shot {round(team.free_throw_percentage * 100, 1)}% from the foul line")

    @nba_team.command(name="offensiverebounds", help="get a team's offensive rebounds")
    async def nba_team_offensive_rebounds(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have {team.offensive_rebounds} offensive rebounds")

    @nba_team.command(name="oppdefensiverebounds", help="get a team's opponents' defensive rebounds")
    async def nba_team_opp_defensive_rebounds(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name}' opponents have {team.opp_defensive_rebounds} defensive rebounds against them")

    @nba_team.command(name="oppoffensiverebounds", help="get a team's opponents' offensive rebounds")
    async def nba_team_opp_offensive_rebounds(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name}' opponents have {team.opp_offensive_rebounds} offensive rebounds against them")

    @nba_team.command(name="oppfieldgoalpercent", help="get a team's opponents' percentage of shots made to shots attempted")
    async def nba_team_opp_field_goal_percentage(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name}' opponents have shot {round(team.opp_field_goal_percentage * 100, 1)}% against them")

    @nba_team.command(name="oppfouls",
                      help="get the number of personal fouls a team's opponent committed against them")
    async def nba_team_opp_personal_fouls(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name}' opponents have committed {team.opp_personal_fouls} fouls against them")

    @nba_team.command(name="opppoints", help="get the number of points a team has given up")
    async def nba_team_opp_points(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have given up {team.opp_points} points")

    @nba_team.command(name="opp3ptpercent", help="get a team's opponents' percentage of 3 point shots made to shots attempted")
    async def nba_team_opp_three_pt_percentage(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name}' opponents have made {round(team.opp_three_point_field_goal_percentage * 100, 1)}% "
                           f"of 3-point shots against them")

    @nba_team.command(name="opp2ptpercent",
                      help="get a team's opponent's percentage of 2 point shots made to shots attempted")
    async def nba_team_opp_two_point_percentage(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(
                f"The {team.name}' opponents have made {round(team.opp_two_point_field_goal_percentage * 100, 1)}% of "
                f"2-point shots against them")

    @nba_team.command(name="oppturnovers", help="get a team's opponents' number of turnovers")
    async def nba_team_opp_turnovers(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name}' opponents have committed {team.opp_turnovers} turnovers")

    @nba_team.command(name="fouls", help="get a team's number of personal fouls committed")
    async def nba_team_personal_fouls(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have committed {team.personal_fouls} fouls")

    @nba_team.command(name="points", help="get the number of points a team scored")
    async def nba_team_points(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have scored {team.points} points")

    @nba_team.command(name="turnovers", help="get the number of turnovers a team committed")
    async def nba_team_turnovers(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have committed {team.turnovers} turnovers")

    @nba_team.command(name="3ptpercent", help="get a team's percentage of 3 point shots made to shots taken")
    async def nba_team_three_point_percentage(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have made {round(team.three_point_field_goal_percentage * 100, 1)}% of "
                           f"3-point shots ")

    @nba_team.command(name="2ptpercent", help="get a team's percentage of 2 point shots made to shots taken")
    async def nba_team_two_point_percentage(self, ctx, *, team_name: str):
        team = await self.get_nba_team(ctx, team_name)
        if team is not None:
            await ctx.send(f"The {team.name} have made {round(team.two_point_field_goal_percentage * 100, 1)}% of "
                           f"2-point shots ")

    # get stats for a NBA player
    @commands.group(name="nbaplayer", help="Parent command to get stats for a NBA player. Retired players will get career stats.")
    async def nba_player(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid parameters")

    """
    @nba_player.command(name="andones", help="gets the number of times the player was fouled during a shot, made the shot,"
                                             "then made his foul shot")
    async def nba_player_and_ones(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} has {player.and_ones} and ones\n"

        await ctx.send(out_string)

    @nba_player.command(name="birthday", help="gets the player's birth date")
    async def nba_player_birth_date(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} was born on {player.birth_date}\n"

        await ctx.send(out_string)

    @nba_player.command(name="dunks", help="gets the player's number of dunks")
    async def nba_player_dunks(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} has {player.dunks} dunks\n"

        await ctx.send(out_string)
    """

    @nba_player.command(name="contract", help="gets the player's current contract")
    async def nba_player_contract(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name}'s contract:\n{player.contract}\n"

        await ctx.send(out_string)

    @nba_player.command(name="halfcourt", help="gets the player's number of half court shots made")
    async def nba_player_half_court_heaves(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} has made {player.half_court_heaves_made} shots from beyond half court\n"
        await ctx.send(out_string)

    @nba_player.command(name="blocks", help="gets the player's number of blocks")
    async def nba_player_blocks(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} has {player.blocks} blocks\n"
        await ctx.send(out_string)

    @nba_player.command(name="freethrowpercent", help="gets the player's percentage of free throws made")
    async def nba_player_free_throw_percentage(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} shot {round(player.free_throw_percentage * 100, 1)}% from the foul line\n"
        await ctx.send(out_string)

    @nba_player.command(name="minutesplayed", help="gets the player's number of minutes in the game")
    async def nba_player_minutes_played(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} played {player.minutes_played} minutes\n"
        await ctx.send(out_string)

    @nba_player.command(name="fouls", help="gets the player's number of personal fouls committed")
    async def nba_player_personal_fouls(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} committed {player.personal_fouls} fouls\n"
        await ctx.send(out_string)

    @nba_player.command(name="offrebounds", help="gets the player's number of offensive rebounds")
    async def nba_player_offensive_rebounds(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} has {player.offensive_rebounds} offensive rebounds\n"
        await ctx.send(out_string)

    @nba_player.command(name="defrebounds", help="gets the player's number of defensive rebounds")
    async def nba_player_defensive_rebounds(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} has {player.defensive_rebounds} defensive rebounds\n"
        await ctx.send(out_string)

    @nba_player.command(name="points", help="gets the player's points scored")
    async def nba_player_points(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} scored {player.points} points\n"
        await ctx.send(out_string)

    @nba_player.command(name="steals", help="gets the player's number of steals")
    async def nba_player_steals(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} has {player.steals} steals\n"
        await ctx.send(out_string)

    @nba_player.command(name="3ptpercent", help="gets the player's percentage of 3-point shots made")
    async def nba_player_three_point_percentage(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} made {round(player.three_point_percentage * 100, 1)}% of 3-point shots\n"
        await ctx.send(out_string)

    @nba_player.command(name="2ptpercent", help="gets the player's percentage of 2-point shots made")
    async def nba_player_two_point_percentage(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} made {round(player.two_point_percentage * 100, 1)}% of 2-point shots\n"
        await ctx.send(out_string)

    @nba_player.command(name="turnovers", help="gets the number of times the player turned the ball over")
    async def nba_player_turnovers(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} committed {player.turnovers} turnovers\n"
        await ctx.send(out_string)

    @nba_player.command(name="team", help="gets the team the player is on, as an abbreviation")
    async def nba_player_team(self, ctx, *, player_name: str):
        players = self.nba_player_name_to_code(player_name)
        if not players:
            await ctx.send("Invalid player name")
            return

        out_string = ""
        for player in players:
            out_string += f"{player.name} plays for {player.team_abbreviation}\n"
        await ctx.send(out_string)

    # get stats for an NBA game
    @commands.group(name="nbagame", help="Parent command to get stats for a game")
    async def nba_game(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid parameters")

    @nba_game.command(name="location", help="gets the location of the game")
    async def nba_game_location(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:       # check for a valid game
            await ctx.send(f"The game was played at {game.location}")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="date", help="gets the date of the game")
    async def nba_game_date(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(f"The game was played on {game.date}")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="summary", help="displays a summary of the game")
    async def nba_game_summary(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # passing in a bad game code won't return a None game, so check a data member for None
            winner = game.winner
            final_output = ""  # contains the message to send to Discord
            quarter_scores = list(game.summary.values())  # get the points scored in each quarter for each team
            # *****getting NBA team names or abbreviations from a Boxscore either return nothing or an error*****
            if winner == "Home":
                final_output += str(quarter_scores[0]) + f"     P: {game.away_points}\tR: {game.away_total_rebounds}\tA: {game.away_assists}\tS: {game.away_steals}\n"
                final_output += str(quarter_scores[1]) + f"    P: {game.home_points}\tR: {game.home_total_rebounds}\tA: {game.home_assists}\tS: {game.home_steals}\n"
            elif winner == "Away":
                final_output += str(quarter_scores[0]) + f"    P: {game.away_points}\tR: {game.away_total_rebounds}\tA: {game.away_assists}\tS: {game.away_steals}\n"
                final_output += str(quarter_scores[1]) + f"    P: {game.home_points}\tR: {game.home_total_rebounds}\tA: {game.home_assists}\tS: {game.home_steals}\n"
            else:
                await ctx.send("Error retrieving game data")
                return

            final_output += f"Game played at {game.location} on {game.date}"
            await ctx.send(final_output)
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="assists", help="gets both teams' assists")
    async def nba_game_assists(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(f"The away team had {game.away_assists} assists and the home team had {game.home_assists} assists")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="blocks", help="gets both teams' blocks")
    async def nba_game_blocks(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team had {game.away_blocks} blocks and the home team had {game.home_blocks} blocks")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="defensiverebounds", help="gets both teams' number of defensive rebounds")
    async def nba_game_defensive_rebounds(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team had {game.away_defensive_rebounds} defensive rebounds and the home team had "
                f"{game.home_defensive_rebounds} defensive rebounds")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="freethrowattempts", help="gets both teams' number of attempted free throws")
    async def nba_game_free_throw_attempts(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team had {game.away_free_throw_attempts} free throw attempts and the home team had "
                f"{game.home_free_throw_attempts} free throw attempts")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="freethrows", help="gets both teams' number of made free throws")
    async def nba_game_free_throws_made(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team made {game.away_free_throws} free throws and the home team made {game.home_free_throws} free throws")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="offensiverebounds", help="gets both teams' number of offensive rebounds")
    async def nba_game_offensive_rebounds(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team had {game.away_offensive_rebounds} offensive rebounds and the home team had "
                f"{game.home_offensive_rebounds} offensive rebounds")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="fouls", help="gets both teams' number of fouls")
    async def nba_game_personal_fouls(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team had {game.away_personal_fouls} fouls and the home team had {game.home_personal_fouls} fouls")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="points", help="gets both teams' points")
    async def nba_game_points(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team scored {game.away_points} points and the home team scored {game.home_points} points")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="steals", help="gets both teams' steals")
    async def nba_game_steals(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team had {game.away_steals} steals and the home team had {game.home_steals} steals")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="turnovers", help="gets both teams' turnovers")
    async def nba_game_turnovers(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team turned the ball over {game.away_turnovers} times, and the home team turned the ball "
                f"over {game.home_turnovers} times")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="2ptfieldgoals", help="gets both teams' 2-point shots made")
    async def nba_game_two_point_field_goals(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team made {game.away_two_point_field_goals} 2-point baskets, and the home team made "
                f"{game.home_two_point_field_goals} 2-point baskets")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="2ptfieldgoalattempts", help="gets both teams' 2-point shots attempted")
    async def nba_game_two_point_field_goals_attempted(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team attempted {game.away_two_point_field_goal_attempts} 2-point baskets, and the home team "
                f"attempted {game.home_two_point_field_goal_attempts} 2-point baskets")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="3ptfieldgoals", help="gets both teams' 3-point shots made")
    async def nba_game_three_point_field_goals(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team made {game.away_three_point_field_goals} 3-point baskets, and the home team made "
                f"{game.home_three_point_field_goals} 3-point baskets")
        else:
            await ctx.send("Invalid game code")

    @nba_game.command(name="3ptfieldgoalattempts", help="gets both teams' 3-point shots attempted")
    async def nba_game_three_point_field_goals_attempted(self, ctx, game_code: str):
        game = NBA_Boxscore(game_code)
        if game.date is not None:  # check for a valid game
            await ctx.send(
                f"The away team attempted {game.away_three_point_field_goal_attempts} 3-point baskets, and the home team "
                f"attempted {game.home_three_point_field_goal_attempts} 3-point baskets")
        else:
            await ctx.send("Invalid game code")

    @commands.command(name="nbascores", help="displays all NBA scores on the given date")
    async def nba_scores(self, ctx, month=None, day=None, year=None):
        if month is None or day is None or year is None:
            await ctx.send("Invalid date parameters")
            return

        try:
            input_date = datetime(int(year), int(month), int(day))
        except ValueError:
            await ctx.send("Invalid date parameters")
            return

        if input_date > datetime.today():
            input_date = datetime.today()

        today_games = NBA_Boxscores(input_date)
        x = input_date.date()
        xFormat = f"{x.month}-{x.day}-{x.year}"
        games = today_games.games[xFormat]  # gets the value (list of games) for the passed in key (date)

        if not games:
            await ctx.send("There are no games on this date")
            return

        games_date = next(iter(today_games.games))  # gets the key (date) of the entire dict
        await ctx.send(f"Scores for: {games_date}")
        out_string = ""
        for game in games:
            # puts the teams' names and scores in the output string
            out_string += f"\n{game.get('away_name')} {game.get('away_score')} - {game.get('home_name')} {game.get('home_score')}"

        await ctx.send(out_string)


async def setup(client):
    await client.wait_until_ready()
    client.add_cog(Sports(client))
