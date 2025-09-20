from time import sleep

from google import genai
from API_KEY import API_KEY  # Assuming you have a file named API_KEY.py with a function API_KEY that returns the api key as a string
import datetime
import os

prompts_folder = 'prompts'
all_files = [f for f in os.listdir(prompts_folder) if f.endswith('.txt')]

for _ in range(500):
    for prompt_file in all_files:
        with open(os.path.join(prompts_folder, prompt_file), 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = [block.strip() for block in content.strip().split('\n\n') if block.strip()]

        client = genai.Client(api_key=API_KEY())

        responses = []
        for i, block in enumerate(blocks, start=1):
            print(f"Processing {prompt_file} block {i}...")
            sleep(4)  # Just to avoid hitting rate limits, adjust as necessary
            prompt = block
            retries = True

            while retries:
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash", contents=prompt
                    )
                    retries = False
                except:
                    continue
            responses.append(response)

            output_content = f"Prompt: {prompt_file} {i}\n\nAnswer: {response.text}"

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output1.5/output_{os.path.splitext(prompt_file)[0]}_{timestamp}_{i}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(output_content)

# with open('prompts.txt', 'r', encoding='utf-8') as f:
#     content = f.read()

# blocks = [block.strip() for block in content.strip().split('\n\n') if block.strip()]

# client = genai.Client(api_key=API_KEY())

# responses = []
# for i, block in enumerate(blocks, start=1):
#     prompt = block
#     response = client.models.generate_content(
#         model="gemini-2.0-flash", contents=prompt
#     )
#     responses.append(response)

#     content = f"Prompt: {prompt}\n\nAnswer: {response.text}"

#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#     filename = f"output/output_{timestamp}.txt"

#     with open(filename, "w") as file:
#         file.write(content)
