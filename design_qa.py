import os
import time
import openai
import re
import streamlit as st

openai.api_key = os.getenv("OPENAI_API_KEY")

readme_output_path = "/Users/frankliu/Desktop/fa24/Takehome/creating_metadata/README.md"
verilog_files_dir = "/Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/"

def get_relevant_files_from_readme(query):
    """Prepend README to the query and ask OpenAI which Verilog files are relevant."""
    readme_content = read_file(readme_output_path)
    if not readme_content:
        return []

    example_response = """
To answer the query regarding [query] the relevant Verilog files along with their paths are:

1. **File: file.v**
   - **Path**: /Path/To/File/file.v
   - **Purpose**: [purpose]

1. **File: file.v**
   - **Path**: /Path/To/File/file.v
   - **Purpose**: [purpose]
"""


    prompt = (
        f"{readme_content}\n\n"
        f"Given the information above, please suggest which Verilog files and their locations should be looked at "
        f"to answer the following query:\n\n"
        f"Query: {query}\n\n"
        f"Please respond in the following format:\n{example_response}"
    )


    response = call_api_with_retries(prompt)
    return response


def call_api_with_retries(content, max_retries=3):
    attempts = 0
    while attempts < max_retries:
        try:
            st.write(f"Calling API... Attempt {attempts + 1}/{max_retries}")
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant with a deep understanding of Verilog and hardware design."},
                    {"role": "user", "content": content}
                ],
                max_tokens=1024
            )

            response = completion.choices[0]['message']['content'].strip()
            st.write("API call successful.")
            return response
        except Exception as e:
            st.error(f"Error during API call: {e}. Retrying {attempts + 1}/{max_retries}...")
            attempts += 1
            time.sleep(2)
    st.error(f"Failed to process content after {max_retries} attempts.")
    return None


