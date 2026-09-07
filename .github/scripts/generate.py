import os
import sys
from abacusai import ApiClient

def main():
    # 1. Fetch only the API token passed by the GitHub Runner
    api_key = os.environ.get("LLM_API_KEY")
    
    if not api_key:
        print("Error: LLM_API_KEY environment variable is missing.")
        sys.exit(1)

    # 2. Authenticate the global client
    client = ApiClient(api_key=api_key)

    prompt = (
        "Write a robust Python script named validation.py that checks if an email address is valid. "
        "Return ONLY executable code blocks. Do not wrap the response in markdown code blocks."
    )

    print("Sending prompt to Abacus AI...")
    
    try:
        # 3. Call evaluate_prompt WITHOUT project_id
        # Define the exact core LLM backend via the llm_name parameter
        response = client.evaluate_prompt(
            prompt=prompt,
            system_message="You are an automated code-writing agent. Output valid python code directly.",
            llm_name="CLAUDE_3_5_SONNET"  # Alternatives: "GEMINI_2_5_FLASH", "GPT_4O", etc.
        )
        
        # Capture the raw string response
        generated_code = response.content.strip()

    except Exception as e:
        print(f"Failed to communicate with Abacus AI API: {str(e)}")
        sys.exit(1)

    # 4. Write the file straight into your GitHub repository workspace
    output_filename = "validation.py"
    with open(output_filename, "w") as f:
        f.write(generated_code)
        
    print(f"Successfully generated {output_filename} without a Project ID!")

if __name__ == "__main__":
    main()
