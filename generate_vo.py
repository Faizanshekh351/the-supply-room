import asyncio
import edge_tts
import os

scenes_vo = [
    {
        "id": 1,
        "text": "The house does not invite. The house admits. You begin in the Waiting Room. You sign, you verify, and you wait. When your verdict reads Admitted, you take your TMF Pass to the desk."
    },
    {
        "id": 2,
        "text": "At the Subscription Desk, zero point zero one ETH purchases a chair. The chair confers a Seat. Four thousand and one positions divided across five syndicates. Every cent from the mint flows directly into the five vaults to build treasury capital from day one."
    },
    {
        "id": 3,
        "text": "Notice the floor beside each chair. That is an ERC 6551 token bound account. The portrait is not a picture; it is a smart account. Whatever the fund earns drops directly into the briefcase, held in kind, unliquidated."
    },
    {
        "id": 4,
        "text": "Holding a chair is not enough. You enroll with TMF tokens to take your Seat. Half are burned, half are locked in the treasury. Every Friday at twenty hundred hours UTC, the Proxy Ballot opens. You vote on asset allocation, vault splits, and the burn rate."
    },
    {
        "id": 5,
        "text": "On Monday, trades settle. Yield arrives in kind, placed directly into your briefcase. If you sell the chair, the briefcase travels with it to the next owner. If you keep the chair, the ledger remains open."
    },
    {
        "id": 6,
        "text": "The NFT is not the product. The fund is. Take your seat."
    }
]

os.makedirs("audio", exist_ok=True)

async def generate():
    voice = "en-US-ChristopherNeural" # Deep, calm, authoritative, low register
    for sc in scenes_vo:
        out_file = f"audio/scene_{sc['id']}.mp3"
        print(f"Generating VO for Scene {sc['id']}...")
        # Rate -8%, pitch -5Hz for dry, institutional, deadpan cadence
        communicate = edge_tts.Communicate(sc['text'], voice, rate="-8%", pitch="-5Hz")
        await communicate.save(out_file)
        print(f"Saved {out_file}")

asyncio.run(generate())
