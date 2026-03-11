import streamlit as st
import pandas as pd

# Define data based on NCCN Antiemesis v2.2025
emetogenic_data = {
"High Risk (>90% frequency)": [
        "AC combination", "Carboplatin AUC >= 4", "Carmustine > 250 mg/m2", "Cisplatin",
        "Cyclophosphamide > 1500 mg/m2", "Dacarbazine", "Datopotamab deruxtecan-dink",
        "Doxorubicin >= 60 mg/m2", "Epirubicin > 90 mg/m2", "Fam-trastuzumab deruxtecan-nxki",
        "Ifosfamide >= 2 g/m2", "Mechlorethamine", "Melphalan >= 140 mg/m2",
        "Sacituzumab govitecan-hziy", "Streptozocin", "Zolbetuximab-clzb", # 修正拼字
        "Aldesleukin > 12-15 million IU/m2", "Daunorubicin", "Lurbinectedin" # 補上
    ],
    "Moderate Risk (30%-90% frequency)": [
        "Amifostine > 300 mg/m2", "Bendamustine", "Busulfan",
        "Carboplatin AUC < 4", "Carmustine <= 250 mg/m2", "Clofarabine", 
        "Cyclophosphamide <= 1500 mg/m2", "Cytarabine > 200 mg/m2", "Dactinomycin", 
        "Dinutuximab", "Doxorubicin < 60 mg/m2", "Melphalan < 140 mg/m2",
        "Dual-drug liposomal encapsulation of cytarabine and daunorubicin", # 補上
        "Epirubicin <= 90 mg/m2", "Idarubicin", "Ifosfamide < 2 g/m2 per dose", # 補上
        "Methotrexate >= 250 mg/m2", "Mirvetuximab soravtansine-gynx", # 補上
        "Naxitamab-gqgk", "Oxaliplatin", "Romidepsin", "Temozolomide", "Trabectedin" # 補上
    ],
    "Low Risk (10%-30% frequency)": [
        "Ado-trastuzumab emtansine", "Arsenic trioxide", "Azacitidine", "Belinostat",
        "Brentuximab vedotin", "Cytarabine (100-200 mg/m2)", "Docetaxel", "Doxorubicin (liposomal)",
        "Elranatamab-bcmm", "Eribulin", "Etoposide", "5-Fluorouracil (5-FU)", "Ixabepilone",
        "Methotrexate (50-250 mg/m2)", "Mitomycin", "Mitoxantrone", "Paclitaxel", "Pemetrexed", "Topotecan"
    ],
    "Minimal Risk (<10% frequency)": [
        "Alemtuzumab", "Asparaginase", "Bevacizumab", "Bleomycin", "Bortezomib", "Cetuximab",
        "Cytarabine < 100 mg/m2", "Daratumumab", "Fludarabine", "Gemcitabine", "Methotrexate <= 50 mg/m2",
        "Nivolumab", "Pembrolizumab", "Rituximab", "Trastuzumab", "Vinblastine", "Vincristine", "Vinorelbine"
    ]
}

# Create a flattened dictionary for easier lookup
drug_db = {}
for risk_level, drugs in emetogenic_data.items():
    for drug in drugs:
        drug_db[drug] = risk_level

# Define dose-dependent drugs mapping base drug -> specific variants
dose_dependent_drugs = {
    "Carboplatin": ["Carboplatin AUC >= 4", "Carboplatin AUC < 4"],
    "Carmustine": ["Carmustine > 250 mg/m2", "Carmustine <= 250 mg/m2"],
    "Cyclophosphamide": ["Cyclophosphamide > 1500 mg/m2", "Cyclophosphamide <= 1500 mg/m2"],
    "Cytarabine": ["Cytarabine > 200 mg/m2", "Cytarabine (100-200 mg/m2)", "Cytarabine < 100 mg/m2"],
    "Doxorubicin": ["Doxorubicin >= 60 mg/m2", "Doxorubicin < 60 mg/m2"],
    "Epirubicin": ["Epirubicin > 90 mg/m2", "Epirubicin <= 90 mg/m2"],
    "Ifosfamide": ["Ifosfamide >= 2 g/m2", "Ifosfamide < 2 g/m2 per dose"],
    "Melphalan": ["Melphalan >= 140 mg/m2", "Melphalan < 140 mg/m2"],
    "Methotrexate": ["Methotrexate >= 250 mg/m2", "Methotrexate (50-250 mg/m2)", "Methotrexate <= 50 mg/m2"],
}

# Collect all standalone drugs and base names of dose-dependent drugs for the selectbox
all_dependent_variants = set([variant for variants in dose_dependent_drugs.values() for variant in variants])
standalone_drugs = [drug for drug in drug_db.keys() if drug not in all_dependent_variants]
selectbox_options = sorted(standalone_drugs + list(dose_dependent_drugs.keys()), key=str.casefold)

def generate_clinical_note(drug, risk, option_text=None, delayed_text=None):
    note = f"Chemotherapy Regimen/Drug: {drug}\n"
    note += f"NCCN Emetogenic Potential: {risk}\n"
    if option_text:
        note += f"\n[Anti-emetic Prevention Plan (NCCN v2.2025)]\n"
        note += f"Day 1: {option_text}\n"
        if delayed_text:
            note += f"Days 2+: {delayed_text}\n"
    return note

