from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import os



#Azure openAI API
##Setup your AzureOpenAI credentials in Environment before using it
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_DEPLOYMENT_ENDPOINT = os.environ["OPENAI_API_BASE"]
OPENAI_DEPLOYMENT_NAME = os.environ["OPENAI_DEPLOYMENT_NAME"]
OPENAI_MODEL_NAME = os.environ["OPENAI_MODEL_NAME"]
OPENAI_DEPLOYMENT_VERSION = os.environ["OPENAI_API_VERSION"]




class AgentHead():

    def __init__(self, n_breakups):
        self.response_schema = []
        for i in range(0,n_breakups):
            self.response_schema.append(ResponseSchema(name=str(i), description=f" Sub-task number {i} of the given task"))
        

        self.llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
                            model_name=OPENAI_MODEL_NAME,
                            openai_api_base=OPENAI_DEPLOYMENT_ENDPOINT,
                            openai_api_version=OPENAI_DEPLOYMENT_VERSION,
                            openai_api_key=OPENAI_API_KEY, verbose=True, temperature=0.0)
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas=self.response_schema)
        self.format_instructions = self.output_parser.get_format_instructions()
        self.template = f"""Divide the given task into {n_breakups} simpler and short subtasks, which should be done sequentially to achieve the main task. 
    """
        self.template = self.template + "{format_instructions}\nHere is the user's task {user_task}."

        self.prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(template=self.template)
            ],
            input_variables=["user_task"],
            partial_variables={"format_instructions": self.format_instructions}

        )
        

        
    def get_response(self,user_task):

        _input = self.prompt.format_prompt(user_task=user_task)
        output = self.llm(_input.to_messages())
        return (self.output_parser.parse(output.content))


if __name__ == "__main__":

    obj = AgentHead(8)
    print(obj.get_response(user_task="wash my dirty pile of cloths"))
