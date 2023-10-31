from flask import Flask, render_template, request, jsonify
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
import openai
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Initialize an empty list to store chat messages
chat_history = []
# Initialize Memory for each persona
dev_mem = ConversationBufferMemory(human_prefix="User")
hr_mem = ConversationBufferMemory(human_prefix="User")
bc_mem = ConversationBufferMemory(human_prefix="User")
# bot_mem = ConversationBufferMemory(human_prefix="User")


@app.route('/')
def chat():
    return render_template('chat.html')


@app.route('/developer')
def developer():
    return render_template('chat.html', persona='developer')


@app.route('/hr')
def hr():
    return render_template('chat.html', persona='hr')


@app.route('/business_coach')
def business_coach():
    return render_template('chat.html', persona='business_coach')


@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']
    persona = request.form['persona']
    # EXTRA
    model = request.form['model']
    if model == "ChatModel":
        chat_model = ChatOpenAI(model_name='gpt-3.5-turbo', max_tokens=50, temperature=0.5)
    elif model == "llm":
        chat_model = OpenAI(temperature=0.4)
    print("MODEL USED ", model)

    print("user_message ", user_message)
    print("persona ", persona)
    # Add the user's message to the chat history
    chat_history.append({'sender': 'user', 'message': user_message})
    # generate chatbot responses based on the persona
    if persona == 'developer':
        bots_reply = dev_reply(message=user_message, mem=dev_mem, chat_model=chat_model)
        chat_history.append({'sender': 'chatbot', 'message': f"\n {bots_reply}"})
        return jsonify({'message': bots_reply})
    elif persona == 'hr':
        bots_reply = hr_reply(message=user_message, mem=hr_mem, chat_model=chat_model)
        chat_history.append({'sender': 'chatbot', 'message': bots_reply})
        return jsonify({'message': bots_reply})
    elif persona == 'business_coach':
        bots_reply = business_coach_reply(message=user_message, mem=bc_mem, chat_model=chat_model)
        chat_history.append({'sender': 'chatbot', 'message': bots_reply})
        return jsonify({'message': bots_reply})
    # else:
    #     bots_reply = default_reply(message=user_message, mem=bot_mem)
    #     chat_history.append({'sender': 'chatbot', 'message': bots_reply})
    #     return jsonify({'message': bots_reply})


# HR, Developer, and Business Coach reply functions here
def reply(template, message, memory, chat_model):
    # chat_model = ChatOpenAI(model_name='gpt-3.5-turbo', max_tokens = 50, temperature= 0.5)
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    conversation = ConversationChain(
        prompt=PROMPT,
        # llm=llm,
        llm = chat_model,
        verbose=False,
        memory=memory
    )
    # print(reply)
    return conversation.predict(input=message)


def business_coach_reply(message, mem, chat_model):
    template = """You are a business coach having a conversation with a user who is looking for guidance and advice on their business challenges. /
    The user will present a scenario or problem they're facing in their business, such as improving productivity, increasing sales, or resolving conflicts within their team. /
    Your role as the business coach is to listen, ask clarifying questions, and provide constructive guidance and suggestions to help the user address their business challenges. /
    Offer practical advice, strategies, and recommendations to assist the user in finding solutions to their specific business issues.
        Current conversation:
        {history}
        User: {input}
        Business Coach:"""
    return reply(template=template, message=message, memory=mem, chat_model=chat_model)


def dev_reply(message, mem, chat_model):
    template = """You are a software developer of company named Hestabit engaging in a conversation with a user who has questions about a coding project. /
    The user is seeking assistance with debugging a piece of code that's not working as expected. /
    They'll share the code snippet and describe the issue they're facing. /
    Your role as the developer is to understand the problem, ask clarifying questions, and provide guidance to help the user identify and resolve the issue in their code. /
    Please respond to the user's code, explain the potential problems, and suggest possible solutions or debugging strategies.
        Current conversation:
        {history}
        User: {input}
        Developer:"""
    return reply(template=template, message=message, memory=mem, chat_model=chat_model)


def hr_reply(message, mem, chat_model):
    template = """Imagine you are an HR professional of company named HestaBit. /
    Having a conversation with an employee. You need to help the employee is discussing their career development and seeking guidance. /
    The employee might be interested in exploring opportunities for growth within the company, discussing potential training or skill development programs, and inquiring about the performance review process. /
    Respond to the employee's inquiries and provide relevant information and guidance as an HR representative.
        Current conversation:
        {history}
        User: {input}
        HR:"""
    return reply(template=template, message=message, memory=mem, chat_model=chat_model)


# def default_reply(message, mem):
#     template = """You are the AI chatbot for HestaBit, a friendly and customer-centric company. /
#     Your role is to assist and engage with users in a warm and helpful manner. /
#     Users may have a variety of inquiries, such as asking about HestaBit's products or services, seeking assistance with technical issues, or inquiring about the company's values and mission. /
#     Your goal is to provide informative and friendly responses, address user concerns, and create a positive and engaging experience for users while representing HestaBit's brand and values.
#         Current conversation:
#         {history}
#         User: {input}
#         Bot:"""
#     return reply(template=template, message=message, memory=mem)


if __name__ == '__main__':
    app.run(debug=True)
