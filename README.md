# Maury Bot

A Discord bot that role-plays as **Captain Maury**, a seafaring ghost pirate.
It uses OpenAI (ChatGPT / DALL·E) for in-character text and images, Reddit for
live wrestling-thread commentary, and a pluggable **text-to-speech (TTS)** layer
that speaks Maury's responses in a voice channel.

## TTS Providers

The bot supports two interchangeable TTS backends, selected by a single config
flag. Both share the same code path, so playback behaves identically regardless
of which one is active:

| Provider | Default | Endpoint / SDK |
| --- | --- | --- |
| **60db** | ✅ yes | `POST https://api.60db.ai/tts-synthesize` |
| **ElevenLabs** | no | `elevenlabs` Python SDK |

Switch providers with the `tts_provider` field in `config.json`
(`"60db"` or `"elevenlabs"`) — no code change required.

## Configuration

Create a `config.json` in the project root (it is gitignored — it holds your
secrets):

```json
{
  "token": "your-discord-bot-token",
  "openai_api_key": "sk-...",

  "tts_provider": "60db",

  "sixtydb_api_key": "sk_live_...",
  "sixtydb_voice_id": "your-60db-voice-uuid",

  "elevenlabs_api_key": "your-elevenlabs-key"
}
```

| Key | Required when | Notes |
| --- | --- | --- |
| `token` | always | Discord bot token |
| `openai_api_key` | always | Powers `!speak` and `!smark` text generation |
| `tts_provider` | optional | `"60db"` (default) or `"elevenlabs"` |
| `sixtydb_api_key` | provider = 60db | 60db API key (`sk_live_...`) |
| `sixtydb_voice_id` | provider = 60db | Voice UUID — see below |
| `elevenlabs_api_key` | provider = elevenlabs | ElevenLabs API key |

### Getting your 60db `voice_id`

List your voices and copy the `voice_id` you want for Maury:

```bash
curl https://api.60db.ai/myvoices \
  -H "Authorization: Bearer your-api-key"
```

Each entry in `data[]` has a `voice_id` (UUID) and a `name`.

## Commands

| Command | Description |
| --- | --- |
| `!speak <message>` | Maury generates an in-character reply (ChatGPT) and speaks it |
| `!recite <message>` | Maury speaks the provided text verbatim |
| `!smark <thread_url>` | Summarizes a live r/SquaredCircle thread in smark style and speaks it |

You must be in a voice channel for the bot to join and play audio.

## Running

```bash
pip install -e .
python -m maury_bot
```

`ffmpeg` must be installed and on your `PATH` (used to transcode audio for
Discord voice playback).

## How TTS is wired

```
cogs/voice.py            !speak / !recite / !smark
   └─ services/tts.py    get_tts_audio()  ← reads config["tts_provider"]
        ├─ services/sixtydb.py     get_sixtydb_audio()   (60db, default)
        └─ services/elevenlabs.py  get_elevenlabs_audio() (ElevenLabs)
```

- `services/tts.py` is the provider dispatcher. It picks the backend from
  `tts_provider` and wraps any provider error in a single `TTSError`.
- Both backends expose the same `get_*_audio(bot, message)` signature, return a
  discord `FFmpegPCMAudio` source, and use a `tenacity` retry policy
  (3 attempts, exponential backoff).
- 60db voice tuning (`stability=30`, `similarity=85` on a 0–100 scale) mirrors
  the ElevenLabs settings so Maury sounds consistent across providers.
