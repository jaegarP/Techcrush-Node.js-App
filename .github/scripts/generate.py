import os
import sys
from abacusai import ApiClient

def main():
    # 1. Retrieve the environment keys passed by the GitHub Runner
    api_key = os.environ.get("LLM_API_KEY")
    project_id = os.environ.get("LLM_PROJECT_ID") # Required if using a specialized project deployment
    
    if not api_key:
        print("Error: LLM_API_KEY is not set.")
        sys.exit(1)

    # 2. Authenticate the Abacus client
    client = ApiClient(api_key=api_key)

    prompt = (
        "Write a robust Python script named validation.py that checks if an email address is valid. "
        "Return ONLY the executable code block. Do not include markdown code ticks (```)."
    )

    print("Sending prompt to Abacus AI ChatLLM...")
    
    try:
        # Call the general text/prompt evaluation function or the direct execution endpoint
        # If your agent is mapped to a specific deployment, use client.evaluate_prompt or deployment endpoints
        response = client.evaluate_prompt(
            prompt=prompt,
            system_instruction="You are an automated code-writing agent. Output valid python code directly.",
            project_id=project_id if project_id else None
        )
        
        # Pull the generated response string
        generated_code = response.content.strip()

    except Exception as e:
        print(f"Failed to communicate with Abacus AI API: {str(e)}")
        sys.exit(1)

    # 3. Write the response payload into a file inside the repository path
    output_filename = "validation.py"
    with open(output_filename, "w") as f:
        f.write(generated_code)
        
    print(f"Successfully generated {output_filename} via Abacus.AI!")

if __name__ == "__main__":
    main()
