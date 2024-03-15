from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_community.callbacks import get_openai_callback
from dotenv import load_dotenv
import json
from .prompts import MCQ_GEN_PROMPT, MCQ_OUTPUT_FORMAT

load_dotenv()


def get_openai_llm_from_key(key):
    try:
        return ChatOpenAI(openai_api_key=key)
    except:
        return False


class MCQGen():
    def __init__(self, openai_api_key) -> None:
        self.llm = get_openai_llm_from_key(openai_api_key)

    def test_key(self):
        try:
            self.llm.invoke("test")
            return True
        except:
            return False

    def prepare_chains(self):

        mcq_gen_prompt = PromptTemplate(
            input_variables=["text", "number",
                              "tone", "response_json"],
            template=MCQ_GEN_PROMPT
        )

        mcq_gen_chain = LLMChain(
            llm=self.llm, prompt=mcq_gen_prompt, output_key="quiz", verbose=True)

        self.final_chain = SequentialChain(
            chains=[mcq_gen_chain],
            input_variables=["text", "number", "tone", "response_json"],
            output_variables=["quiz"], verbose=True,
        )

    def get_json_results(self,text_block, number_of_questions, difficulty):
        if not self.final_chain:
            return
        
        with get_openai_callback() as cb:
            response = self.final_chain(
                {
                    'text': text_block,
                    'number': number_of_questions,
                    'tone': difficulty,
                    'response_json': json.dumps(MCQ_OUTPUT_FORMAT)
                }
            )
        return json.loads(response.get('quiz').strip())
