import os
import json
import base64

# 1. Load and encode all visual assets
assets = {}
med_path = 'marks/medallion-384.png'
if os.path.exists(med_path):
    with open(med_path, 'rb') as f:
        assets['medallion'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

for fund in ['argon', 'bogle', 'smaug', 'midas', 'vladd']:
    for i in range(1, 6):
        p_path = f'portraits/{fund}-0{i}.png'
        c_path = f'cutouts/{fund}-0{i}.png'
        if os.path.exists(p_path):
            with open(p_path, 'rb') as f:
                assets[f'p_{fund}_{i}'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')
        if os.path.exists(c_path):
            with open(c_path, 'rb') as f:
                assets[f'c_{fund}_{i}'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

print(f"Loaded {len(assets)} assets.")

# 2. Structured Campaign Data (Python Dicts -> serialized via json.dumps)
campaign_weeks = [
    {
        "week": 1,
        "title": "Week 1: The Initial Intake",
        "note": "Establish admissions standards. Confirm soulbound passes and Deng Desk holdings.",
        "dossiers": [
            {
                "seatId": "#1402", "fund": "argon", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0x81fa...91bc · 28,400 $TMF", "pass": "Soulbound (2 Chairs Minted)", "deng": "128 Days · 1.62 Credits",
                "portraitKey": "p_argon_1", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Applicant requests enrollment under Argon books. Stated intent: hold dividend checks in briefcase until quarterly liquidation. Displays inert temperament, completely unmoved by volatile headlines."
            },
            {
                "seatId": "#0841", "fund": "bogle", "chair": "The Interns Folding Chair", "tier": "Class I Intern",
                "briefcase": "0x43da...22aa · 12,000 $TMF", "pass": "Soulbound (2 Chairs Minted)", "deng": "95 Days · 1.50 Credits",
                "portraitKey": "p_bogle_3", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Applicant firmly believes in buying the whole haystack. Refuses single-stock exposure. Ready to tender additional passes upon the Deng Desk roll call."
            },
            {
                "seatId": "#2930", "fund": "smaug", "chair": "The Gilded Throne", "tier": "Class VII Sovereign",
                "briefcase": "0x98bb...c144 · 194,500 $TMF", "pass": "Soulbound (2 Chairs Minted)", "deng": "210 Days · 1.95 Credits",
                "portraitKey": "p_smaug_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Sleeps on the hoard. Claims knowledge of every individual coin inside the vault. Demands strict adherence to fee-burn policies at the Proxy Ballot."
            },
            {
                "seatId": "#3312", "fund": "vladd", "chair": "Creaking Wooden Swivel", "tier": "Class II Clerk",
                "briefcase": "0x0000...0000 · 0 $TMF", "pass": "Forged Paper Slip", "deng": "2 Days · 0.05 Credits",
                "portraitKey": "p_vladd_1", "isAnomaly": True, "correctVerdict": "DECLINED",
                "memo": "Applicant arrived with wet ink on their admission slip. Deng holding period is only 48 hours. Demands immediate access to Vladd distressed order routing."
            }
        ]
    },
    {
        "week": 2,
        "title": "Week 2: The Deng Desk Verification",
        "note": "ApeChain blockhash audit in effect. Tendered Dengs must meet 45-day tenure for credit claiming.",
        "dossiers": [
            {
                "seatId": "#1880", "fund": "midas", "chair": "Tasteful Walnut Lounge", "tier": "Class III Executive",
                "briefcase": "0x33b1...7710 · 67,200 $TMF", "pass": "Soulbound (Verified Desk)", "deng": "140 Days · 1.68 Credits",
                "portraitKey": "p_midas_4", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Bullion specialist. Proposes conversion of dividend checks into gold-backed certificates upon Fiscal Friday bell."
            },
            {
                "seatId": "#0419", "fund": "argon", "chair": "Deep Button Chesterfield", "tier": "Class V Trustee",
                "briefcase": "0x12ac...55ff · 45,000 $TMF", "pass": "Soulbound (Verified Desk)", "deng": "110 Days · 1.55 Credits",
                "portraitKey": "p_argon_3", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Senior shareholder. Requests placement on the Argon Proxy Ballot committee. Never sold an on-chain position."
            },
            {
                "seatId": "#0992", "fund": "bogle", "chair": "The Interns Folding Chair", "tier": "Class I Intern",
                "briefcase": "0x55aa...1122 · 5,000 $TMF", "pass": "Unconfirmed Slip", "deng": "12 Days · 0.40 Credits",
                "portraitKey": "p_bogle_4", "isAnomaly": True, "correctVerdict": "FLAGGED",
                "memo": "Deng credits do not match primary wallet file on ApeChain. Claims desk clerk signed manual waiver."
            },
            {
                "seatId": "#2241", "fund": "vladd", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0x66cc...9988 · 82,000 $TMF", "pass": "Soulbound (Verified Desk)", "deng": "160 Days · 1.78 Credits",
                "portraitKey": "p_vladd_4", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Distressed asset manager. Liquidated short positions during recent pullback and tenders 3 Deng passes."
            }
        ]
    },
    {
        "week": 3,
        "title": "Week 3: The Shadow Syndicate",
        "note": "Anonymous entities are attempting to seat operatives with identical briefcases across all five funds.",
        "dossiers": [
            {
                "seatId": "#3001", "fund": "smaug", "chair": "Creaking Wooden Swivel", "tier": "Class II Clerk",
                "briefcase": "0xbad0...beef · 1,000 $TMF", "pass": "Soulbound (Valid)", "deng": "180 Days · 1.85 Credits",
                "portraitKey": "p_smaug_3", "isAnomaly": True, "correctVerdict": "FLAGGED",
                "memo": "Memo field contains coded instructions referencing forced dissolution vote at Week 13. Signed simply The Syndicate."
            },
            {
                "seatId": "#2410", "fund": "midas", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0x77dd...3321 · 54,000 $TMF", "pass": "Soulbound (Valid)", "deng": "90 Days · 1.48 Credits",
                "portraitKey": "p_midas_1", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Member in good standing. Allocating 100% of briefcase yields to the Smaug-Midas liquidity pair."
            },
            {
                "seatId": "#1109", "fund": "argon", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0x8899...0011 · 39,000 $TMF", "pass": "Soulbound (Valid)", "deng": "135 Days · 1.65 Credits",
                "portraitKey": "p_argon_4", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Argon loyalist. Promises never to participate in speculative merger proposals without unanimous consent."
            },
            {
                "seatId": "#0702", "fund": "bogle", "chair": "The Interns Folding Chair", "tier": "Class I Intern",
                "briefcase": "0xdead...1337 · 0 $TMF", "pass": "Revoked Pass", "deng": "0 Days · 0.00 Credits",
                "portraitKey": "p_bogle_1", "isAnomaly": True, "correctVerdict": "DECLINED",
                "memo": "Blacklisted address from Robinscan. Attempted to pass off an ApeChain dummy token as a Soulbound TMF Pass."
            }
        ]
    },
    {
        "week": 4,
        "title": "Week 4: The Chair Mergers",
        "note": "First quarter-close M&A consolidation. Ensure surviving seats retain uncashed briefcase checks.",
        "dossiers": [
            {
                "seatId": "#1650", "fund": "vladd", "chair": "Beige Task Chair", "tier": "Class II Clerk",
                "briefcase": "0x44aa...88ee · 22,000 $TMF", "pass": "Soulbound (Valid)", "deng": "88 Days · 1.46 Credits",
                "portraitKey": "p_vladd_3", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Wishes to consolidate two folding chairs into an upgraded task chair under Vladd charter."
            },
            {
                "seatId": "#3220", "fund": "smaug", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0x9922...bb33 · 91,000 $TMF", "pass": "Soulbound (Valid)", "deng": "195 Days · 1.90 Credits",
                "portraitKey": "p_smaug_4", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Auditor for Smaug fund. Verifying that the 401,000 $TMF base rate holds in the Open Market till."
            },
            {
                "seatId": "#2105", "fund": "bogle", "chair": "Creaking Wooden Swivel", "tier": "Class II Clerk",
                "briefcase": "0x3344...5566 · 31,000 $TMF", "pass": "Soulbound (Valid)", "deng": "105 Days · 1.52 Credits",
                "portraitKey": "p_bogle_4", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Long term index accumulator. Submits monthly briefcases for dividend check audits."
            },
            {
                "seatId": "#1010", "fund": "midas", "chair": "Tasteful Walnut Lounge", "tier": "Class III Executive",
                "briefcase": "0xbeef...0000 · 10,000 $TMF", "pass": "Suspicious Slip", "deng": "4 Days · 0.10 Credits",
                "portraitKey": "p_midas_3", "isAnomaly": True, "correctVerdict": "DECLINED",
                "memo": "Tendered forged ApeChain voucher. Claims their Deng was delivered by courier directly to the Chairman."
            }
        ]
    },
    {
        "week": 5,
        "title": "Week 5: The Open Market Arbitrage",
        "note": "AMM trading surge. Brokers exploiting the plus 16% pick premium on voting chairs.",
        "dossiers": [
            {
                "seatId": "#1777", "fund": "argon", "chair": "The Interns Folding Chair", "tier": "Class I Intern",
                "briefcase": "0x7788...9900 · 14,000 $TMF", "pass": "Soulbound (Valid)", "deng": "115 Days · 1.58 Credits",
                "portraitKey": "p_argon_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Junior clerk seeking admission. Complies with all Argon inertia covenants."
            },
            {
                "seatId": "#2888", "fund": "smaug", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0x1122...3344 · 110,000 $TMF", "pass": "Soulbound (Valid)", "deng": "220 Days · 2.00 Credits",
                "portraitKey": "p_smaug_5", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Treasure hoarder. Insists that all uncashed checks remain locked inside the token-bound account indefinitely."
            },
            {
                "seatId": "#0555", "fund": "bogle", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0x9900...aabb · 88,000 $TMF", "pass": "Soulbound (Valid)", "deng": "130 Days · 1.64 Credits",
                "portraitKey": "p_bogle_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Bogle trustee. Recommends expanding market coverage to include all StonkBrokers launches."
            },
            {
                "seatId": "#3999", "fund": "vladd", "chair": "The Interns Folding Chair", "tier": "Class I Intern",
                "briefcase": "0x4444...4444 · 0 $TMF", "pass": "Duplicate Pass", "deng": "15 Days · 0.45 Credits",
                "portraitKey": "p_vladd_5", "isAnomaly": True, "correctVerdict": "FLAGGED",
                "memo": "Applicant attempted to tender a pass ID that was already redeemed at the Subscription Desk yesterday."
            }
        ]
    },
    {
        "week": 6,
        "title": "Week 6: The Smaug Treasury Audit",
        "note": "Every token counted down to the penny. Smaug requests strict inspection of all fee balances.",
        "dossiers": [
            {
                "seatId": "#2500", "fund": "midas", "chair": "Creaking Wooden Swivel", "tier": "Class II Clerk",
                "briefcase": "0x2233...4455 · 26,000 $TMF", "pass": "Soulbound (Valid)", "deng": "95 Days · 1.50 Credits",
                "portraitKey": "p_midas_3", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Gold desk applicant. Agrees to all standard mint fees and 100% token-bound account routing."
            },
            {
                "seatId": "#1333", "fund": "argon", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0x6677...8899 · 35,000 $TMF", "pass": "Soulbound (Valid)", "deng": "140 Days · 1.68 Credits",
                "portraitKey": "p_argon_1", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Argon veteran. Stated purpose: preserve capital during anticipated summer drawdowns."
            },
            {
                "seatId": "#0222", "fund": "smaug", "chair": "Beige Task Chair", "tier": "Class II Clerk",
                "briefcase": "0xbbbb...cccc · 500 $TMF", "pass": "Forged Seal", "deng": "8 Days · 0.25 Credits",
                "portraitKey": "p_smaug_1", "isAnomaly": True, "correctVerdict": "DECLINED",
                "memo": "Pass bears a photocopy of the Chairman medallion seal. Smaug auditors immediately flagged the file."
            },
            {
                "seatId": "#3444", "fund": "vladd", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0xdddd...eeee · 62,000 $TMF", "pass": "Soulbound (Valid)", "deng": "175 Days · 1.82 Credits",
                "portraitKey": "p_vladd_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Contrarian buyer. Enrolling during peak panic with full adherence to Vladd blood-in-the-streets principle."
            }
        ]
    },
    {
        "week": 7,
        "title": "Week 7: The Proxy Ballot Dispute",
        "note": "Three proposals on the table: profit distribution ratios, fee burn volume, and treasury buybacks.",
        "dossiers": [
            {
                "seatId": "#0888", "fund": "bogle", "chair": "Deep Button Chesterfield", "tier": "Class V Trustee",
                "briefcase": "0x1212...3434 · 95,000 $TMF", "pass": "Soulbound (Valid)", "deng": "165 Days · 1.78 Credits",
                "portraitKey": "p_bogle_5", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Index veteran. Pledges vote towards automated indexing of all Robinhood Chain verified tokens."
            },
            {
                "seatId": "#2777", "fund": "midas", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0x5656...7878 · 74,000 $TMF", "pass": "Soulbound (Valid)", "deng": "120 Days · 1.60 Credits",
                "portraitKey": "p_midas_5", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Midas partner. Votes for maximal gold reserve allocation on the weekly ballot."
            },
            {
                "seatId": "#1999", "fund": "vladd", "chair": "The Interns Folding Chair", "tier": "Class I Intern",
                "briefcase": "0x0011...2233 · 18,000 $TMF", "pass": "Soulbound (Valid)", "deng": "100 Days · 1.52 Credits",
                "portraitKey": "p_vladd_5", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Junior partner. Ready to support aggressive distress buying on Friday."
            },
            {
                "seatId": "#3888", "fund": "smaug", "chair": "The Gilded Throne", "tier": "Class VII Sovereign",
                "briefcase": "0x9999...9999 · 210,000 $TMF", "pass": "Mismatched Key", "deng": "20 Days · 0.50 Credits",
                "portraitKey": "p_smaug_2", "isAnomaly": True, "correctVerdict": "FLAGGED",
                "memo": "Applicant holds high balance but fails key signature challenge on ApeChain bridge."
            }
        ]
    },
    {
        "week": 8,
        "title": "Week 8: The Chairman's Dispatches",
        "note": "Pneumatic dispatches from Seat 0 in the rotunda. Reminding the desk that no chair is ever for sale.",
        "dossiers": [
            {
                "seatId": "#1250", "fund": "argon", "chair": "Creaking Wooden Swivel", "tier": "Class II Clerk",
                "briefcase": "0x4455...6677 · 30,000 $TMF", "pass": "Soulbound (Valid)", "deng": "130 Days · 1.64 Credits",
                "portraitKey": "p_argon_5", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Desk clerk in good standing. Committed to orderly administration of fund books."
            },
            {
                "seatId": "#2600", "fund": "midas", "chair": "Deep Button Chesterfield", "tier": "Class V Trustee",
                "briefcase": "0x8899...aabb · 85,000 $TMF", "pass": "Soulbound (Valid)", "deng": "145 Days · 1.70 Credits",
                "portraitKey": "p_midas_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Senior bullion trustee. Recommends locking dividend checks in escrow until the annual report."
            },
            {
                "seatId": "#0333", "fund": "bogle", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0xccdd...eeff · 48,000 $TMF", "pass": "Soulbound (Valid)", "deng": "115 Days · 1.58 Credits",
                "portraitKey": "p_bogle_1", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Bogle officer. Recommends balanced weighting across the 4,000 active chairs."
            },
            {
                "seatId": "#3666", "fund": "argon", "chair": "Deep Button Chesterfield", "tier": "Class V Trustee",
                "briefcase": "0xdead...beef · 0 $TMF", "pass": "Stolen Pass", "deng": "1 Day · 0.01 Credits",
                "portraitKey": "p_argon_3", "isAnomaly": True, "correctVerdict": "DECLINED",
                "memo": "Pass reported compromised from the Waiting Room night safe. Applicant refused to provide identification."
            }
        ]
    },
    {
        "week": 9,
        "title": "Week 9: The Liquidity Squeeze",
        "note": "Market panic. AMM till under heavy strain. Mailroom dispatches are vital to maintain Postage pool.",
        "dossiers": [
            {
                "seatId": "#1500", "fund": "smaug", "chair": "Creaking Wooden Swivel", "tier": "Class II Clerk",
                "briefcase": "0x1111...2222 · 60,000 $TMF", "pass": "Soulbound (Valid)", "deng": "185 Days · 1.86 Credits",
                "portraitKey": "p_smaug_3", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Smaug member depositing fresh liquidity into the till to offset market outflows."
            },
            {
                "seatId": "#3111", "fund": "vladd", "chair": "Beige Task Chair", "tier": "Class II Clerk",
                "briefcase": "0x3333...4444 · 38,000 $TMF", "pass": "Soulbound (Valid)", "deng": "150 Days · 1.72 Credits",
                "portraitKey": "p_vladd_3", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Contrarian applicant capitalizing on the drawdown to acquire distressed chairs."
            },
            {
                "seatId": "#0777", "fund": "argon", "chair": "The Interns Folding Chair", "tier": "Class I Intern",
                "briefcase": "0x5555...6666 · 15,000 $TMF", "pass": "Soulbound (Valid)", "deng": "105 Days · 1.52 Credits",
                "portraitKey": "p_argon_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Calm index holder. Refuses to panic sell despite wild volatility."
            },
            {
                "seatId": "#2999", "fund": "bogle", "chair": "Beige Task Chair", "tier": "Class II Clerk",
                "briefcase": "0x9999...0000 · 1,000 $TMF", "pass": "Counterfeit Voucher", "deng": "10 Days · 0.30 Credits",
                "portraitKey": "p_bogle_3", "isAnomaly": True, "correctVerdict": "DECLINED",
                "memo": "Applicant tendered invalid ApeChain receipt. Attempted to slip forged envelope across the blotter."
            }
        ]
    },
    {
        "week": 10,
        "title": "Week 10: The Counterfeit Seals",
        "note": "Forged rubber stamps identified in circulation. Verify seal ink and rotation closely.",
        "dossiers": [
            {
                "seatId": "#1800", "fund": "midas", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0x7777...8888 · 65,000 $TMF", "pass": "Soulbound (Valid)", "deng": "135 Days · 1.65 Credits",
                "portraitKey": "p_midas_1", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Midas officer with verified seal impression. Portfolio holds 100% gold-reserve parity."
            },
            {
                "seatId": "#0444", "fund": "smaug", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0xaaaa...bbbb · 98,000 $TMF", "pass": "Soulbound (Valid)", "deng": "205 Days · 1.94 Credits",
                "portraitKey": "p_smaug_4", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Treasury custodian verifying that no unbacked vouchers exist in the Smaug vault."
            },
            {
                "seatId": "#3555", "fund": "vladd", "chair": "Deep Button Chesterfield", "tier": "Class V Trustee",
                "briefcase": "0xcccc...dddd · 125,000 $TMF", "pass": "Soulbound (Valid)", "deng": "190 Days · 1.88 Credits",
                "portraitKey": "p_vladd_1", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Veteran distressed operator pledging full support for the continued survival of all five funds."
            },
            {
                "seatId": "#1111", "fund": "argon", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0x6666...0000 · 2,000 $TMF", "pass": "Counterfeit Stamp", "deng": "18 Days · 0.48 Credits",
                "portraitKey": "p_argon_4", "isAnomaly": True, "correctVerdict": "FLAGGED",
                "memo": "Dossier bears a counterfeit rubber stamp using modern font. Suspected syndicate plant."
            }
        ]
    },
    {
        "week": 11,
        "title": "Week 11: The Whistleblower",
        "note": "Confidential leak confirms syndicate attempting hostile liquidation at Week 13 Continuation Vote.",
        "dossiers": [
            {
                "seatId": "#2100", "fund": "bogle", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0xeeee...ffff · 92,000 $TMF", "pass": "Soulbound (Valid)", "deng": "155 Days · 1.74 Credits",
                "portraitKey": "p_bogle_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Whistleblower file. Provides evidence of syndicate wallets aiming to dissolve the mutual fund."
            },
            {
                "seatId": "#1200", "fund": "argon", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0x1122...4455 · 40,000 $TMF", "pass": "Soulbound (Valid)", "deng": "125 Days · 1.60 Credits",
                "portraitKey": "p_argon_1", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Argon officer voting against any dissolution motions on the upcoming Proxy Ballot."
            },
            {
                "seatId": "#3777", "fund": "midas", "chair": "Tasteful Walnut Lounge", "tier": "Class III Executive",
                "briefcase": "0x2233...5566 · 58,000 $TMF", "pass": "Soulbound (Valid)", "deng": "110 Days · 1.55 Credits",
                "portraitKey": "p_midas_4", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Gold desk shareholder committing all dividend checks to bolster vault liquidity."
            },
            {
                "seatId": "#0666", "fund": "smaug", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0xbeef...1337 · 100 $TMF", "pass": "Syndicate Proxy", "deng": "5 Days · 0.15 Credits",
                "portraitKey": "p_smaug_5", "isAnomaly": True, "correctVerdict": "DECLINED",
                "memo": "Operative identified in whistleblower leak. Explicit mission: vote YES on fund dissolution."
            }
        ]
    },
    {
        "week": 12,
        "title": "Week 12: The Final Ledger Audit",
        "note": "One week remaining before the Continuation Vote. Lock in legitimate voters across the five books.",
        "dossiers": [
            {
                "seatId": "#3333", "fund": "vladd", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0x7788...1122 · 72,000 $TMF", "pass": "Soulbound (Valid)", "deng": "160 Days · 1.76 Credits",
                "portraitKey": "p_vladd_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Vladd trustee voting NO on dissolution. Recommends strict adherence to fund covenants."
            },
            {
                "seatId": "#1444", "fund": "argon", "chair": "Deep Button Chesterfield", "tier": "Class V Trustee",
                "briefcase": "0x8899...2233 · 52,000 $TMF", "pass": "Soulbound (Valid)", "deng": "145 Days · 1.70 Credits",
                "portraitKey": "p_argon_3", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Argon trustee confirming full quorum support for continued operations."
            },
            {
                "seatId": "#0111", "fund": "bogle", "chair": "The Interns Folding Chair", "tier": "Class I Intern",
                "briefcase": "0x9900...3344 · 20,000 $TMF", "pass": "Soulbound (Valid)", "deng": "100 Days · 1.52 Credits",
                "portraitKey": "p_bogle_3", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Dedicated indexer pledging full voting weight to preserve the mutual fund."
            },
            {
                "seatId": "#2889", "fund": "midas", "chair": "Deep Button Chesterfield", "tier": "Class V Trustee",
                "briefcase": "0x0000...9999 · 50 $TMF", "pass": "Syndicate Proxy", "deng": "12 Days · 0.35 Credits",
                "portraitKey": "p_midas_2", "isAnomaly": True, "correctVerdict": "FLAGGED",
                "memo": "Hostile proxy buyer attempting to slip in before the ballot freezes at Friday bell."
            }
        ]
    },
    {
        "week": 13,
        "title": "Week 13: The Continuation Vote",
        "note": "The final bell. Quorum tally underway. Every stamped verdict determines the fate of the building.",
        "dossiers": [
            {
                "seatId": "#4000", "fund": "smaug", "chair": "The Gilded Throne", "tier": "Class VII Sovereign",
                "briefcase": "0xaaaa...ffff · 250,000 $TMF", "pass": "Soulbound (Valid)", "deng": "240 Days · 2.10 Credits",
                "portraitKey": "p_smaug_2", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Final vote for Smaug treasury survival. Pledges entire briefcase to the continued life of the fund."
            },
            {
                "seatId": "#3998", "fund": "vladd", "chair": "Oxblood Wingback", "tier": "Class V Partner",
                "briefcase": "0xbbbb...eeee · 115,000 $TMF", "pass": "Soulbound (Valid)", "deng": "180 Days · 1.84 Credits",
                "portraitKey": "p_vladd_4", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Contrarian leader casting vote to reject liquidation and keep all five books open."
            },
            {
                "seatId": "#1987", "fund": "argon", "chair": "Green Bankers Chair", "tier": "Class IV Officer",
                "briefcase": "0xcccc...dddd · 64,000 $TMF", "pass": "Soulbound (Valid)", "deng": "150 Days · 1.72 Credits",
                "portraitKey": "p_argon_1", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "The final Argon vote. Unmoved by panic, noble, and casting ballot for permanence."
            },
            {
                "seatId": "#0001", "fund": "bogle", "chair": "Deep Button Chesterfield", "tier": "Class V Trustee",
                "briefcase": "0xdddd...cccc · 140,000 $TMF", "pass": "Soulbound (Valid)", "deng": "190 Days · 1.88 Credits",
                "portraitKey": "p_bogle_5", "isAnomaly": False, "correctVerdict": "ADMITTED",
                "memo": "Founding seat candidate. The haystack must remain whole. Casts vote for perpetual continuation."
            }
        ]
    }
]

# 3. Read template parts
css_and_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Mutual Fun: The Thirteenth Week (1987)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap" rel="stylesheet">
  <style>
    :root {
      --paper: #F6EFE3;
      --paper-raised: #FDF8EE;
      --paper-sunken: #EDE3CF;
      --ink: #211B14;
      --ink-muted: #6B5F4E;
      --rule: #D8CCB4;
      --oxblood: #7A2E2E;
      --oxblood-deep: #5E2222;
      --gold: #B08A3C;
      --foil: #D4AF37;
      --lamp: #2F6B3D;
      --argon: #49698C;
      --bogle: #4E8A5A;
      --smaug: #9C5248;
      --midas: #B9902F;
      --vladd: #6E5D8C;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

    body {
      background: #110d0a;
      color: var(--ink);
      font-family: 'Source Serif 4', Georgia, serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px 16px 40px;
      position: relative;
      overflow-x: hidden;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at 50% 8%, rgba(47, 107, 61, 0.22) 0%, transparent 65%),
                  radial-gradient(circle at 50% 50%, rgba(28, 18, 14, 0.95), #080504);
      z-index: -2;
    }

    .header-bar {
      max-width: 1240px;
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .brass-plaque {
      background: linear-gradient(180deg, #c79b4b 0%, #8f6826 40%, #573e13 100%);
      border: 2px solid #e5c178;
      border-radius: 4px;
      padding: 6px 24px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.4);
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brass-plaque h1 {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 18px;
      letter-spacing: 2px;
      color: #1a1207;
      text-shadow: 0 1px 0 rgba(255, 255, 255, 0.3);
      text-transform: uppercase;
      font-weight: 700;
    }

    .brass-plaque .sub {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      letter-spacing: 1px;
      color: #2b1d09;
      font-weight: 600;
      border-left: 1px solid rgba(0,0,0,0.25);
      padding-left: 12px;
    }

    .game-stats-ribbon {
      display: flex;
      gap: 14px;
      background: rgba(22, 16, 12, 0.9);
      border: 1px solid #3d2d20;
      padding: 6px 16px;
      border-radius: 4px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      color: #bfaea0;
      align-items: center;
    }

    .game-stats-ribbon span b { color: #e5c178; }
    .game-stats-ribbon .week-pill {
      background: var(--oxblood);
      color: var(--paper-raised);
      padding: 2px 8px;
      font-weight: 600;
      border-radius: 2px;
      letter-spacing: 1px;
    }

    .contract-bar {
      max-width: 1240px;
      width: 100%;
      background: #19120d;
      border: 1px solid #2e2117;
      padding: 5px 14px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: #7d6b5b;
      flex-wrap: wrap;
      gap: 10px;
    }

    .contract-bar span b { color: #a8947f; }

    .main-workspace {
      max-width: 1240px;
      width: 100%;
      display: grid;
      grid-template-columns: 280px 1fr 310px;
      gap: 20px;
      align-items: start;
    }

    @media (max-width: 1100px) {
      .main-workspace { grid-template-columns: 1fr; }
    }

    .sheet-panel {
      background: var(--paper-raised);
      border: 1px solid var(--rule);
      box-shadow: 0 8px 25px rgba(0,0,0,0.4), inset 0 0 0 1px #fff;
      padding: 16px;
      position: relative;
    }

    .panel-title {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 14px;
      font-weight: 700;
      color: var(--ink);
      border-bottom: 2px solid var(--ink);
      padding-bottom: 5px;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }

    .fund-cards-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .fund-entry {
      border: 1px solid var(--rule);
      background: #faf6ee;
      padding: 8px 10px;
      transition: all 0.12s ease;
      cursor: pointer;
    }

    .fund-entry:hover, .fund-entry.active {
      border-color: var(--ink);
      background: #fff;
      box-shadow: 2px 2px 0 var(--ink);
    }

    .fund-tag {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 9px;
      font-weight: 600;
      color: #fff;
      padding: 1px 5px;
      border-radius: 2px;
      display: inline-block;
      margin-bottom: 3px;
    }

    .fund-name-row {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--ink);
      display: flex;
      justify-content: space-between;
    }

    .fund-motto-txt {
      font-size: 10px;
      font-style: italic;
      color: var(--ink-muted);
      line-height: 1.3;
      margin-top: 2px;
    }

    .fund-numbers {
      margin-top: 5px;
      padding-top: 4px;
      border-top: 1px dashed var(--rule);
      display: flex;
      justify-content: space-between;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
    }

    .fund-progress-bar {
      height: 4px;
      background: var(--paper-sunken);
      margin-top: 4px;
      overflow: hidden;
      border-radius: 1px;
    }

    .fund-progress-fill {
      height: 100%;
      transition: width 0.3s ease;
    }

    /* Center: Dossier Paper */
    .dossier-paper {
      background: var(--paper);
      border: 2px solid var(--ink);
      box-shadow: 0 12px 35px rgba(0,0,0,0.5), 4px 4px 0 rgba(0,0,0,0.25);
      padding: 24px 28px 24px;
      position: relative;
      background-image: 
        radial-gradient(circle at 100% 0%, rgba(122, 46, 46, 0.03) 0%, transparent 40%),
        repeating-linear-gradient(0deg, transparent, transparent 23px, rgba(216, 204, 180, 0.3) 24px);
    }

    .dossier-engraved-border {
      position: absolute;
      inset: 7px;
      border: 1px solid var(--rule);
      pointer-events: none;
    }

    .dossier-engraved-border::after {
      content: "";
      position: absolute;
      inset: 2px;
      border: 1px solid rgba(33, 27, 20, 0.12);
    }

    .dossier-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--ink);
      padding-bottom: 10px;
      margin-bottom: 16px;
    }

    .medallion-mark {
      width: 44px;
      height: 44px;
      object-fit: contain;
    }

    .dossier-titles { text-align: center; }
    .dossier-titles h2 {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 20px;
      font-weight: 700;
      color: var(--oxblood);
      letter-spacing: 1.5px;
      text-transform: uppercase;
    }

    .dossier-titles p {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 11px;
      font-variant: small-caps;
      letter-spacing: 1.5px;
      color: var(--ink-muted);
    }

    .dossier-badge-number {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      text-align: right;
      color: var(--ink);
      font-weight: 600;
    }

    .dossier-body-grid {
      display: grid;
      grid-template-columns: 140px 1fr;
      gap: 18px;
      margin-bottom: 14px;
    }

    .portrait-box {
      background: #faf6ee;
      border: 2px solid var(--ink);
      padding: 6px;
      text-align: center;
      box-shadow: 2px 2px 0 var(--rule);
    }

    .portrait-canvas-img {
      width: 124px;
      height: 124px;
      image-rendering: pixelated;
      image-rendering: crisp-edges;
      border: 1px solid var(--rule);
      background: #fff;
      display: block;
    }

    .chair-caption {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 11px;
      color: var(--ink);
      margin-top: 5px;
      line-height: 1.2;
      font-style: italic;
    }

    .chair-tier-tag {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 9px;
      color: var(--oxblood);
      font-weight: 600;
      text-transform: uppercase;
      margin-top: 2px;
    }

    .dossier-details {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .dossier-row {
      display: grid;
      grid-template-columns: 115px 1fr;
      font-size: 12px;
      border-bottom: 1px dotted var(--rule);
      padding-bottom: 3px;
    }

    .dossier-row .lbl {
      font-family: 'Source Serif 4', Georgia, serif;
      font-variant: small-caps;
      letter-spacing: 1px;
      color: var(--ink-muted);
    }

    .dossier-row .val {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      color: var(--ink);
      font-weight: 500;
    }

    .dossier-statement-box {
      background: var(--paper-sunken);
      border: 1px solid var(--rule);
      padding: 8px 12px;
      margin-top: 4px;
      border-left: 3px solid var(--oxblood);
    }

    .dossier-statement-box p {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 11px;
      line-height: 1.45;
      color: var(--ink);
    }

    .anomaly-flag-box {
      background: #fbf0f0;
      border: 1px solid #d49a9a;
      padding: 6px 10px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: var(--oxblood-deep);
      margin-top: 4px;
      display: none;
    }

    .stamp-target-plate {
      position: relative;
      height: 80px;
      border: 1px dashed var(--rule);
      margin: 12px 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(253, 248, 238, 0.5);
    }

    .stamp-guide-text {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 11px;
      font-style: italic;
      color: var(--ink-muted);
    }

    .rubber-impression {
      position: absolute;
      padding: 4px 18px;
      border: 4px solid;
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 26px;
      font-weight: 700;
      letter-spacing: 3px;
      text-transform: uppercase;
      opacity: 0;
      pointer-events: none;
      transition: all 0.15s cubic-bezier(0.18, 0.89, 0.32, 1.28);
      mix-blend-mode: multiply;
      transform: scale(0.85);
    }

    .rubber-impression.visible {
      opacity: 0.94;
      transform: rotate(var(--rot, -3deg)) scale(1);
    }

    .rubber-impression.admitted { color: var(--lamp); border-color: var(--lamp); }
    .rubber-impression.pending  { color: var(--gold); border-color: var(--gold); }
    .rubber-impression.flagged  { color: var(--oxblood); border-color: var(--oxblood); }
    .rubber-impression.declined { color: var(--ink); border-color: var(--ink); }

    .rubber-stamp-rack {
      border-top: 2px solid var(--ink);
      padding-top: 10px;
      text-align: center;
    }

    .rack-label {
      font-family: 'Source Serif 4', Georgia, serif;
      font-variant: small-caps;
      letter-spacing: 2px;
      font-size: 10px;
      color: var(--ink-muted);
      margin-bottom: 8px;
    }

    .stamp-buttons-row {
      display: flex;
      gap: 10px;
      justify-content: center;
      flex-wrap: wrap;
    }

    .stamp-tool-btn {
      background: linear-gradient(180deg, #f7efe4 0%, #dcd0be 100%);
      border: 2px solid #5a4631;
      padding: 8px 14px;
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      cursor: pointer;
      box-shadow: 0 4px 0 #3a2b1b, 0 5px 6px rgba(0,0,0,0.3);
      position: relative;
      transition: all 0.06s ease;
      text-transform: uppercase;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
    }

    .stamp-tool-btn span.handle {
      display: block;
      width: 14px;
      height: 3px;
      background: #7a5835;
      border-radius: 2px;
    }

    .stamp-tool-btn:active {
      transform: translateY(4px);
      box-shadow: 0 0 0 #3a2b1b, 0 1px 2px rgba(0,0,0,0.2);
    }

    .stamp-tool-btn.btn-admitted { color: var(--lamp); }
    .stamp-tool-btn.btn-pending  { color: #8f6826; }
    .stamp-tool-btn.btn-flagged  { color: var(--oxblood); }
    .stamp-tool-btn.btn-declined { color: var(--ink); }

    .dossier-nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 14px;
    }

    .desk-button {
      background: var(--ink);
      color: var(--paper-raised);
      border: 1px solid var(--ink);
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 12px;
      padding: 6px 12px;
      cursor: pointer;
      transition: background 0.12s ease;
    }

    .desk-button:hover {
      background: var(--oxblood);
      border-color: var(--oxblood);
    }

    .desk-button.secondary {
      background: transparent;
      color: var(--ink);
      border-color: var(--rule);
    }

    .desk-button.secondary:hover {
      background: var(--paper-sunken);
      border-color: var(--ink);
    }

    /* Right Sidebar */
    .right-sidebar {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .amm-box {
      background: #18120e;
      border: 1px solid #3d2f24;
      color: #ede3cf;
      padding: 14px;
    }

    .amm-title {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 13px;
      color: #c9a86a;
      border-bottom: 1px solid #3d2f24;
      padding-bottom: 4px;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
    }

    .amm-rate-display {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 16px;
      color: #f6efe3;
      font-weight: 600;
      margin: 4px 0 8px;
    }

    .amm-rate-display small { font-size: 10px; color: #8c7b68; }

    .amm-deal-rows {
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
    }

    .amm-deal-row {
      display: flex;
      justify-content: space-between;
      padding: 4px 6px;
      background: #241c16;
      align-items: center;
    }

    .amm-action-btn {
      background: var(--oxblood);
      color: #f6efe3;
      border: none;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      padding: 2px 7px;
      cursor: pointer;
      border-radius: 1px;
    }

    .amm-action-btn:hover { background: #9c3f3f; }

    .merger-box {
      background: var(--paper-raised);
      border: 1px solid var(--rule);
      padding: 12px;
    }

    .merger-chairs-preview {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 8px 0;
      gap: 4px;
    }

    .chair-thumb { width: 55px; text-align: center; }
    .chair-thumb img {
      width: 44px;
      height: 44px;
      image-rendering: pixelated;
      border: 1px solid var(--rule);
      background: #fff;
    }

    .chair-thumb p { font-size: 8px; line-height: 1.1; margin-top: 2px; }

    .mailroom-box {
      background: #faf6ee;
      border: 1px solid var(--rule);
      padding: 12px;
    }

    .dispatch-log-panel {
      max-width: 1240px;
      width: 100%;
      margin-top: 18px;
      background: #18120e;
      border: 1px solid #33261c;
      padding: 10px 16px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      color: #bfaea0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .log-feed {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #c9a86a;
    }

    .bell-dot {
      width: 8px;
      height: 8px;
      background: #c9a86a;
      border-radius: 50%;
      box-shadow: 0 0 6px #c9a86a;
      animation: pulse 2s infinite;
    }

    @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }

    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(10, 7, 5, 0.85);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 100;
      padding: 20px;
    }

    .modal-overlay.active { display: flex; }

    .modal-sheet {
      background: var(--paper);
      border: 3px solid var(--ink);
      max-width: 580px;
      width: 100%;
      padding: 28px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8);
      position: relative;
    }

    .modal-sheet h3 {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 20px;
      color: var(--oxblood);
      margin-bottom: 6px;
      text-transform: uppercase;
      border-bottom: 1px solid var(--ink);
      padding-bottom: 8px;
    }

    .modal-sheet p {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 13px;
      line-height: 1.5;
      color: var(--ink);
      margin-top: 10px;
      white-space: pre-line;
    }

    .modal-sheet .quote {
      background: var(--paper-sunken);
      border-left: 3px solid var(--oxblood);
      padding: 8px 12px;
      font-style: italic;
      margin: 12px 0;
      font-size: 12px;
    }

    .modal-actions {
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      margin-top: 18px;
    }
  </style>
</head>
<body>

  <div class="header-bar">
    <div class="brass-plaque">
      <img src="__MEDALLION_B64__" style="width:36px;height:36px;object-fit:contain;" alt="Seal">
      <div>
        <h1>The Mutual Fun</h1>
      </div>
      <div class="sub">
        EST. 1987 · ROBINHOOD CHAIN · WAITING ROOM DESK
      </div>
    </div>

    <div class="game-stats-ribbon">
      <span class="week-pill" id="weekDisplay">WEEK 1 / 13</span>
      <span>Postage: <b id="postageDisplay">0.050 ETH</b></span>
      <span>$TMF Till: <b id="tmfTillDisplay">1,402,000</b></span>
      <span>Reputation: <b id="repDisplay">100%</b></span>
    </div>
  </div>

  <div class="contract-bar">
    <span><b>Deployer:</b> 0x4609585Ac28c827678B1554DfcE3bc6b411dAa3e</span>
    <span><b>Vault:</b> 0x48dF666dA1D12c952aFfCda214e30958a512A118</span>
    <span><b>TMF Pass CA:</b> 0xED37605FF0e513e46d50B26244DEb2024189751a</span>
    <span><b>Cap:</b> 4,001 Seats (Seat 0: Chairman)</span>
  </div>

  <div class="main-workspace">

    <div class="sheet-panel">
      <div class="panel-title">
        <span>The Five Funds</span>
        <span style="font-family:'IBM Plex Mono';font-size:10px;color:var(--ink-muted);">Target: 800 Seats</span>
      </div>
      <div class="fund-cards-list" id="fundListEl"></div>
    </div>

    <div class="dossier-paper">
      <div class="dossier-engraved-border"></div>

      <div class="dossier-header">
        <img src="__MEDALLION_B64__" class="medallion-mark" alt="Medallion">
        <div class="dossier-titles">
          <h2>Shareholder Intake Dossier</h2>
          <p id="dossierSubtitle">Waiting Room Desk · File 1987-W01</p>
        </div>
        <div class="dossier-badge-number">
          <span style="color:var(--ink-muted);font-size:9px;display:block;">SEAT LOT</span>
          <span id="dossierSeatId">#1402</span>
        </div>
      </div>

      <div class="dossier-body-grid">
        <div class="portrait-box">
          <img id="dossierPortraitImg" src="" class="portrait-canvas-img" alt="Shareholder Portrait">
          <div class="chair-caption" id="dossierChairName">Green Bankers Chair</div>
          <div class="chair-tier-tag" id="dossierChairTier">Class IV Officer</div>
        </div>

        <div class="dossier-details">
          <div class="dossier-row">
            <span class="lbl">Assigned Fund</span>
            <span class="val" id="dossierFundName" style="font-weight:700;">The Argon Fund</span>
          </div>
          <div class="dossier-row">
            <span class="lbl">Briefcase (TBA)</span>
            <span class="val" id="dossierBriefcase">0x81fa...91bc · 28,400 $TMF</span>
          </div>
          <div class="dossier-row">
            <span class="lbl">TMF Pass Status</span>
            <span class="val" id="dossierPass">Soulbound (2 Chairs Minted)</span>
          </div>
          <div class="dossier-row">
            <span class="lbl">Deng Desk Tenure</span>
            <span class="val" id="dossierDeng">128 Days · 1.62 Credits</span>
          </div>

          <div class="dossier-statement-box">
            <p id="dossierMemo"></p>
          </div>

          <div class="anomaly-flag-box" id="anomalyAlert">
            AUDIT NOTICE: File credentials flagged for desk review. Inspect ApeChain tenure and seal before stamping.
          </div>
        </div>
      </div>

      <div class="stamp-target-plate">
        <span class="stamp-guide-text" id="stampGuideText">Select an official verdict from the stamp rack below.</span>
        <div class="rubber-impression" id="rubberStampImpression">ADMITTED</div>
      </div>

      <div class="rubber-stamp-rack">
        <div class="rack-label">Desk Stamps · Official Verdicts Only</div>
        <div class="stamp-buttons-row">
          <button class="stamp-tool-btn btn-admitted" onclick="stampDossier('ADMITTED', 'admitted')">
            <span class="handle"></span>
            Admitted
          </button>
          <button class="stamp-tool-btn btn-pending" onclick="stampDossier('PENDING', 'pending')">
            <span class="handle"></span>
            Pending
          </button>
          <button class="stamp-tool-btn btn-flagged" onclick="stampDossier('FLAGGED', 'flagged')">
            <span class="handle"></span>
            Flagged
          </button>
          <button class="stamp-tool-btn btn-declined" onclick="stampDossier('DECLINED', 'declined')">
            <span class="handle"></span>
            Declined
          </button>
        </div>
      </div>

      <div class="dossier-nav-bar">
        <button class="desk-button secondary" onclick="prevDossier()">Previous Dossier</button>
        <span style="font-family:'IBM Plex Mono';font-size:11px;color:var(--ink-muted);" id="dossierProgressText">Dossier 1 of 4</span>
        <button class="desk-button" onclick="nextDossier()">Next Dossier</button>
      </div>

    </div>

    <div class="right-sidebar">

      <div class="amm-box">
        <div class="amm-title">
          <span>The Open Market</span>
          <span style="font-size:10px;">Anvil AMM</span>
        </div>
        <div style="font-size:10px; color:#8c7b68;">Base House Rate:</div>
        <div class="amm-rate-display">401,000 <small>$TMF / Seat</small></div>

        <div class="amm-deal-rows">
          <div class="amm-deal-row">
            <span>Random Shelf (+8%)</span>
            <span>433,080 $TMF</span>
            <button class="amm-action-btn" onclick="tradeAMM('random')">Buy</button>
          </div>
          <div class="amm-deal-row">
            <span>Handpick (+16%)</span>
            <span>465,160 $TMF</span>
            <button class="amm-action-btn" onclick="tradeAMM('pick')">Pick</button>
          </div>
          <div class="amm-deal-row">
            <span>Sell to Till (-8%)</span>
            <span>368,920 $TMF</span>
            <button class="amm-action-btn" onclick="tradeAMM('sell')">Sell</button>
          </div>
        </div>
      </div>

      <div class="merger-box">
        <div class="panel-title" style="margin-bottom:6px;">
          <span>Fiscal Friday M&A</span>
          <span style="font-size:10px;color:var(--oxblood);font-family:'IBM Plex Mono';">Merger Lab</span>
        </div>
        <p style="font-size:10px;color:var(--ink-muted);line-height:1.3;margin-bottom:8px;">
          Merge two enrolled duplicate seats of the same class to climb the hierarchy. Briefcases combine.
        </p>

        <div class="merger-chairs-preview" id="mergerPreview"></div>

        <button class="desk-button" style="width:100%;text-align:center;font-size:11px;" onclick="executeMerger()">
          Execute Chair Upgrade
        </button>
      </div>

      <div class="mailroom-box">
        <div class="panel-title" style="margin-bottom:4px;">
          <span>The Mailroom</span>
          <span style="font-size:10px;color:var(--lamp);font-family:'IBM Plex Mono';">+0.015 ETH</span>
        </div>
        <p style="font-size:10px;color:var(--ink-muted);line-height:1.3;margin-bottom:8px;">
          Public tasks and dispatches. Clear ticker slips to earn Postage tips and maintain vault liquidity.
        </p>
        <button class="desk-button secondary" style="width:100%;font-size:11px;" onclick="runMailroomTask()">
          Run Weekly Dispatch
        </button>
      </div>

      <button class="desk-button" style="width:100%;padding:10px;background:var(--oxblood);font-size:13px;letter-spacing:1px;" onclick="endWeekRitual()">
        Ring Closing Bell (End Week)
      </button>

    </div>

  </div>

  <div class="dispatch-log-panel">
    <div class="log-feed">
      <div class="bell-dot"></div>
      <span id="logFeedText">LOBBY TICKER: ALL 5 FUNDS OPEN. SEAT 0 RESTS IN THE ROTUNDA. WAITING ROOM INTAKE ACTIVE.</span>
    </div>
    <div>
      <button class="desk-button secondary" style="font-size:10px;padding:3px 8px;" onclick="toggleAudio()">
        AUDIO: <span id="audioStateText">ON</span>
      </button>
    </div>
  </div>

  <div class="modal-overlay" id="storyModal">
    <div class="modal-sheet">
      <h3 id="modalTitle">Friday Closing Bell</h3>
      <p id="modalBody"></p>
      <div class="quote" id="modalQuote"></div>
      <div class="modal-actions">
        <button class="desk-button" onclick="closeStoryModal()">Acknowledge and Continue</button>
      </div>
    </div>
  </div>

  <script>
    const ASSETS = __ASSETS_JSON__;
    const CAMPAIGN = __CAMPAIGN_JSON__;

    let audioCtx = null;
    let audioEnabled = true;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById('audioStateText').innerText = audioEnabled ? "ON" : "MUTED";
      if (audioEnabled) playClick();
    }

    function playStampThump() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(95, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(28, audioCtx.currentTime + 0.28);
        gain.gain.setValueAtTime(0.85, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.38);

        const bSize = audioCtx.sampleRate * 0.12;
        const b = audioCtx.createBuffer(1, bSize, audioCtx.sampleRate);
        const d = b.getChannelData(0);
        for (let i = 0; i < bSize; i++) d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (audioCtx.sampleRate * 0.025));
        const n = audioCtx.createBufferSource();
        n.buffer = b;
        const ng = audioCtx.createGain();
        ng.gain.setValueAtTime(0.35, audioCtx.currentTime);
        n.connect(ng);
        ng.connect(audioCtx.destination);
        n.start();
      } catch(e) {}
    }

    function playClick() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(1400, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.05);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.06);
      } catch(e) {}
    }

    function playPaper() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const bSize = audioCtx.sampleRate * 0.12;
        const b = audioCtx.createBuffer(1, bSize, audioCtx.sampleRate);
        const d = b.getChannelData(0);
        for (let i = 0; i < bSize; i++) d[i] = (Math.random() * 2 - 1) * 0.07;
        const n = audioCtx.createBufferSource();
        n.buffer = b;
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(1100, audioCtx.currentTime);
        n.connect(filter);
        filter.connect(audioCtx.destination);
        n.start();
      } catch(e) {}
    }

    function playBell() {
      if (!audioEnabled) return;
      initAudio();
      try {
        [523.25, 659.25, 783.99].forEach((freq, idx) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime + idx * 0.15);
          gain.gain.setValueAtTime(0.3, audioCtx.currentTime + idx * 0.15);
          gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + idx * 0.15 + 1.8);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(audioCtx.currentTime + idx * 0.15);
          osc.stop(audioCtx.currentTime + idx * 0.15 + 1.9);
        });
      } catch(e) {}
    }

    let currentWeek = 1;
    let postageETH = 0.050;
    let tmfTill = 1402000;
    let deskReputation = 100;
    let currentDossierIndex = 0;

    const funds = {
      argon: { name: "The Argon Fund", tag: "ARGON", color: "#49698C", motto: "Noble, inert, and unmoved by the news.", seats: 742, book: 4200000 },
      bogle: { name: "The Bogle Fund", tag: "BOGLE", color: "#4E8A5A", motto: "Buys the whole haystack.", seats: 789, book: 5800000 },
      smaug: { name: "The Smaug Fund", tag: "SMAUG", color: "#9C5248", motto: "Sleeps on the pile and knows every coin in it.", seats: 698, book: 8100000 },
      midas: { name: "The Midas Fund", tag: "MIDAS", color: "#B9902F", motto: "Everything it touches, marked to gold.", seats: 755, book: 6400000 },
      vladd: { name: "The Vladd Fund", tag: "VLADD", color: "#6E5D8C", motto: "Buys when there is blood in the streets.", seats: 712, book: 3900000 }
    };

    function renderFundCards() {
      const el = document.getElementById('fundListEl');
      el.innerHTML = '';
      Object.keys(funds).forEach(k => {
        const f = funds[k];
        const pct = Math.min(100, Math.round((f.seats / 800) * 100));
        const div = document.createElement('div');
        div.className = 'fund-entry';
        div.innerHTML = `
          <span class="fund-tag" style="background:${f.color};">${f.tag}</span>
          <div class="fund-name-row">
            <span>${f.name}</span>
            <span style="font-family:'IBM Plex Mono';font-size:11px;">${f.seats}/800</span>
          </div>
          <div class="fund-motto-txt">${f.motto}</div>
          <div class="fund-numbers">
            <span>Book: $${(f.book / 1000000).toFixed(1)}M</span>
            <span>Quorum: ${pct}%</span>
          </div>
          <div class="fund-progress-bar">
            <div class="fund-progress-fill" style="width:${pct}%; background:${f.color};"></div>
          </div>
        `;
        el.appendChild(div);
      });
    }

    function renderDossier() {
      const weekData = CAMPAIGN[currentWeek - 1];
      const dossier = weekData.dossiers[currentDossierIndex];

      document.getElementById('weekDisplay').innerText = `WEEK ${currentWeek} / 13`;
      document.getElementById('dossierSubtitle').innerText = `Waiting Room Desk · File 1987-W${currentWeek.toString().padStart(2, '0')}`;
      document.getElementById('dossierSeatId').innerText = dossier.seatId;
      document.getElementById('dossierPortraitImg').src = ASSETS[dossier.portraitKey] || '';
      document.getElementById('dossierChairName').innerText = dossier.chair;
      document.getElementById('dossierChairTier').innerText = dossier.tier;

      const fInfo = funds[dossier.fund];
      const fundNameEl = document.getElementById('dossierFundName');
      fundNameEl.innerText = fInfo.name;
      fundNameEl.style.color = fInfo.color;

      document.getElementById('dossierBriefcase').innerText = dossier.briefcase;
      document.getElementById('dossierPass').innerText = dossier.pass;
      document.getElementById('dossierDeng').innerText = dossier.deng;
      document.getElementById('dossierMemo').innerText = dossier.memo;

      const alertBox = document.getElementById('anomalyAlert');
      if (dossier.isAnomaly) {
        alertBox.style.display = 'block';
      } else {
        alertBox.style.display = 'none';
      }

      const stampEl = document.getElementById('rubberStampImpression');
      stampEl.className = 'rubber-impression';
      document.getElementById('stampGuideText').style.display = 'block';

      document.getElementById('dossierProgressText').innerText = `Dossier ${currentDossierIndex + 1} of ${weekData.dossiers.length}`;

      renderMergerPreview(dossier.fund);
      playPaper();
    }

    function renderMergerPreview(fundKey) {
      const container = document.getElementById('mergerPreview');
      const f = funds[fundKey];
      container.innerHTML = `
        <div class="chair-thumb">
          <img src="${ASSETS.p_bogle_3}" alt="Folding Chair">
          <p>Folding</p>
        </div>
        <span style="font-weight:700;color:var(--ink-muted);">+</span>
        <div class="chair-thumb">
          <img src="${ASSETS.p_bogle_3}" alt="Folding Chair">
          <p>Folding</p>
        </div>
        <span style="font-weight:700;color:var(--oxblood);">➜</span>
        <div class="chair-thumb">
          <img src="${ASSETS.p_argon_1}" alt="Bankers Chair" style="border:2px solid ${f.color};">
          <p style="font-weight:700;color:${f.color};">Bankers</p>
        </div>
      `;
    }

    function nextDossier() {
      const weekData = CAMPAIGN[currentWeek - 1];
      currentDossierIndex = (currentDossierIndex + 1) % weekData.dossiers.length;
      renderDossier();
    }

    function prevDossier() {
      const weekData = CAMPAIGN[currentWeek - 1];
      currentDossierIndex = (currentDossierIndex - 1 + weekData.dossiers.length) % weekData.dossiers.length;
      renderDossier();
    }

    function stampDossier(verdict, cls) {
      playStampThump();
      const stampEl = document.getElementById('rubberStampImpression');
      stampEl.innerText = verdict;
      stampEl.className = `rubber-impression ${cls} visible`;
      
      const rot = (Math.random() * 8 - 4).toFixed(1);
      stampEl.style.setProperty('--rot', `${rot}deg`);
      document.getElementById('stampGuideText').style.display = 'none';

      const weekData = CAMPAIGN[currentWeek - 1];
      const dossier = weekData.dossiers[currentDossierIndex];

      if (dossier.isAnomaly) {
        if (verdict === "FLAGGED" || verdict === "DECLINED") {
          deskReputation = Math.min(100, deskReputation + 2);
          updateTicker(`AUDIT PASS: Suspect file correctly ${verdict.toLowerCase()}. Syndicate prevented.`);
        } else {
          deskReputation = Math.max(0, deskReputation - 10);
          updateTicker(`SECURITY BREACH: Hostile file ${verdict.toLowerCase()}. Reputation penalized.`);
        }
      } else {
        if (verdict === "ADMITTED") {
          funds[dossier.fund].seats = Math.min(800, funds[dossier.fund].seats + 1);
          funds[dossier.fund].book += 50000;
          updateTicker(`SEAT CONFERRED: Admitted to ${funds[dossier.fund].name}. Quorum increased.`);
        } else {
          deskReputation = Math.max(0, deskReputation - 4);
          updateTicker(`INCONVENIENCE: Legitimate shareholder ${verdict.toLowerCase()}.`);
        }
      }

      updateUI();
    }

    function updateUI() {
      document.getElementById('repDisplay').innerText = `${deskReputation}%`;
      document.getElementById('postageDisplay').innerText = `${postageETH.toFixed(3)} ETH`;
      document.getElementById('tmfTillDisplay').innerText = tmfTill.toLocaleString();
      renderFundCards();
    }

    function updateTicker(msg) {
      document.getElementById('logFeedText').innerText = `LOBBY TICKER: ${msg.toUpperCase()}`;
    }

    function tradeAMM(type) {
      playClick();
      if (type === 'random') {
        if (tmfTill >= 433080) {
          tmfTill += 433080;
          postageETH += 0.005;
          updateTicker("OPEN MARKET: Random shelf chair purchased (+8% premium). Till replenished.");
        }
      } else if (type === 'pick') {
        if (tmfTill >= 465160) {
          tmfTill += 465160;
          postageETH += 0.010;
          updateTicker("OPEN MARKET: Specific seat acquired (+16% premium). StonkBrokers fee routed.");
        }
      } else if (type === 'sell') {
        if (tmfTill >= 368920) {
          tmfTill -= 368920;
          updateTicker("OPEN MARKET: Chair sold back to till (-8% take). $TMF paid out.");
        } else {
          updateTicker("OPEN MARKET NOTICE: Till liquidity insufficient for buyback.");
        }
      }
      updateUI();
    }

    function executeMerger() {
      playStampThump();
      const weekData = CAMPAIGN[currentWeek - 1];
      const dossier = weekData.dossiers[currentDossierIndex];
      const f = funds[dossier.fund];
      f.book += 120000;
      updateTicker(`M&A CONSOLIDATION: Two duplicate folding chairs consolidated into Green Bankers Chair under ${f.name}.`);
      updateUI();
    }

    function runMailroomTask() {
      playClick();
      postageETH += 0.015;
      tmfTill += 50000;
      deskReputation = Math.min(100, deskReputation + 1);
      updateTicker("MAILROOM TASK RUN: Dispatched weekly task on-chain. 0.015 ETH Postage earned.");
      updateUI();
    }

    function endWeekRitual() {
      playBell();
      const weekData = CAMPAIGN[currentWeek - 1];

      if (currentWeek < 13) {
        showStoryModal(
          `Fiscal Friday Bell: Week ${currentWeek}`,
          `The Closing Bell rings at 20:00 UTC. The books trade, dividend checks drop in kind into briefcases, and the ledger balances.\n\n${weekData.note}`,
          `"Every Friday at the bell: the books trade, the checks go out in kind."`
        );
        currentWeek++;
        currentDossierIndex = 0;
        renderDossier();
        updateUI();
      } else {
        const avgSeats = Object.values(funds).reduce((acc, f) => acc + f.seats, 0) / 5;
        let outcomeTitle = "Continuation Vote Result";
        let outcomeBody = "";
        let quote = "";

        if (deskReputation >= 75 && avgSeats >= 720) {
          outcomeTitle = "Ending A: The Chairman Medallion (Victory)";
          outcomeBody = `The Week 13 Continuation Vote concludes at the Closing Bell.\n\nAll five funds (Argon, Bogle, Smaug, Midas, Vladd) achieved overwhelming quorum. Every syndicate operative was flagged and expelled before seating. The vault remains 100% collateralized, dividend checks are distributed in kind across all 4,000 active briefcases, and Seat 0 rests in peace in the lobby.\n\nThe Chairman brass medallion is conferred upon your desk.`;
          quote = `"The house admits; it never invites. The five funds shall remain open in perpetuity."`;
        } else if (deskReputation < 50) {
          outcomeTitle = "Ending B: The Hostile Liquidation (Defeat)";
          outcomeBody = `The syndicate managed to seat sufficient voting proxies across the books.\n\nAt the 20:00 UTC bell, the Continuation Vote failed to achieve legitimate shareholder quorum. A forced liquidation resolution passed. The Open Market till has been frozen, and corporate liquidators have arrived with heavy brass padlocks to seal the headquarters doors.`;
          quote = `"A chair is only wood and leather. The building is officially sealed."`;
        } else {
          outcomeTitle = "Ending C: The Compromised Charter";
          outcomeBody = `Quorum was narrowly missed in Argon and Bogle, but Smaug and Vladd survived by consolidating their reserves.\n\nThe mutual fund survives in reduced form under an amended charter. The desk retains its post, but scrutiny from the Robinscan explorer will be unrelenting in the quarters ahead.`;
          quote = `"The books trade, but the margins remain thin."`;
        }

        showStoryModal(outcomeTitle, outcomeBody, quote);
      }
    }

    function showStoryModal(title, body, quote) {
      document.getElementById('modalTitle').innerText = title;
      document.getElementById('modalBody').innerText = body;
      document.getElementById('modalQuote').innerText = quote;
      document.getElementById('storyModal').classList.add('active');
    }

    function closeStoryModal() {
      document.getElementById('storyModal').classList.remove('active');
      playClick();
    }

    window.addEventListener('load', () => {
      renderFundCards();
      renderDossier();
      updateUI();
    });
  </script>
</body>
</html>
"""

# Inject serialized JSON data
final_html = css_and_html.replace('__MEDALLION_B64__', assets.get('medallion', ''))
final_html = final_html.replace('__ASSETS_JSON__', json.dumps(assets))
final_html = final_html.replace('__CAMPAIGN_JSON__', json.dumps(campaign_weeks))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

brain_path = r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html'
with open(brain_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Game built cleanly and written to index.html and brain index.html")
