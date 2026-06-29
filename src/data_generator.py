import os
import random
import uuid
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TeslaRecruitingDataGenerator:
    def __init__(self, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        self.sources = ['LinkedIn', 'Employee Referral', 'Tesla Careers Site', 'University Recruiting', 'X (Twitter) Sourcing']
        self.departments = ['Manufacturing Engineering', 'Software Engineering', 'Artificial Intelligence', 'Robotics', 'Supply Chain', 'Tesla Energy']
        self.locations = ['Austin, TX', 'Fremont, CA', 'Berlin, Germany', 'Shanghai, China']
        self.stages_sequence = ['Applied', 'Phone Screen', 'Technical Interview', 'Offer Issued', 'Hired']
        
        self.recruiters = [
            {"recruiter_id": f"REC_{100+i}", "recruiter_name": name, "team": team}
            for i, (name, team) in enumerate([
                ("Alex Chen", "AI/Robotics"), ("Sarah Jenkins", "Gigafactory Manufacturing"),
                ("Marcus Vance", "Core Software"), ("Elena Rostova", "Global Supply Chain"),
                ("David Kim", "Energy Products")
            ])
        ]

    def generate_requisitions(self, num_reqs=50):
        req_list = []
        start_date = datetime(2025, 1, 1)
        for i in range(num_reqs):
            req_id = f"REQ_{2000 + i}"
            open_date = start_date + timedelta(days=random.randint(0, 180))
            req_list.append({
                "req_id": req_id,
                "hiring_manager": f"Manager {random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])}",
                "department": random.choice(self.departments),
                "location": random.choice(self.locations),
                "priority": random.choice(['P0 - Critical', 'P1 - High', 'P2 - Medium']),
                "planned_hires": random.randint(1, 5),
                "requisition_open_date": open_date.strftime('%Y-%m-%d')
            })
        return pd.DataFrame(req_list)

    def generate_pipeline(self, df_reqs, num_candidates=1000):
        candidates = []
        pipeline_records = []
        for i in range(num_candidates):
            candidate_id = f"CAND_{100000 + i}"
            associated_req = df_reqs.sample(1).iloc[0]
            req_id = associated_req['req_id']
            req_open_dt = datetime.strptime(associated_req['requisition_open_date'], '%Y-%m-%d')
            
            source = random.choices(self.sources, weights=[0.40, 0.15, 0.25, 0.10, 0.10], k=1)[0]
            recruiter = random.choice(self.recruiters)
            
            # Anomaly Injection 1: Null Source Tracking
            if random.random() < 0.04:
                source = None
                
            email = f"talent_{i}@simulation-tesla-portfolio.io"
            # Anomaly Injection 2: Duplicate Records
            if random.random() < 0.02 and i > 5:
                email = candidates[random.randint(0, len(candidates)-1)]['email']
                
            candidates.append({
                "candidate_id": candidate_id, 
                "email": email, 
                "associated_req_id": req_id, 
                "assigned_recruiter_id": recruiter['recruiter_id']
            })
            
            current_date = req_open_dt + timedelta(days=random.randint(1, 10))
            max_stage_idx = random.choices([0, 1, 2, 3, 4], weights=[0.45, 0.25, 0.15, 0.10, 0.05], k=1)[0]
            
            # Anomaly Injection 3: Out-of-Sequence Jumps (e.g., skipping straight to an offer)
            skip_sequence = random.random() < 0.03 and max_stage_idx >= 3
            stages = ['Applied', 'Offer Issued'] if skip_sequence else self.stages_sequence[:max_stage_idx + 1]
            
            for stage_name in stages:
                current_date += timedelta(days=random.randint(2, 15))
                if current_date > datetime(2026, 6, 28):
                    break
                pipeline_records.append({
                    "pipeline_event_id": str(uuid.uuid4())[:8],
                    "candidate_id": candidate_id,
                    "req_id": req_id,
                    "source_channel": source,
                    "stage_reached": stage_name,
                    "stage_entry_timestamp": current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "recruiter_id": recruiter['recruiter_id']
                })
                
        return pd.DataFrame(candidates), pd.DataFrame(pipeline_records)

    def execute(self):
        df_reqs = self.generate_requisitions(50)
        df_cand, df_pipe = self.generate_pipeline(df_reqs, 1200)
        df_recruiter = pd.DataFrame(self.recruiters)
        
        df_reqs.to_csv("./data/raw_requisitions.csv", index=False)
        df_cand.to_csv("./data/raw_candidates.csv", index=False)
        df_pipe.to_csv("./data/raw_pipeline_events.csv", index=False)
        df_recruiter.to_csv("./data/raw_recruiters.csv", index=False)
        print(f"[SUCCESS] CSV Datasets Written to ./data/")

if __name__ == "__main__":
    TeslaRecruitingDataGenerator().execute()