def read_file(file_path):
    """Read the contents of a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        st.error(f"Error reading {file_path}: {e}")
        return None


def extract_file_info(response):
    """Extract file name, path, and purpose from the LLM response."""
    file_info = []
    pattern = re.compile(r"(\/Users\/frankliu\/Desktop\/fa24\/Takehome\/bronco-zipcpu\/(bench|rtl|sim)\/(formal|mcy|zipcpu|zipdma|core|ex|peripherals|rtl)\/[a-zA-Z0-9_\-]+\.v)", re.DOTALL)
    matches = pattern.findall(response)
    for match in matches:
        file_info.append({
            "file_path": match[0]
        })
    return file_info

def gather_file_contents(file_paths):
    """Gather the contents of the provided Verilog file paths."""
    file_contents = []
    for file_path in file_paths:
        full_path = file_path.strip()
        content = read_file(full_path)
        if content:
            file_contents.append((file_path, content))
        else:
            st.warning(f"Skipping {file_path} due to read error.")
    return file_contents

def design_qa(query):
    st.write(f"Received query: {query}")


    st.write("Identifying relevant files based on the README...")
    relevant_files_response = get_relevant_files_from_readme(query)
    if not relevant_files_response:
        return "Unable to identify relevant files."
    
    
    st.subheader(f"Relevant File Response")
    st.markdown(relevant_files_response) 


    file_info = extract_file_info(relevant_files_response)
    if not file_info:
        return "No relevant files found based on the query."

    st.write(f"Identified relevant files: {file_info}")

    
    file_paths = [info['file_path'] for info in file_info]
    file_contents = gather_file_contents(file_paths)
    if not file_contents:
        return "Unable to gather file contents."


    for file_path, content in file_contents:
        st.subheader(f"File: {file_path}")
        st.text(content[:3000])


    st.write("Preparing final answer based on file contents...")
    verilog_files_content = "\n".join([f"File: {fc[0]}\n{fc[1][:3000]}" for fc in file_contents])

    answer_prompt = (
        f"Based on the contents of the Verilog files below, please answer the following query:\n\n"
        f"{verilog_files_content}\n\n"
        f"Query: {query}"
        f"When possible, reference specific lines of verilog to make the response more robust."
        f"Think step-by-step."
    )

    final_response = call_api_with_retries(answer_prompt)

    return final_response or "Unable to generate an answer based on the Verilog files."

def main():
    st.title("Verilog Q&A Assistant")

    user_query = st.text_input("Ask a question about the Verilog codebase")

    if st.button("Submit"):
        if user_query:
            response = design_qa(user_query)
            st.subheader("Response")
            st.write(response)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
 
 
# if __name__ == "__main__":
#     sample_questions = {
#         "easy": [
#             "Which files contain the implementation for arithmetic and logic?",
#             "Explain the interface of the pipemem module",
#         ],
#         "medium": [
#             "How does pipemem check for a stalled pipeline?",
#             "How does the design of the 3-clock multiplier change between verilator sim and synthesis?",
#         ],
#         "hard": [
#             "Give me a cycle-accurate walkthrough of the 3-clock multiplier on 8 x 3",
#             "When I use the multiplier with parameter code 4 it seems to fail on unsigned cases. Why? Give me the code to fix it."
#         ]
#     }

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

# import os
# import time
# import openai
# import re  # Import regex for parsing

# # Set the OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Define the path to the README file and the Verilog files directory
# readme_output_path = "/Users/frankliu/Desktop/fa24/Takehome/creating_metadata/README.md"
# verilog_files_dir = "/Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/"

# # Function to call the OpenAI API with retries and detailed prints
# def call_api_with_retries(content, max_retries=3):
#     attempts = 0
#     while attempts < max_retries:
#         try:
#             print(f"Calling API... Attempt {attempts + 1}/{max_retries}")
#             completion = openai.ChatCompletion.create(
#                 model="gpt-4o-mini",  # Using the correct model identifier
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant with a deep understanding of Verilog and hardware design."},
#                     {"role": "user", "content": content}
#                 ],
#                 max_tokens=1024
#             )
#             # Extract and return the message content from the API response
#             response = completion.choices[0]['message']['content'].strip()
#             print(response)
#             print("API call successful.")
#             return response
#         except Exception as e:
#             print(f"Error during API call: {e}. Retrying {attempts + 1}/{max_retries}...")
#             attempts += 1
#             time.sleep(2)  # Optional: sleep before retrying
#     print(f"Failed to process content after {max_retries} attempts.")
#     return None

# # Function to read a file's content
# def read_file(file_path):
#     """Read the contents of a file."""
#     try:
#         with open(file_path, 'r') as file:
#             return file.read()
#     except Exception as e:
#         print(f"Error reading {file_path}: {e}")
#         return None

# # Function to break Verilog code into manageable chunks
# def split_into_chunks(verilog_code, chunk_size=3000):
#     return [verilog_code[i:i + chunk_size] for i in range(0, len(verilog_code), chunk_size)]

# # Function to get relevant files from README based on the query with few-shot prompting
# def get_relevant_files_from_readme(query):
#     """Prepend README to the query and ask OpenAI which Verilog files are relevant."""
#     readme_content = read_file(readme_output_path)
#     if not readme_content:
#         return []

#     # Few-shot prompting for structured response
#     example_response = """
# To answer the query regarding [query] the relevant Verilog files along with their paths are:

# 1. **File: file.v**
#    - **Path**: /Path/To/File/file.v
#    - **Purpose**: [purpose]

# 1. **File: file.v**
#    - **Path**: /Path/To/File/file.v
#    - **Purpose**: [purpose]
# """

#     # Construct the prompt with the README content, example, and query
#     prompt = (
#         f"{readme_content}\n\n"
#         f"Given the information above, please suggest which Verilog files and their locations should be looked at "
#         f"to answer the following query:\n\n"
#         f"Query: {query}\n\n"
#         f"Please respond in the following format:\n{example_response}"
#     )

#     # Call OpenAI API
#     response = call_api_with_retries(prompt)
#     return response

