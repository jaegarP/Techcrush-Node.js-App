import os
import sys
from abacusai import ApiClient

def main():
    # 1. Fetch your API token from your repository secrets
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        print("Error: LLM_API_KEY is not set.")
        sys.exit(1)

    # 2. Authenticate the Abacus client
    client = ApiClient(api_key=api_key)

    prompt = (
        "Write a robust Python script named validation.py that checks if an email address is valid. "
        "Return ONLY the executable code block. Do not include markdown code ticks (```)."
    )

    print("Sending prompt to Abacus AI...")
    
    try:
        # 3. Call evaluate_prompt with the exact schema supported by the SDK
        # We explicitly omit project_id here to prevent parameter mismatch errors
        response = client.evaluate_prompt(
            prompt=prompt,
            system_message="You are an automated code-writing agent. Output valid python code directly.",
            llm_name="CLAUDE_3_5_SONNET" # Supported formats: "CLAUDE_3_5_SONNET", "GEMINI_2_FLASH", "GPT_4O"
        )
        
        # Extract the pure code text block
        generated_code = response.content.strip()

    except Exception as e:
        print(f"Failed to communicate with Abacus AI API: {str(e)}")
        sys.exit(1)

    # 4. Write the file straight into your GitHub repository workspace
    output_filename = "validation.py"
    with open(output_filename, "w") as f:
        f.write(generated_code)
        
    print(f"Successfully generated {output_filename} via Abacus.AI!")

if __name__ == "__main__":
    main()
