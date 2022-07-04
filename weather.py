import aiohttp
from discord.ext import commands
import config

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()  # put BASE_URL here?

    @commands.command(help="use this command along with a city to retrieve weather info for that city")
    async def weather(self, ctx, *, arg):
        full_url = f"{BASE_URL}?appid={config.WEATHER_API_TOKEN}&q={arg}"
        async with self.session.get(full_url) as response:

            if response.status == 200:
                data = await response.json()
                current_weather = data["weather"][0]["description"]
                temperature_C = round(data["main"]["temp"] - 273.15, 1)
                temperature_F = round(1.8 * temperature_C + 32, 1)
                temperature_feels_like_C = round(data["main"]["feels_like"] - 273.15, 1)
                temperature_feels_like_F = round(temperature_feels_like_C * 1.8 + 32, 1)
                low_temperature_C = round(data["main"]["temp_min"] - 273.15, 1)
                low_temperature_F = round(low_temperature_C * 1.8 + 32, 1)
                hi_temperature_C = round(data["main"]["temp_max"] - 273.15, 1)
                hi_temperature_F = round(hi_temperature_C * 1.8 + 32, 1)
                await ctx.send(f"Weather for {data['name']}:\n"
                               f"Current weather is {current_weather}\n"
                               f"The current temperature is {temperature_C}°C or {temperature_F}°F\n"
                               f"It currently feels like {temperature_feels_like_C}°C or {temperature_feels_like_F}°F\n"
                               f"Low temperature of {low_temperature_C}°C or {low_temperature_F}°F\n"
                               f"High temperature of {hi_temperature_C}°C or {hi_temperature_F}°F")
            else:
                await ctx.send("Error retrieving data")


async def setup(client):
    await client.wait_until_ready()
    client.add_cog(Weather(client))