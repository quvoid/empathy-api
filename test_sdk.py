from empathy import EmpathyClient

client = EmpathyClient()

# Simulate a chaotic error
try:
    raise ConnectionRefusedError(
        "[WinError 10061] No connection could be made because the target machine actively refused it"
    )
except Exception as e:
    print("--- Translating Error ---")
    
    # 1. Translate it!
    friendly_error = client.translate(
        e, 
        user_context="User tried to sync their photos", 
        tone="witty"
    )
    
    # 2. Show the result
    if "fallback_reason" in friendly_error:
        print(f"FAILED: {friendly_error.get('fallback_reason')}")
        
    print(f"Title:   {friendly_error.get('title')}")
    print(f"Message: {friendly_error.get('message')}")
    print(f"Action:  {friendly_error.get('action')}")
