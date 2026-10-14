"""Convert 2_deals.csv / TEST_deals.csv rows into HubSpot API payloads (internal property names)."""
import csv, json, sys
STAGES = {'Handover': '6220012735', 'Setup': '6220536008', 'Live': '6220536009', 'Renewal decision': '6220536010',
          'Paused': '6220536011', 'Ended': '6220019928', 'Cancelled': '6228758726'}
FIELDS = {'Deal Name': 'dealname', 'Amount': 'amount', 'Total budget': 'total_budget',
          'Monthly budget Open Web': 'monthly_budget_open_web', 'Monthly budget ChatGPT': 'monthly_budget_chatgpt',
          'Duration (days)': 'duration_days', 'CPC': 'cpc', 'Signature date': 'signature_date', 'Close Date': 'closedate',
          'Launch date': 'launch_date', 'Campaign end date': 'campaign_end_date', 'Network/ Agency': 'network_agency',
          'Inventory': 'inventory', 'Objective type': 'objective_type', 'Objective source': 'objective_source',
          'Objectives details': 'objectives_details', 'Product feed': 'product_feed', 'Outcome': 'outcome',
          'Churn reason': 'churn_reason', 'Churn details': 'churn_details'}
OWNER = '38675653'
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
out = []
for r in rows:
    props = {api: r[col] for col, api in FIELDS.items() if r[col] != ''}
    props.update(pipeline='4216622308', dealstage=STAGES[r['Deal Stage']], hubspot_owner_id=OWNER)
    obj = {'objectType': 'deals', 'properties': props}
    if r['Company Record ID']:
        obj['associations'] = [{'targetObjectType': 'COMPANY', 'targetObjectId': int(r['Company Record ID'])}]
    out.append(obj)
json.dump(out, sys.stdout, ensure_ascii=False)
