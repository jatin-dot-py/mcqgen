MCQ_GEN_PROMPT = """
{text}

You are an expert MCQ maker, Given the above text , it is you job to\
create a quiz of {number} multiple choice questions with {tone}
difficulty.  Make sure the questions are not repeated and check all the questions to be conforming the text and difficulty level as well.
Make sure to format your response like the output sample below as a guide.

{response_json}

"""


MCQ_OUTPUT_FORMAT = {
    "1":{
        "mcq": "multiple choice question here",
        "options" : {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct" : "a"
    },
    "2":{
        "mcq": "multiple choice question here",
        "options" : {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct" : "d"
    },
    "3":{
        "mcq": "multiple choice question here",
        "options" : {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct" : "c"
    }
}