# # Function to extract file names, paths, and purposes using regex
# def extract_file_info(response):
#     """Extract file name, path, and purpose from the LLM response."""
#     file_info = []
    
#     # Updated regex pattern to match the full file paths in the directories
#     pattern = re.compile(r"(\/Users\/frankliu\/Desktop\/fa24\/Takehome\/bronco-zipcpu\/(bench|rtl|sim)\/(formal|mcy|zipcpu|zipdma|core|ex|peripherals|rtl)\/[a-zA-Z0-9_\-]+\.v)", re.DOTALL)
    
#     # This will return the entire match, not just the capture groups
#     matches = pattern.findall(response)
    
#     print(f"MATCHES: \n\n {matches}")

#     for match in matches:
#         # match[0] contains the entire matched file path
#         file_info.append({
#             "file_path": match[0]  # Use the full match for file path
#         })

#     return file_info


# # Function to gather the contents of relevant Verilog files
# def gather_file_contents(file_paths):
#     """Gather the contents of the provided Verilog file paths."""
#     file_contents = []
#     for file_path in file_paths:
#         full_path = file_path.strip()  # No need to append verilog_files_dir as file_path is absolute
#         content = read_file(full_path)
#         if content:
#             file_contents.append((file_path, content))
#         else:
#             print(f"Skipping {file_path} due to read error.")
#     return file_contents

# # Main function to handle Verilog design Q&A
# def design_qa(query):
#     """Main logic for the design Q&A process."""
#     print(f"Received query: {query}")

#     # Step 1: Ask the LLM for relevant files based on the README
#     print("Identifying relevant files based on the README...")
#     relevant_files_response = get_relevant_files_from_readme(query)
#     if not relevant_files_response:
#         return "Unable to identify relevant files."

#     # Step 2: Extract file information using regex
#     file_info = extract_file_info(relevant_files_response)
#     print(file_info)
#     if not file_info:
#         return "No relevant files found based on the query."

#     print(f"Identified relevant files: {file_info}")

#     # Step 3: Gather the contents of the relevant files
#     print("Gathering file contents...")
#     file_paths = [info['file_path'] for info in file_info]
#     print(f"\n\n{file_paths}")
#     file_contents = gather_file_contents(file_paths)
#     if not file_contents:
#         return "Unable to gather file contents."

#     # Step 4: Ask the LLM to answer the query based on the Verilog file contents
#     print("Preparing final answer based on file contents...")
#     verilog_files_content = "\n".join([f"File: {fc[0]}\n{fc[1][:]}" for fc in file_contents])  # Limit content size to 3000 chars per file

#     answer_prompt = (
#         f"Based on the contents of the Verilog files below, please answer the following query:\n\n"
#         f"{verilog_files_content}\n\n"
#         f"Query: {query}"
#     )

#     # Call the OpenAI API again with the Verilog file contents
#     final_response = call_api_with_retries(answer_prompt)

#     return final_response or "Unable to generate an answer based on the Verilog files."

# # Main script execution
# if __name__ == "__main__":
#     sample_questions = {
#         "easy": [
#             "Which files contain the implementation for arithmetic and logic?",
#             "Explain the interface of the pipemem module",
#         ],
#         "medium": [
#             "How does pipemem check for a stalled pipeline?",
#             "How does the design of the 3-clock multiplier change between verilator sim and synthesis?",
#         ],
#         "hard": [
#             "Give me a cycle-accurate walkthrough of the 3-clock multiplier on 8 x 3",
#             "When I use the multiplier with parameter code 4 it seems to fail on unsigned cases. Why? Give me the code to fix it."
#         ]
#     }

#     while True:
#         user_question = input("Ask a question about the Verilog codebase (or type 'exit' to quit): ")
#         if user_question.lower() == 'exit':
#             break

#         try:
#             response = design_qa(user_question)
#             print("\nResponse:\n")
#             print(response)

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
