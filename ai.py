import os
import openai

openai.api_key = "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"

prompt = str(input("?"))

completion = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.5,
  max_tokens=1024,
  n=1,
  stop=None
)

response = completion.choices[0].text
print(response)