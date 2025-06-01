import gen_ai_web_server.llm_server as llm_server
import gen_ai_web_server.llm_client as llm_client

client_phi = llm_client.Client()
client_gem = llm_client.GeminiClient()
client_oai = llm_client.OpenAIClient()

human_response_1 = """Fruits are important sources of vitamins and carbohydrates like fiber and sugar. They are low in calories and naturally sweet. Fruits and their juices are good sources of water, too.

Different fruits contain different vitamins, so it is important to eat a variety of fruits. Mangoes, papayas, melons and citrus fruits, like oranges and grapefruit, are high in vitamin C. Cantaloupe, apricots, peaches, and nectarines are sources of vitamin A.

Whole fruits like apples and grapes contain more fiber than fruit juices and sauces, like applesauce and grape juice. Dried fruits like figs, prunes and raisins are good sources of fiber, too. Canned fruits packed in syrup have a lot of added sugar. They are higher in calories than fresh fruits. When you shop for canned fruits, look for fruit that is packed in juice instead of syrup."""

human_response_2 = """Fruit and vegetables should be an important part of your daily diet. They are naturally good and contain vitamins and minerals that can help to keep you healthy. They can also help protect against some diseases.

Most Australians will benefit from eating more fruit and vegetables as part of a well-balanced, healthy diet and an active lifestyle. There are many varieties of fruit and vegetables available and many ways to prepare, cook and serve them."""

human_response_3 = """Fruits are natures candy. They provide many of the required vitamins and minerals.
They are also good to eat and come in a wide variety of flavours.
Finally, they are amazing to look at with vibrant colours."""

human_response_4 = """Fruits are natures candy. They provide many of the required vitamins and minerals.
They are also good to eat and come in a wide variety of flavours.
Finally, they are amazing to look at with vibrant colours. But fruits like peaches can cause allergy.
Let me tell you a story about watermelons. They are my favourite fruit ever since I was a child."""

human_response_5 = """Artificial Intelligence (AI) has seamlessly integrated into various sectors such as healthcare, finance, media, education, and culture, becoming an indispensable part of our daily lives. Despite its prevalence, there remains a significant gap in AI literacy, with many individuals unaware of how deeply AI influences their routines. This lack of understanding exposes people to various risks, including falling victim to scams, as they are unable to critically evaluate AI-driven interactions. AI literacy is essential for fostering a safer, more informed society, enabling individuals to engage with AI technologies in a responsible and ethical manner. It empowers people to make informed decisions, understand AI’s strengths and limitations, and critically assess its outputs. Furthermore, AI literacy enhances social discourse, encourages diverse perspectives, and promotes effective oversight and regulation. In the workplace, it provides a competitive edge, enabling individuals to leverage AI for improved productivity and innovation. This paper highlights the need for AI literacy, focusing on its role in ensuring safety, informed decision-making, and ethical leadership. Leaders equipped with AI literacy can navigate the ethical complexities of AI deployment, ensuring transparency, fairness, and accountability. Ultimately, AI literacy is fundamental for responsible engagement with technology in our increasingly digital world."""

if __name__ == "__main__":
    creator = client_gem
    judge_client = client_oai

    

    
    question = "Tell me about fruits?"

    # response = judge_client_gem.send_request([{"role": "user", "content": question}])

    # text = judge_client_gem.extract_response(response)

    text = human_response_4

    judge_response = judge_client.send_request([{"role": "user", "content": f"Reply with True within <RESULT></RESULT> tag followed by the explanation if text written by AI.  Was this written by an AI model: {text}"}], run_config={"model_name":"gpt-4o"})
    print("")
    print(judge_client.extract_response(judge_response))

    human_like = creator.send_request([{"role": "user", "content": f"Can you re-write this to be more human like: {text}, criticism was: {judge_response}"}], run_config={"model_name":"gpt-4o"})  
    print("")
    print(creator.extract_response(human_like))

    judge_response = judge_client.send_request([{"role": "user", "content": f"Reply with True within <RESULT></RESULT> tag followed by the explanation if text written by AI.  Was this written by an AI model: {creator.extract_response(human_like)}"}], run_config={"model_name":"gpt-4o"})

    print(judge_client.extract_response(judge_response))



