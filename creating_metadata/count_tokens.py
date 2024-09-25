import json
import tiktoken

# Load the JSON file containing the Verilog chunks
with open('/Users/frankliu/Desktop/fa24/Takehome/creating_metadata/json/cleaned/cleaned_verilog_chunks.json', 'r') as f:
    data = json.load(f)

# Initialize the tokenizer (this example assumes GPT-3 or similar tokenization)
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Adjust model if needed

def count_tokens_in_chunks(chunks):
    """
    Counts the total number of tokens in the given list of chunks.
    """
    total_tokens = 0
    for chunk in chunks:
        tokens = encoding.encode(chunk)
        total_tokens += len(tokens)
    return total_tokens

# Iterate through all files and count tokens
total_tokens_across_all_files = 0
file_token_counts = {}

for file in data:
    file_name = file['file_name']
    chunks = file['chunks']
    
    file_token_count = count_tokens_in_chunks(chunks)
    file_token_counts[file_name] = file_token_count
    total_tokens_across_all_files += file_token_count

# Output the total token count and per file token count
print(f"Total tokens across all Verilog files: {total_tokens_across_all_files}")
print("Token counts per file:")
for file_name, token_count in file_token_counts.items():
    print(f"{file_name}: {token_count}")

# Optionally, you could save the token counts to a file
with open('/Users/frankliu/Desktop/fa24/Takehome/creating_metadata/json/token_counts.json', 'w') as f:
    json.dump(file_token_counts, f, indent=4)

print("Token counts saved to token_counts.json.")
