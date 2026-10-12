# 🌤️ The Easiest AI Agent You Can Build: a Weather Assistant with Mistral

Here's the easiest possible agent: one tool, one file, plain Python, free-tier APIs. There are no frameworks and no SDK magic, so you can see every moving part.

If you can run `pip install` and use a text editor, you can build this.

## What you'll build

A terminal agent you can talk to in plain language:

```
You: Should I take an umbrella in Lisbon today?
  [agent calls get_weather(city='Lisbon')]
  [tool returned: Weather in Lisbon: 16.2°C (feels like 14.8°C), ...]
Agent: Yes, there's a 70% chance of rain today. Take a small umbrella. 🌂

You: What is 12 * 34?
Agent: 408
```

It decides on its own whether it needs live data (a tool call) or can just answer. That decision, made by the model and not by your code, is what makes it an agent rather than a script.

## The big idea in one paragraph

A script does what you hardcoded. An agent does what it decides. You give the model a menu of tools (functions you wrote). It reads your question, and if it needs real-world data it asks your code to run the right function with the right arguments, gets the result back, and answers. The loop is: model thinks, calls your tool, gets results, answers.

## Repo structure

```
ai-umbrella-agent/
├── README.md
├── step1_fetch_weather.py     <- what's an API? (no AI yet)
├── step2_add_the_brain.py     <- adding an LLM to the data
├── step3_the_agent.py         <- the real agent with tool use
├── requirements.txt
└── .gitignore
```

## Prerequisites

- Python 3.10+ and a terminal
- `pip install -r requirements.txt`
- A free Mistral account: sign up at [console.mistral.ai](https://console.mistral.ai), activate the free **Experiment** plan, and create an API key. Never paste the key into code. Store it as an environment variable.

**Set the key (same terminal you'll run from):**

```bash
# macOS / Linux
export MISTRAL_API_KEY="your-key-here"
```

```powershell
# Windows PowerShell
$env:MISTRAL_API_KEY="your-key-here"
```

**Privacy note:** on the free Experiment plan, your prompts may be used by Mistral to improve its models. Don't send anything private.

**Model name:** the scripts default to `ministral-8b-latest`. Model names change over time. If you get a "model not found" error, list the models your key can use and set one:

```bash
curl -s https://api.mistral.ai/v1/models -H "Authorization: Bearer $MISTRAL_API_KEY"
export MISTRAL_MODEL="the-model-id-you-picked"
```

---

## Step 1: What's an API? Fetch weather without AI (5 minutes)

An API is a waiter: you order from a fixed menu in a fixed format, and the kitchen sends back data. We use [Open-Meteo](https://open-meteo.com), which is free and needs no key.

Run it:

```bash
python step1_fetch_weather.py
```

You just called an API and parsed its JSON answer.

## Step 2: Add the brain, let Mistral summarize the data

Now we make a second API call, to Mistral's chat API, and put the weather data inside the prompt. This is the pattern behind almost every AI app: gather data, then ask the model.

```bash
python step2_add_the_brain.py
```

Your program now talks to two APIs and combines them.

## Step 3: The real agent, the model decides when to call your code

The big inversion: instead of your code deciding "fetch weather, then ask," you register your weather function as a tool and let the model decide whether and how to call it. A geocoding call lets the agent handle any city by name.

```bash
python step3_the_agent.py
```

Try:

- `What's the weather in Berlin?` and watch it call the tool
- `Should I take an umbrella in Lisbon today?` for a tool call plus judgment
- `What is 12 * 34?` with no tool call, because it decides
- `quit`

## Lessons worth knowing

- **429 errors on the free tier.** Free-plan rate limits are low and are set per organization. Your exact limits are on the Limits page of the Mistral console. The scripts retry with increasing waits instead of hammering the API in a fast loop.
- **Jailbreak test.** With a soft system prompt, models can be talked into ignoring instructions. The hard guardrails live in code: a tool allow-list, argument validation, request timeouts, and a cap on tool-call rounds. Even a fully jailbroken model here can only look up city names. You don't make agents safe by making the model un-trickable. You make jailbreaks harmless by granting the least power that does the job.
- **Key hygiene.** The key lives in an environment variable, never in code or in git history.

## Next steps

- More tools, each with its own input validation
- Swap raw `requests` for the official [Mistral SDKs](https://docs.mistral.ai/resources/sdks)
- A small web UI on top of the agent loop

## Data, licensing and attribution

Weather data by [Open-Meteo.com](https://open-meteo.com), licensed CC BY-NC 4.0. The free Open-Meteo API is for non-commercial use only and has fair-use call limits (see their [terms](https://open-meteo.com/en/terms)). This repo is for learning. If you build a commercial product, use a paid Open-Meteo plan.

LLM: [Mistral API](https://docs.mistral.ai).