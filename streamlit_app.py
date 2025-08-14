import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tipping Disbursement Tool", layout="wide")
st.title("💰 Tipping Disbursement Tool")

st.markdown("Choose a method to calculate tips distribution:")
method = st.selectbox(
    "Calculation Method",
    ["Weighted by Hours", "Weighted by Role", "Weighted by Hours & Role"]
)

# Weighted by Hours
if method == "Weighted by Hours":
    st.subheader("Weighted by Hours")
    tip_total = st.number_input("Total Tips ($)", min_value=0.0, value=1000.0)
    data = st.data_editor(
        pd.DataFrame({
            "Employee": pd.Series(dtype="str"),
            "Hours Worked": pd.Series(dtype="float")
        }),
        num_rows="dynamic",
        key="hours_data"
    )
    if st.button("Calculate"):
        if not data.empty and "Hours Worked" in data.columns:
            total_hours = data["Hours Worked"].sum()
            if total_hours > 0:
                data["Tips Earned"] = data["Hours Worked"] / total_hours * tip_total
                st.dataframe(data)
            else:
                st.error("Total hours must be greater than 0.")
        else:
            st.error("Please enter employee names and hours worked.")

# Weighted by Role
elif method == "Weighted by Role":
    st.subheader("Weighted by Role")
    tip_total = st.number_input("Total Tips ($)", min_value=0.0, value=1000.0)
    data = st.data_editor(
        pd.DataFrame({
            "Role": pd.Series(dtype="str"),
            "Percent Weight": pd.Series(dtype="float"),
            "Employee Count": pd.Series(dtype="float")
        }),
        num_rows="dynamic",
        key="role_data"
    )
    if st.button("Calculate"):
        if not data.empty and "Percent Weight" in data.columns:
            total_weight = data["Percent Weight"].sum()
            if total_weight > 0:
                data["Tip Share"] = data["Percent Weight"] / total_weight * tip_total
                data["Tips per Employee"] = data["Tip Share"] / data["Employee Count"]
                st.dataframe(data)
            else:
                st.error("Total weight must be greater than 0.")
        else:
            st.error("Please enter role details.")

# Weighted by Hours & Role
elif method == "Weighted by Hours & Role":
    st.subheader("Weighted by Hours & Role")
    tip_total = st.number_input("Total Tips ($)", min_value=0.0, value=1000.0)
    role_weights = st.data_editor(
        pd.DataFrame({
            "Role": pd.Series(dtype="str"),
            "Weight": pd.Series(dtype="float")
        }),
        num_rows="dynamic",
        key="role_weights"
    )
    employee_data = st.data_editor(
        pd.DataFrame({
            "Employee": pd.Series(dtype="str"),
            "Hours Worked": pd.Series(dtype="float"),
            "Role": pd.Series(dtype="str")
        }),
        num_rows="dynamic",
        key="hours_role_data"
    )
    if st.button("Calculate"):
        if not employee_data.empty and not role_weights.empty:
            merged = employee_data.merge(role_weights, on="Role", how="left")
            merged["Weighted Hours"] = merged["Hours Worked"] * merged["Weight"]
            total_weighted_hours = merged["Weighted Hours"].sum()
            if total_weighted_hours > 0:
                merged["Tips Earned"] = merged["Weighted Hours"] / total_weighted_hours * tip_total
                st.dataframe(merged)
            else:
                st.error("Total weighted hours must be greater than 0.")
        else:
            st.error("Please fill in both role weights and employee data.")