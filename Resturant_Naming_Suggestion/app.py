from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnableParallel

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash',temperature = 0.7)

## example 1: (prompt using template)
# template = "Suggest me 3 {origin} restaurant name"
# prompt_template = ChatPromptTemplate.from_template(template)

# prompt = prompt_template.invoke({"origin" : "bengali"})
# response = model.invoke(prompt)
# print(response.content)

#-----------------------------

## example 2: (prompt using messages / tuple)
# messages = [
#     ("system", "You're AI assistance, Name is Hogo"),
#     ("human", "Suggest me 3 {origin} restaurant name")
# ]
# prompt_template = ChatPromptTemplate.from_messages(messages)

# prompt = prompt_template.invoke({"origin" : "bengali"})
# response = model.invoke(prompt)
# print(prompt)
# print(response.content)

#-----------------------------

## example 3: (using LangChain Expression language)
# messages = [
#     ("system", "You're AI assistance, Name is Hogo"),
#     ("human", "Suggest me {count} {origin} restaurant name")
# ]
# prompt_template = ChatPromptTemplate.from_messages(messages)

# chain = prompt_template | model | StrOutputParser()
# response = chain.invoke({"count" : 2,"origin" : "bengali"})
# print(f'Response :: {response}')

# ----------------------
# Extended chaining
# ----------------------

# restaurant_title_prompt = PromptTemplate.from_template("Suggest me one {origin} restaurant name only")
# restaurant_title_chain = restaurant_title_prompt | model | StrOutputParser() 

# # Wrap the title string into a dict for downstream steps
# wrap_title = RunnableLambda(lambda title: {"title": title})

# # Print the restaurant title
# printing_title = RunnableLambda(lambda x: print(f"Restaurant Title: {x['title']}") or x)


# restaurant_menus_prompt = PromptTemplate.from_template("Suggest me six food items name only of restaurant {title}")
# restaurant_menus_chain = (
#     restaurant_title_chain
#     | wrap_title
#     | printing_title
#     | restaurant_menus_prompt
#     | model
#     | StrOutputParser()
# )
# response = restaurant_menus_chain.invoke({'origin' : 'bengali'})
# print(f"Menus : {response}")

# ----------------------
# Parallel chaining
# ----------------------

# naming_chain = ChatPromptTemplate.from_template("Suggest one name of {origin} restaurant only") | model | StrOutputParser()
# title = naming_chain.invoke({'origin' : 'bengali'})
# print(f"Title : {title}")

# meal_menu_chain = ChatPromptTemplate.from_template("Suggest 4 meal item name only of {title} restaurant") | model | StrOutputParser()
# snacks_menu_chain = ChatPromptTemplate.from_template("Suggest 4 snacks item name only of {title} restaurant") | model | StrOutputParser()

# parallel_chain = RunnableParallel(meals = meal_menu_chain, snacks = snacks_menu_chain)

# res = parallel_chain.invoke({'title' : title})
# print(f"Meal items : {res['meals']}")
# print(f"Snacks items : {res['snacks']}")