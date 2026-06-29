import pandas as pd
import sys

class AutomatedDataQualityEngine:
    def __init__(self, pipeline_path, req_path):
        self.df_pipe = pd.read_csv(pipeline_path)
        self.df_req = pd.read_csv(req_path)

    def execute_suite(self):
        print("====== STARTING PROJECT HELIOS TEST INTEGRITY MATRIX ======")
        
        # Test 1: Null Key Constraints
        null_keys = self.df_pipe['pipeline_event_id'].isnull().sum()
        t1_status = "PASSED" if null_keys == 0 else "FAILED"
        print(f"TEST 1: Null Primary Key Check: {t1_status} ({null_keys} null keys detected)")
        
        # Test 2: Source Tracking Completeness
        missing_sources = self.df_pipe['source_channel'].isnull().sum()
        pct_missing = (missing_sources / len(self.df_pipe)) * 100
        t2_status = "PASSED" if pct_missing < 5.0 else "WARNING_ALERT"
        print(f"TEST 2: Sourcing Field Completeness Check: {t2_status} ({pct_missing:.2f}% missing entries)")
        
        # Test 3: Relational Reference Integrity Checks
        invalid_refs = ~self.df_pipe['req_id'].isin(self.df_req['req_id'])
        invalid_count = invalid_refs.sum()
        t3_status = "PASSED" if invalid_count == 0 else "REJECT_DEPLOYMENT"
        print(f"TEST 3: Relational Reference Integrity Check: {t3_status} ({invalid_count} unmapped keys found)")
        
        global_health = 100.0 - pct_missing
        print(f"====== GLOBAL PIPELINE HEALTH CAPACITY: {global_health:.2f}% ======")
        
        if t3_status == "REJECT_DEPLOYMENT":
            sys.exit(1)
        print("[SUCCESS] Operational testing phases complete.")

if __name__ == "__main__":
    AutomatedDataQualityEngine("./data/raw_pipeline_events.csv", "./data/raw_requisitions.csv").execute_suite()
