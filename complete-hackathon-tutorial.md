# Building a Startup Launch Team using CompleteAI

Learn how you can create 3 agents that work together to manage a SaaS product

We are going to Build 3 collaborating AI Agents that work together to take a startup idea from concept to launch-ready — including market research, product definition, pitch deck, and landing page copy.

What you'll build:

• Research Agent — Analyzes competitors, identifies market gaps, summarizes findings
• Product Agent — Defines features, user flows, and technical requirements
• Marketing Agent — Creates pitch deck content, landing page copy, and go-to-market strategy

Prerequisites: 
* Complete.dev account
* Basic familiarity with Agent Builder

Step 1: Set Up Your Shared Workspace: 

1. Create a new workspace in Complete.dev called "Startup Launch Team"
2. FIll in the Space Name, Description & members that you would like to add. 
2. Invite your teammates (if any)

![Click on "Create Space" button]()

![Fill in the details of your space]()

Step 2: Build the Research Agent: 

Go to your ``dashboard`` button 

Click on ``Add member`` 

![Clicking on dashboard & clicking on add member button]()

Type in ``Agent Builder``

![Typing and selecting Agent Builder]()

Add the agent builder and go back to general chat, then send in the prompt: 
```bash
Create the Agent called "Market Researcher" that is responsible for analyzing competitors, identifying market trends, and finding gaps in the market. This is the system prompt:
You are a market research analyst. Your job is to analyze competitors, identify market trends, and find gaps in the market. Always provide structured output with:

Executive Summary
Competitor Analysis (3-5 key players)
Market Gap/Opportunity
Recommendations
Save all outputs to the /research folder.
```

But fist of all ensure you've inserted your preferred model API key, in our case we will use Gemini API 

Go to [google ai studio](https://aistudio.google.com/api-keys) and get your API Key there, then send it as part of the prompt: 
```bash
GOOGLE_API_KEY=xxxxxxxx
``` 

Once it's done, this is what you'll see as the output 

![Agent builder completing the Research agent]()

When you go to ``Code`` --> ``General`` --> ``market_researcher.py`` you can see and verify the agent code that has just been created for your Researcher Agent. 

![Research Agent Final code]()

#### Testing your market research agent: 

Agent Builder provides a URL to a live test application, if it hasn't, you can specifically prompt it to do that. 

Now you can test the agent using the prompt: 
```bash
Research the AI scheduling assistant market. Who are the main competitors? What features are missing? Save your analysis to /research/scheduling-market.md
```

![Testing market research agent - sending the prompt]()

![Final results of market research prompt]()

#### Step 3: Build the Product Agent

Now let's go back to the ``#general`` chat and build the product agent. This is the prompt you'll use: 

```bash 
Now let's build the product agent, this is the system prompt: 
You are a product manager and technical architect. Your job is to transform market research into concrete product specifications. Given research input, you will:
- Define core features (MVP scope)
- Create user stories
- Design user flows
- Define technical requirements

Always read relevant research from /research before starting.
Save outputs to /product/ folder.
```

