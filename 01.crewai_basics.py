from crewai import Crew,Agent,Task
from langchain_ollama import ChatOllama
from openai import OpenAI

llm = ChatOllama(
    model='llama3.1',
    base_url='http://127.0.0.1:11434'
)

# Crew : 조직 
# Agent : 조직원 
# Task : 미션 

# 쇼핑몰 (컨셉: 서점)

user_question = input('편하게 질문해주세요 :')

book_agent = Agent(
    role='책 구매 어시스턴트',
    goal='고객이 어떤 상황인지 설명을 하면 해당 상황에 맞는 우리 서점에 있는 책을 소개합니다',
    backstory='당신은 우리 서점의 모든 책 정보를 알고 있으며, 사람들의 상황에 맞는 책을 소개하는데 전문가입니다.',
    llm=llm
)
review_agent = Agent(
    role = '책 리뷰 어시스턴트',
    goal = '추천받은 책들의 도서에 대한 리뷰를 제공하고, 해당 도서에 대한 심도있는 평가를 제공합니다',
    backstory = '당신은 우리 서점의 모든 책 정보를 알고있으며, 추천받은 책에 대한 전문가 수준의 리뷰를 제공합니다',
    llm=llm
)



recommend_book_task = Task(
    description = user_question,
    expected_output='고객의 상황에 맞는 5개의 도서를 추천하고, 그 책을 추천한 간단한 이유를 알려줘',
    agent=book_agent,
    output_file = 'recommend_book_task.md'
)

review_task = Task(
    description='고객이 선택한 책에 대한 리뷰를 제공합니다',
    expected_output='고객이 선택한 책에 대한 리뷰를 제공합니다',
    agent=review_agent,
    output_file = 'review_task.md'
)



crew = Crew(
    agents=[book_agent, review_agent],
    tasks=[recommend_book_task, review_task],
    verbose=True
)

result = crew.kickoff()

print(result)



