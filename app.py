import gradio as gr
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import sqlite3
from pathlib import Path

class SQLAgentApp:
    def __init__(self):
        # Initialize database connection
        data_path = Path("/home/sonujha/rnd/text2sql/dbsetup/")
        db_uri = f"sqlite:///{data_path/'user_features.db'}"
        self.db = SQLDatabase.from_uri(db_uri)

        # Initialize LLM and agent
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.agent = create_sql_agent(
            self.llm,
            db=self.db,
            agent_type="openai-tools",
            verbose=True
        )

    def query_agent(self, query, history):
        try:
            # Execute query through agent
            response = self.agent.invoke(query)
            return response["output"]
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    # Initialize the app
    app = SQLAgentApp()

    # Create Gradio interface
    with gr.Blocks(title="SQL Database Agent") as interface:
        gr.Markdown("# SQL Database Agent")
        gr.Markdown("Ask questions about your database in natural language.")

        chatbot = gr.Chatbot(
            show_label=False,
            height=400
        )

        with gr.Row():
            query_input = gr.Textbox(
                placeholder="Ask a question about your database...",
                label="Query",
                scale=4
            )
            submit_btn = gr.Button("Submit", scale=1)

        gr.Examples(
            examples=[
                "How many total users are there?",
                "Show me the user distribution by country",
                "What's the average age of users?",
                "List the top 5 most common user features"
            ],
            inputs=query_input
        )

        def respond(message, chat_history):
            response = app.query_agent(message, chat_history)
            chat_history.append((message, response))
            return "", chat_history

        submit_btn.click(
            respond,
            inputs=[query_input, chatbot],
            outputs=[query_input, chatbot]
        )
        query_input.submit(
            respond,
            inputs=[query_input, chatbot],
            outputs=[query_input, chatbot]
        )

    # Launch the app
    interface.launch(share=True)

if __name__ == "__main__":
    main()
