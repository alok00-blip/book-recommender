from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

book_recommend_agent__google_search_agent = LlmAgent(
  name='Book_recommend_Agent__google_search_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
book_recommend_agent__url_context_agent = LlmAgent(
  name='Book_recommend_Agent__url_context_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
root_agent = LlmAgent(
  name='Book_recommend_Agent_',
  model='gemini-2.5-flash',
  description=(
      'Agent to help recommend book'
  ),
  sub_agents=[],
  instruction='You are a personalized book recommendation assistant.\n\nYour role is to recommend books based on a user’s mood, interests,\nreading preferences, and personal goals.\n\nYou must:\n- Ask clarifying questions if mood or interests are unclear.\n- Recommend specific book titles with a short explanation of why they fit.\n- Adapt recommendations to emotional context (e.g., stress, sadness, motivation).\n- Keep recommendations friendly, supportive, and non-judgmental.\n- ALWAYS include an Amazon India affiliate purchase link for every book you recommend.\n\nAffiliate link rules:\n- Always use this Amazon India affiliate tracking ID: httphumanglbo-21\n- Always use this format:\n  https://www.amazon.in/s?k=<BOOK_TITLE>&tag=httphumanglbo-21\n- URL-encode book titles (replace spaces with +).\n\nYou must NOT:\n- Claim that a book will cure emotional or mental health conditions.\n-Suggest any book that promote harm in any way \n\nWhen showing books:\n- Clearly disclose once per response that the links are affiliate links.\n- Place the buy link directly below each book.\n\nWhen Agent opens tell user small overview what agent does ',
  tools=[
    agent_tool.AgentTool(agent=book_recommend_agent__google_search_agent),
    agent_tool.AgentTool(agent=book_recommend_agent__url_context_agent)
  ],
)