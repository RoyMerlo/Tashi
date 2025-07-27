# Redirect Analyzer Tool

<img width="1024" height="1024" alt="Tashi123" src="https://github.com/user-attachments/assets/1db7cbf0-307d-4328-9291-81040f854861" />


A simple and powerful GUI! 

-based Redirect Analyzer that tracks HTTP redirects, resolves IP addresses, and retrieves WHOIS data for each domain encountered during the request chain.

## 🔍 Features

- **Tracks all HTTP redirects** from the initial URL to the final destination
- **Resolves IP address** for each URL visited
- **Displays WHOIS information** (Registrar, Creation Date, Expiry Date, Name Servers)
- **Supports auto-complete URLs** (e.g., typing `google.com` will try `https://google.com ` first)
- **Exports results to CSV or TXT**
- **Copy & Paste support**
- **Clean and customizable UI with color-coded redirect steps**

 (https://github.com/user-attachments/assets/774a9107-df0f-41d1-9bb3-a4f4534a18bb)


## 📦 Requirements

Make sure you have these Python packages installed:

```bash
pip install requests python-whois pyfiglet
🚀 How to Run 

    Clone the repository: 
    bash
     

 
1
git clone https://github.com/yourusername/redirect-analyzer.git 
 
 

Navigate into the directory: 
bash
 
 
1
cd redirect-analyzer
 
 

Run the script: 
bash
 

     
    1
    python redirect_analyzer.py
     
     
     

💾 Save Results 

You can save the output as: 

    .txt file (plain text)
    .csv file (structured data for spreadsheets)
     

🎨 Interface Overview 

    ASCII Banner : Displays the "TASHI" logo using pyfiglet
    Powered by : Credit line shown below the banner
    URL Input Field : Supports paste (Ctrl+V) and clear
    Analyze Button : Follows redirects and displays step-by-step info
    Output Area : Shows detailed redirect path, IP, and WHOIS info
    Copy / Save Buttons : Easy to export findings
     

🧪 Example Output 
 
🚧 Step 1 - Redirect
🌐 URL: http://example.com
📶 IP Address: 93.184.216.34
📋 WHOIS Info:
   Registrar: MarkMonitor Inc.
   Creation Date: 1997-04-21 04:00:00
   Expiry Date: 2028-04-20 04:00:00
   Name Servers: A.VERISIGN-GLOBALREGISTRY.COM, B.VERISIGN-GLOBALREGISTRY.COM
------------------------------------------------------------
🏁 Step 2 - Final
🌐 URL: https://www.example.com 
 SPF IP: 93.184.216.34
📋 WHOIS Info:
   Registrar: MarkMonitor Inc.
   Creation Date: 1997-04-21 04:00:00
   Expiry Date: 2028-04-20 04:00:00
   Name Servers: A.VERISIGN-GLOBALREGISTRY.COM, B.VERISIGN-GLOBALREGISTRY.COM
------------------------------------------------------------
 
 
📁 File Structure 
 
 
1
2
3
4
5
6
7
redirect-analyzer/
│
├── redirect_analyzer.py     # Main script
├── README.md                # This file
├── LICENSE                  # GNU GPL v3.0 License
└── screenshots/             # Optional folder for images
    └── ui.png
 
 
🛡 Disclaimer 

This tool is for educational and ethical use only. Do not use on domains without permission. 
📄 License 

This project is licensed under the GNU General Public License v3.0  – see LICENSE  for details. 

If you distribute this software, you must make the source code available to users. 

    ⚠️ Important Note:  If you modify and redistribute this code, you are required to: 

        Keep the license file included
        Share your modified source code
        Give credit where due
         

     

Read the full GNU GPL v3.0 license here  
👤 Author 

Roy Merlo (2025) 

📧 Contact: merloroy200@gmail.com  
