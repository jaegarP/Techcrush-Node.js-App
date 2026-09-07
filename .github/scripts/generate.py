import os
import sys
from abacusai import ApiClient

def main():
    # 1. Fetch the API token from the GitHub Runner environment
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        print("Error: LLM_API_KEY environment variable is missing.")
        sys.exit(1)

    # 2. Authenticate the client
    client = ApiClient(api_key=api_key)
    
    temp_project = None
    generated_code = ""

    try:
        # 3. Dynamically create a temporary project container to satisfy the API backend
        print("Creating temporary workspace in Abacus.AI...")
        temp_project = client.create_project(
            name="github_actions_stateless_run", 
            use_case="CHAT_LLM"
        )
        project_id = temp_project.project_id

        prompt = (
            "Write a robust Python script named validation.py that checks if an email address is valid. "
            "Return ONLY executable code blocks. Do not wrap the response in markdown code blocks."
        )

        print(f"Sending prompt using temporary Project ID: {project_id}...")
        
        # 4. Invoke the evaluation prompt inside the runtime container
        response = client.evaluate_prompt(
            prompt=prompt,
            system_message="You are an automated code-writing agent. Output valid python code directly.",
            llm_name="CLAUDE_3_5_SONNET",
            project_id=project_id
        )
        
        generated_code = response.content.strip()

    except Exception as e:
        print(f"Failed to communicate with Abacus AI API: {str(e)}")
        sys.exit(1)
        
    finally:
        # 5. Clean up and delete the temporary project workspace so your dashboard stays clean
        if temp_project:
            print("Cleaning up temporary Abacus workspace...")
            try:
                client.delete_project(project_id=temp_project.project_id)
            except Exception as clean_err:
                print(f"Warning: Could not clean up project container: {str(clean_err)}")

    # 6. Save the generated code into your GitHub workspace
    if generated_code:
        output_filename = "validation.py"
        with open(output_filename, "w") as f:
            f.write(generated_code)
        print(f"Successfully generated {output_filename}!")
    else:
        print("Error: No code snippet was returned from the model.")
        sys.exit(1)

if __name__ == "__main__":
    main()
