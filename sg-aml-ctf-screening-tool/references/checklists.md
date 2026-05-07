# Required Lists (Singapore-focused)
- UNSCR 1718 Sanctions List  
- UNSCR 1533 Sanctions List  
- UNSCR Consolidated List  
- UNSCR 1970 Sanctions List  
- UNSCR 1844 Sanctions List  
- UNSCR 2206 Sanctions List  
- UNSCR 1591 Sanctions List  
- UNSCR 2140 Sanctions List  
- ISIL (Da'esh) & Al-Qaida Sanctions List  
- UNSCR 1988 Taliban Sanctions List  
- First Schedule of the Terrorism (Suppression of Financing) Act  
- ACRA-promulgated lists  

Local resource: `references/tsfa-first-schedule.md` holds the current First Schedule snapshot (TSFA, as provided); load it when screening against domestic CT names.
Local resource: `assets/alert-list-2025-12-23.csv` (and .txt) — ACRA Alert List (23 Dec 2025). Prefer the CSV for matching; replace when newer lists arrive.

Prompt: “Please confirm all required lists are included. If any are missing, paste them now.”

Record outcome: `Lists confirmed` or `Missing: <list names>`.

# Intake Template (paste to user)
```
Name: 
Aliases/Spelling Variants:
Date of Birth (DD/MM/YYYY):
Nationality:
Identifier(s): Passport/NRIC/Business Reg No:
Customer Type & Context (onboarding/vendor/periodic review):
List/Data Source Pasted:
Additional Information:
```

# Similarity Bands (guidance)
- High: ≥0.85 name similarity or exact + matching DOB/nationality.
- Medium: 0.70–0.84 or strong alias match with one supporting attribute.
- Low: <0.70 or weak contextual alignment.

# Adverse Media Keywords (scan for)
- Financial crime: fraud, embezzlement, tax evasion, money laundering, bribery, kickback.
- Terrorism: terrorist, bombing, radicalisation, extremist, militant.
- Sanctions/Proliferation: sanctioned, embargo, proliferation, dual-use, WMD, missile.
- Corruption/Governance: corruption, illicit payments, undue influence.
- Cyber/Other: hacking, ransomware, data breach, smuggling.

Classification prompt: tag each mention as Direct / Association / Neutral, then severity High / Medium / Low.
