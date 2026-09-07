```python
import re
import sys


def is_valid_email(email):
    """
    Validates an e-mail address according to RFC 5322 standards (simplified).
    
    Args:
        email: String to validate as email address
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Remove leading/trailing whitespace
    email = email.strip()
    
    # Check length constraints
    if len(email) > 254:  # RFC 5321
        return False
    
    # Basic structure check: must contain exactly one @
    if email.count('@') != 1:
        return False
    
    # Split into local and domain parts
    try:
        local, domain = email.rsplit('@', 1)
    except ValueError:
        return False
    
    # Validate local part (before @)
    if not local or len(local) > 64:  # RFC 5321
        return False
    
    # Local part pattern: alphanumeric, dots, hyphens, underscores, plus signs
    # Cannot start or end with dot, no consecutive dots
    local_pattern = r'^[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+(\.[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+)*$'
    if not re.match(local_pattern, local):
        return False
    
    # Validate domain part (after @)
    if not domain or len(domain) > 253:
        return False
    
    # Domain must contain at least one dot
    if '.' not in domain:
        return False
    
    # Domain pattern: alphanumeric and hyphens, separated by dots
    # Each label must start and end with alphanumeric
    # TLD must be at least 2 characters
    domain_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    if not re.match(domain_pattern, domain):
        return False
    
    # Check for valid characters in domain
    if domain.startswith('-') or domain.endswith('-'):
        return False
    
    # Check each domain label
    labels = domain.split('.')
    for label in labels:
        if not label or len(label) > 63:  # RFC 1035
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
    
    return True


def validate_email(email):
    """
    Main validation function with detailed feedback.
    
    Args:
        email: String to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not email:
        return False, "Email address is empty"
    
    if not isinstance(email, str):
        return False, "Email must be a string"
    
    email = email.strip()
    
    if len(email) > 254:
        return False, "Email address is too long (max 254 characters)"
    
    if '@' not in email:
        return False, "Email must contain @ symbol"
    
    if email.count('@') > 1:
        return False, "Email must contain exactly one @ symbol"
    
    try:
        local, domain = email.rsplit('@', 1)
    except ValueError:
        return False, "Invalid email format"
    
    if not local:
        return False, "Local part (before @) is missing"
    
    if len(local) > 64:
        return False, "Local part is too long (max 64 characters)"
    
    if not domain:
        return False, "Domain part (after @) is missing"
    
    if '.' not in domain:
        return False, "Domain must contain at least one dot"
    
    if is_valid_email(email):
        return True, "Valid email address"
    else:
        return False, "Invalid email format"


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python validation.py <email_address>")
        print("Example: python validation.py user@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    is_valid, message = validate_email(email)
    
    print(f"Email: {email}")
    print(f"Valid: {is_valid}")
    print(f"Message: {message}")
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
