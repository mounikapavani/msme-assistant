import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

# 1. SETUP API KEY (Use your actual key)
# Note: In a real terminal, set this via `set GEMINI_API_KEY=...` or paste it below for testing
if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = "AIzaSyBjAL97L_8ve3lUJgj-UwelUxVBjAn_HlU"  # Replace with your actual key

# Initialize the Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=os.environ["GEMINI_API_KEY"]
)

# --- 2. DEFINE THE TOOLS (The "Arms and Legs") ---

def analyze_cash_flow_runway(file_path: str):
    """
    Reads a bank statement CSV to calculate the 'Runway' (days of cash left).
    Input must be a valid file path string (e.g., 'bank_statement.csv').
    Returns a status string indicating if the business is in danger.
    """
    try:
        # Check if file exists to prevent errors
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."

        df = pd.read_csv(file_path)
        start_bal = df.iloc[0]['Balance']
        end_bal = df.iloc[-1]['Balance']
        days = len(df)
        
        # Net Loss over the period
        net_change = end_bal - start_bal
        
        if net_change >= 0:
            return f"Healthy Financials. Balance grew by {net_change}. No action needed."
        
        # Calculate burn rate
        daily_burn = abs(net_change) / days
        if daily_burn == 0: daily_burn = 1 # Avoid div by zero
        days_left = end_bal / daily_burn
        
        return (f"CRITICAL ALERT: The business is losing money (Burn Rate: ₹{daily_burn:.2f}/day). "
                f"Current Balance: ₹{end_bal:.2f}. "
                f"Estimated Runway: {int(days_left)} days remaining before bankruptcy.")
    except Exception as e:
        return f"Error analyzing data: {str(e)}"

def search_telangana_schemes(business_category: str):
    """
    Searches for Telangana State Government subsidies based on business category.
    Input should be a category like 'Textile', 'Agriculture', or 'Tech'.
    """
    # Simulated Database of Schemes
    schemes = {
        "textile": "T-TAP (Telangana Textile and Apparel Policy): Provides 25% capital subsidy and 100% stamp duty reimbursement.",
        "agriculture": "Rythu Bandhu: Investment support for agriculture.",
        "tech": "T-IDEA: Incentive scheme for IT startups and expansions.",
        "general": "Mudra Loan (Kishore Category): Loans up to ₹5 Lakhs for existing small businesses."
    }
    
    key = business_category.lower()
    if "textile" in key or "cloth" in key:
        return schemes["textile"]
    elif "farm" in key or "agri" in key:
        return schemes["agriculture"]
    elif "tech" in key or "software" in key:
        return schemes["tech"]
    else:
        return schemes["general"]

def save_application_letter(content: str):
    """
    Saves the drafted application letter to a text file.
    Input should be the full text of the letter.
    """
    filename = "Draft_Application_Letter.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Success: Letter saved to {filename}"

# --- 3. INITIALIZE THE AGENT ---

# Load tools into a list
tools = [analyze_cash_flow_runway, search_telangana_schemes, save_application_letter]

# Create a simple chain-based agent approach
def run_agent_tasks():
    """Execute the agent workflow step by step"""
    
    print("📊 Step 1: Analyzing Cash Flow...")
    cash_flow_status = analyze_cash_flow_runway("bank_statement.csv")
    print(f"Status: {cash_flow_status}\n")
    
    print("🔍 Step 2: Searching for Telangana Schemes...")
    scheme = search_telangana_schemes("Textile")
    print(f"Found Scheme: {scheme}\n")
    
    print("✍️ Step 3: Drafting Application Letter...")
    
    # Create a professional letter
    letter = f"""
District Industries Centre (DIC), Sircilla
Telangana, India

Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}

Subject: Application for {scheme.split(':')[0]} - Financial Assistance Due to Cash Flow Crisis

Dear Sir/Madam,

I am writing to request immediate financial assistance and subsidy under the Telangana Government's {scheme.split(':')[0]} scheme.

SITUATION:
{cash_flow_status}

JUSTIFICATION:
Our textile business in Sircilla is experiencing severe financial constraints. The current liquidity crisis threatens our operations and employment of our workforce.

SCHEME REQUESTED:
{scheme}

This scheme aligns perfectly with our business needs and would provide the critical capital support required to stabilize operations.

REQUIRED ACTIONS:
1. Enrollment in {scheme.split(':')[0]}
2. Processing of subsidy claim
3. Expedited approval given the critical nature of our situation

I am available to provide additional documentation and attend any required meetings.

Thanking you for your prompt attention to this matter.

Yours sincerely,
Textile Shop Owner
Sircilla, Telangana
"""
    
    result = save_application_letter(letter)
    print(f"✅ {result}")
    print("\n" + "="*50)
    print("🎯 AGENT MISSION COMPLETED")
    print("="*50)

# --- 4. EXECUTE THE MISSION ---

print("🤖 CFO Agent Started... Reading Bank Statement...")
print("="*50)

run_agent_tasks()

print("\nCheck the 'Draft_Application_Letter.txt' file for the complete letter.")