def display_high_risk_options(drug_name, risk):
    st.error("### 💊 急性與延遲性止吐預防處方 (High Emetic Risk)")
    st.markdown("**Day 1 Treatment Options (Category 1)**")
    
    options = {
        "Option A (Preferred)": "Olanzapine (2.5-10 mg) + NK1 RA + 5-HT3 RA + Dexamethasone (12 mg)",
        "Option B": "Olanzapine (2.5-10 mg) + Palonosetron + Dexamethasone (12 mg)",
        "Option C": "NK1 RA + 5-HT3 RA + Dexamethasone (12 mg)"
    }
    
    selected_option = st.radio("選擇 Day 1 處方：", list(options.keys()))
    delayed_plan = "接續使用對應的延遲性止吐藥物 (如 Olanzapine 或 Aprepitant + Dexamethasone)"
    st.info(f"📌 **提醒：** Days 2, 3, 4 {delayed_plan}。")
    
    st.markdown("---")
    st.subheader("📝 複製病歷紀錄 (Clinical Note)")
    note = generate_clinical_note(drug_name, risk, options[selected_option], delayed_plan)
    st.text_area("可直接複製貼上至 HIS 系統：", value=note, height=150)

def display_moderate_risk_options(drug_name, risk):
    st.warning("### 💊 急性與延遲性止吐預防處方 (Moderate Emetic Risk)")
    st.markdown("**Day 1 Treatment Options (Category 1)**")
    
    options = {
        "Option D": "5-HT3 RA + Dexamethasone (12 mg)",
        "Option E": "Olanzapine (2.5-10 mg) + Palonosetron + Dexamethasone (12 mg)",
        "Option F": "NK1 RA + 5-HT3 RA + Dexamethasone (12 mg)"
    }
    
    selected_option = st.radio("選擇 Day 1 處方：", list(options.keys()))
    delayed_plan = "視情況繼續給予 Dexamethasone, 5-HT3 RA 或 Olanzapine/Aprepitant"
    st.info(f"📌 **提醒：** Days 2, 3 {delayed_plan}。")
    
    st.markdown("---")
    st.subheader("📝 複製病歷紀錄 (Clinical Note)")
    note = generate_clinical_note(drug_name, risk, options[selected_option], delayed_plan)
    st.text_area("可直接複製貼上至 HIS 系統：", value=note, height=150)

def display_low_risk_options(drug_name, risk):
    st.info("### 💊 急性與延遲性止吐預防處方 (Low Emetic Risk)")
    st.markdown("建議單獨使用 Dexamethasone, 5-HT3 RA 等藥物")
    
    st.markdown("---")
    st.subheader("📝 複製病歷紀錄 (Clinical Note)")
    note = generate_clinical_note(drug_name, risk)
    st.text_area("可直接複製貼上至 HIS 系統：", value=note, height=100)

def display_minimal_risk_options(drug_name, risk):
    st.success("### 💊 急性與延遲性止吐預防處方 (Minimal Emetic Risk)")
    st.markdown("常規不需給予預防性止吐藥物")
    
    st.markdown("---")
    st.subheader("📝 複製病歷紀錄 (Clinical Note)")
    note = generate_clinical_note(drug_name, risk)
    st.text_area("可直接複製貼上至 HIS 系統：", value=note, height=100)

def setup_page():
    st.set_page_config(
        page_title="NCCN Emetogenic Potential App",
        page_icon="💊",
        layout="centered"
    )

def main():
    setup_page()
    
    st.title("NCCN 化療藥物致吐性風險查詢系統")
    st.markdown("**(依據 NCCN Antiemesis v2.2025)**")
    
    # Streamlit 的 selectbox 預設即支援模糊搜尋 (fuzzy search)
    st.subheader("請選擇化療藥物")
    
    selected_base_drug = st.selectbox(
        "輸入或選擇藥物名稱 (支援拼字搜尋)：",
        options=[""] + selectbox_options,
        index=0,
        format_func=lambda x: "請選擇..." if x == "" else x
    )
    
    # 顯示結果
    if selected_base_drug:
        # 處理劑量相依藥物的 Radio Button 邏輯
        if selected_base_drug in dose_dependent_drugs:
            final_drug_name = st.radio(
                f"請選擇 {selected_base_drug} 的具體劑量/條件：",
                options=dose_dependent_drugs[selected_base_drug]
            )
        else:
            final_drug_name = selected_base_drug

        if final_drug_name:
            risk = drug_db[final_drug_name]
            
            # 使用 Streamlit 內建警示框顯示致吐性風險
            if "High" in risk:
                st.error(f"### 致吐性風險：{risk}")
            elif "Moderate" in risk:
                st.warning(f"### 致吐性風險：{risk}")
            elif "Low" in risk:
                st.info(f"### 致吐性風險：{risk}")
            else:
                st.success(f"### 致吐性風險：{risk}")
                
            st.markdown(f"**藥物名稱：** {final_drug_name}")
            
            # 根據 Risk Level 顯示 Treatment Options 及 Clinical Note
            if "High Emetic Risk" in risk or "High Risk" in risk:
                display_high_risk_options(final_drug_name, risk)
            elif "Moderate Emetic Risk" in risk or "Moderate Risk" in risk:
                display_moderate_risk_options(final_drug_name, risk)
            elif "Low Emetic Risk" in risk or "Low Risk" in risk:
                display_low_risk_options(final_drug_name, risk)
            else:
                display_minimal_risk_options(final_drug_name, risk)

    st.markdown("---")
    st.caption("免責聲明：本系統僅供醫療人員參考，不應取代臨床專業判斷。開發者不對使用本系統所產生的任何醫療決定負責。")

if __name__ == "__main__":
    main()
