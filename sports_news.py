from openai import OpenAI, AsyncOpenAI
import os
import asyncio
import pandas as pd
from agents import Agent, Runner, WebSearchTool, trace
from pathlib import Path
import load_dotenv

load_dotenv.load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)
favorite_teams = ["Los Angeles Lakers", "Polonia Warsaw", "Radomiak Radom", "Znicz Pruszkow"]

async def get_team_summary(team):
    response = await client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful sports news assistant."},
            {"role": "user", "content": f"Based on latest news about '{team}' and give me one interesting update in a single sentence."}
        ]
    )
    return {
        "Team": team,
        "News": response.choices[0].message.content.strip(),
        "Link": None  # Web search not available in this simple version
    }

async def main():
    results = []
    for team in favorite_teams:
        print(f"🔍 Getting news for {team}...")
        summary = await get_team_summary(team)
        results.append(summary)

    # Save to /app
    df = pd.DataFrame(results)
    os.makedirs("output", exist_ok=True)
    output_path = Path("output/") / "team_news_summary.xlsx"
    df.to_excel(output_path, index=False)
    print(f"\n News saved to '{output_path}'")

if __name__ == "__main__":
    asyncio.run(main())