import pandas as pd
import numpy as np
from scipy import stats

print("====== INITIATING CORE STATISTICAL EXTRAPOLATION ENGINE ======")

try:
    # Load and combine data assets
    df_pipe = pd.read_csv("./data/raw_pipeline_events.csv")
    df_req = pd.read_csv("./data/raw_requisitions.csv")
    
    # Clean and cast timestamp fields
    df_pipe['stage_entry_timestamp'] = pd.to_datetime(df_pipe['stage_entry_timestamp'])
    df_pipe = df_pipe.sort_values(by=['candidate_id', 'stage_entry_timestamp'])
    
    # Calculate cycle times between hiring stages
    df_pipe['days_in_prior_stage'] = df_pipe.groupby('candidate_id')['stage_entry_timestamp'].diff().dt.days
    df_clean = df_pipe.dropna(subset=['days_in_prior_stage', 'source_channel'])
    
    # Core Analysis 1: One-Way ANOVA Test
    # H0: Onboarding speeds do not differ significantly across channels.
    channels = df_clean['source_channel'].unique()
    channel_groups = [df_clean[df_clean['source_channel'] == c]['days_in_prior_stage'].values for c in channels]
    
    f_stat, p_val_anova = stats.f_oneway(*channel_groups)
    print("\n[ANALYSIS 1 RESULTS: SOURCING SPEED VARIANCE (ANOVA)]")
    print(f"Calculated F-Statistic: {f_stat:.4f}")
    print(f"Calculated P-Value: {p_val_anova:.6f}")
    print(f"Reject Null Hypothesis (H0): {p_val_anova < 0.05}")
    
    # Core Analysis 2: Pearson Correlation Check
    candidate_summary = df_pipe.groupby('candidate_id').agg(
        total_interactions=('stage_reached', 'count'),
        is_hired=('stage_reached', lambda x: 1 if 'Hired' in x.values else 0)
    )
    
    r_coeff, p_val_corr = stats.pearsonr(candidate_summary['total_interactions'], candidate_summary['is_hired'])
    print("\n[ANALYSIS 2 RESULTS: STAGE DEPTH VS. HIRE OUTCOME (PEARSON)]")
    print(f"Pearson Correlation Coefficient (r): {r_coeff:.4f}")
    print(f"Calculated Significance P-Value: {p_val_corr:.6f}")

except Exception as e:
    print(f"[ERROR ENCOUNTERED] Analysis terminated prematurely: {str(e)}")
