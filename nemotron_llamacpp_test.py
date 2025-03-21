from llama_cpp import Llama

# Load the model
try:
    llm = Llama(model_path="Nemotron-Mini-4B-Instruct-Q4_K_M.gguf")
except FileNotFoundError:
    print("Error: Model file not found. Please ensure 'nemotron-mini-4b-instruct.gguf' is in the current directory.")
    exit(1)

# Define the prompt
prompt = "Write a poem about AI."

# Generate a response
response = llm.create_completion(prompt, max_tokens=100, temperature=0.7)

# Print the generated text
print(response['choices'][0]['text'])
