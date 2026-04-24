from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def register(email, password, role):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        # Store role in users table
        supabase.table("users").insert({
            "id": user.user.id,
            "email": email,
            "role": role
        }).execute()
        return {"success": True, "message": "Registration successful"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def login(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user_data = supabase.table("users").select("*").eq("id", user.user.id).execute()
        return {"success": True, "user": user_data.data[0] if user_data.data else None}
    except Exception as e:
        return {"success": False, "message": str(e)}

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ")
        
        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            role = input("Role (student/employer): ")
            result = register(email, password, role)
            print(result["message"])
        
        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            result = login(email, password)
            if result["success"]:
                print(f"Login successful! Role: {result['user']['role']}")
            else:
                print(result["message"])
        
        elif choice == "3":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_hereSUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here