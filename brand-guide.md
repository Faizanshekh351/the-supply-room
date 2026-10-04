# The Mutual Fun, for people making things

The house guide, cut down for somebody outside the building. Generated
by art:supplies from the same files the site itself reads, so nothing
here can quietly stop being true.

## The terms

Take these and make things. Posts, memes, videos, whatever your machine makes of them, paid work included. Do not mint them or sell them as a collection of your own, and do not use them to suggest TMF has endorsed you or to pass yourself off as us.

## The idea

A 1987 annual report that became an NFT collection. Warm paper, ink,
oxblood, brass. Everything is furniture in an office building: rooms,
desks, sheets of paper, rubber stamps, a guest book at the door. Nothing
is neon and nothing is cold.

## Color

| Color | Hex | What it is |
| --- | --- | --- |
| The Argon Fund | `#49698C` | Noble, inert, and unmoved by the news. |
| The Bogle Fund | `#4E8A5A` | Buys the whole haystack. |
| The Smaug Fund | `#9C5248` | Sleeps on the pile and knows every coin in it. |
| The Midas Fund | `#B9902F` | Everything it touches, marked to gold. |
| The Vladd Fund | `#6E5D8C` | Buys when there is blood in the streets. |
| Paper | `#F6EFE3` | The wall everything hangs on. |
| Ink | `#211B14` | Every word in the building. |
| Oxblood | `#7A2E2E` | The stamp, the seal, the serious line. |
| Gold foil | `#D4AF37` | The rare frame, and nothing that is not rare. |

The five funds each own a color and a wall. After Hours is the dark
theme, and its values are their own set rather than the light ones
dimmed. Both are in `tokens.json`.

## Type

| Role | Face | Where it goes |
| --- | --- | --- |
| Display | Libre Caslon Text | Headlines, fund names, certificate headers |
| Body | Source Serif 4 | Paragraphs and anything read at length |
| Figures | IBM Plex Mono | Every number, tabular |
| Labels | Source Serif 4, small caps, letterspaced | Section labels and stamps |

All three are under the SIL Open Font License, and all three are on
Google Fonts. The house serves its own copies and never a font CDN.

## The art

Every portrait is 64 by 64 pixels from a palette of 64 colors, stored as
bytes in a sealed contract on chain. The chain draws the picture itself,
as an SVG of one rect per run of color, with no smoothing anywhere. If
you scale one up, scale it by a whole number and turn smoothing off.
The `.svg` files in this kit are the exact markup the chain emits.

## Voice

Plain, dry, and never excited. The house admits, it does not invite. It
says what a thing is and then stops. No exclamation marks, no hype, and
no dashes: the house writes with commas, colons and full stops, and
never an em dash or an en dash.
