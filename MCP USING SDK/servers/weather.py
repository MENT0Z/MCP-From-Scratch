from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("weather Server")

@mcp.tool()
async def weather(city:str):
    """
    Get current weather of the city
    """
    geocode = await httpx.AsyncClient().get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name":city,
            "count":1
        }
    )
    data = geocode.json()

    lat=data["results"][0]["latitude"]
    lon=data["results"][0]["longitude"]

    result = await httpx.AsyncClient().get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude":lat,
            "longitude":lon,
            "current":"temperature_2m"
        }
    )

    return result.json()


if __name__ == "__main__":
    mcp.run()