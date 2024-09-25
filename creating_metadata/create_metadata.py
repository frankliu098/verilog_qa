import os
import time
import openai

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths for input and output files
metadata_file_path = "/Users/frankliu/Desktop/fa24/Takehome/creating_metadata
/verilog_files_metadata.txt"
readme_output_path = "/Users/frankliu/Desktop/fa24/Takehome/creating_metadata
/README.md"

# Function to call the OpenAI API with retries and detailed prints
def call_api_with_retries(content, max_retries=3):
    attempts = 0
    while attempts < max_retries:
        try:
            print(f"Calling API... Attempt {attempts + 1}/{max_retries}")
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant with a deep understanding of Verilog and hardware design."},
                    {"role": "user", "content": content}
                ],
                max_tokens=1024
            )
            # Extract and return the message content from the API response
            response = completion.choices[0].message.content.strip()
            print("API call successful.")
            return response
        except Exception as e:
            print(f"Error during API call: {e}. Retrying {attempts + 1}/{max_retries}...")
            attempts += 1
            time.sleep(2)  # Optional: sleep before retrying
    print(f"Failed to process content after {max_retries} attempts.")
    return None

# Function to read the Verilog file metadata from a text file
def read_verilog_files_metadata(file_path):
    print(f"Reading Verilog file metadata from {file_path}...")
    verilog_files = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                file_name, file_path = line.replace("File Name:", "").replace("File Path:", "").split(",")
                verilog_files.append({
                    "file_name": file_name.strip(),
                    "file_path": file_path.strip()
                })
    print(f"Found {len(verilog_files)} Verilog files to process.")
    return verilog_files

# Function to read the contents of the Verilog file
def read_verilog_file(file_path):
    print(f"Reading Verilog file: {file_path}...")
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

# Function to gather metadata for each Verilog file
def gather_metadata_for_verilog_files(verilog_files):
    metadata = []

    # Few-shot example for prompting
    few_shot_example = """
    Example for Verilog file description:

    File Name: ffetch.v
    File Path: /path/to/ffetch.v
    Purpose: The ffetch.v file implements the instruction fetch logic for the CPU, handling the prefetching and fetching of instructions from memory.
    Inter-module Relationships: It interacts with the decode and execution stages of the pipeline and fetches instructions from the memory subsystem.
    Signals: Inputs: i_clk, i_reset, cpu_new_pc. Outputs: fc_pc, fc_illegal.
    Behavior: The module performs pipelined instruction fetching and maintains alignment with CPU control flow.
    """

    # Create the prompt containing the list of Verilog files for better context
    verilog_file_list_prompt = "Here is a list of Verilog files and their locations:\n"
    for vf in verilog_files:
        verilog_file_list_prompt += f"File Name: {vf['file_name']}, File Path: {vf['file_path']}\n"

    # For each Verilog file, gather metadata using the API
    for idx, vf in enumerate(verilog_files):
        print(f"\nProcessing file {idx + 1}/{len(verilog_files)}: {vf['file_name']}")

        # Read the Verilog file contents
        verilog_contents = read_verilog_file(vf['file_path'])
        if not verilog_contents:
            print(f"Skipping {vf['file_name']} due to file read error.")
            continue

        # Prompt construction with Verilog contents
        prompt = f"""
        {few_shot_example}
        {verilog_file_list_prompt}
        
        Now analyze the Verilog file {vf['file_name']} located at {vf['file_path']}.
        Here is the full content of the Verilog file:
        {verilog_contents}

        Please describe:
        - The overall purpose of the file.
        - Inter-module relationships, explaining how it interacts with other modules in the CPU architecture.
        - Key signals (inputs/outputs).
        - The behavior of the module, including any control logic or state machines.
        """

        # Call the API to get the metadata for the file
        response = call_api_with_retries(prompt)
        
        if response:
            print(f"Successfully gathered metadata for {vf['file_name']}.")
            metadata.append({
                "file_name": vf['file_name'],
                "file_path": vf['file_path'],
                "description": response
            })
        else:
            print(f"Failed to gather metadata for {vf['file_name']}. Skipping...")

    return metadata

# Function to create a README file from scratch with the gathered metadata
def create_readme_from_scratch(metadata, output_path):
    print(f"\nCreating README file at {output_path}...")
    with open(output_path, "w") as f:
        # Write the basic information about the Zip CPU
        f.write("# The Zip CPU\n\n")
        f.write("The Zip CPU is a small, light-weight, RISC CPU. Specific design goals include:\n")
        f.write("- 32-bit: All registers, addresses, and instructions are 32-bits in length.\n")
        f.write("- A RISC CPU: Instructions nominally complete in one cycle each, with exceptions for multiplies, divides, memory accesses, and (eventually) floating-point instructions.\n")
        f.write("- A load/store architecture: Only load and store instructions may access memory.\n")
        f.write("- Includes Wishbone, AXI4-Lite, and AXI4 memory options.\n")
        f.write("- A (minimally) Von-Neumann architecture: Shared buses for instructions and data.\n")
        f.write("- A pipelined architecture: Stages for prefetch, decode, read-operand(s), ALU, memory, divide, and write-back.\n")
        f.write("- Two operating modes: Supervisor and user, with distinct access levels.\n")
        f.write("- Completely open source, licensed under the GPLv3.\n\n")

        # Write the unique features of the Zip CPU
        f.write("## Unique features and characteristics\n\n")
        f.write("- 29 instructions are currently implemented. Six additional instructions are reserved for a floating-point unit (FPU), which has yet to be implemented.\n")
        f.write("- Most instructions can be executed conditionally.\n")
        f.write("- The CPU makes heavy use of pipelining.\n")
        f.write("- The CPU has no interrupt vectors, but uses two register sets for interrupt handling.\n\n")

        # Add metadata for each Verilog file
        f.write("## Verilog File Descriptions\n\n")
        for data in metadata:
            f.write(f"### File: {data['file_name']}\n")
            f.write(f"- **Path**: {data['file_path']}\n")
            f.write(f"{data['description']}\n\n")

    print(f"README file has been successfully created and saved to {output_path}.")

# Main script to gather Verilog file metadata and create the README
def main():
    try:
        # Step 1: Read the Verilog files metadata from the provided text file
        print("Step 1: Reading Verilog files metadata...")
        verilog_files = read_verilog_files_metadata(metadata_file_path)
        
        # Step 2: Gather metadata for each Verilog file using the OpenAI API
        print("\nStep 2: Gathering metadata for each Verilog file using OpenAI API...")
        metadata = gather_metadata_for_verilog_files(verilog_files)
        
        # Step 3: Create the README from scratch with the gathered metadata
        print("\nStep 3: Creating the README from scratch with the gathered metadata...")
        create_readme_from_scratch(metadata, readme_output_path)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
