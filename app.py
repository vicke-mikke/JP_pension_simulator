# Calculate the Japanese pension benefit per monthly contribution
import plotly.express as px
import pandas as pd
import streamlit as st

def calculate_annual_withdrawal(capital, annual_return_rate, years):
    """
    Calculate the annual withdrawal amount from the capital.
    
    Parameters:
        capital (float): The initial capital amount.
        annual_return_rate (float): The annual capital return rate in percentage.
        years (int): The number of years to use all the capital.
        
    Returns:
        float: The annual withdrawal amount.
    """
    # Convert the annual return rate to a decimal
    r = annual_return_rate / 100
    
    # Calculate the annuity payment using the formula
    annuity_payment = capital / ((1 - (1 + r) ** -years) / r)
    
    return annuity_payment


def main():
    #  parameters
    st.title('Japanese Pension Calculator')
    st.write('This calculator is to estimate the annual withdrawal amount from a monthly contribution to the Japanese pension system if invested')
    monthly_contribution=st.number_input('Monthly contribution (Yen)', value=16520, step=10)
    current_pension_benefit=st.number_input('Current pension benefit (Yen)', value=795000, step=1000)
    life_after_retirement=st.number_input('Life after retirement (Years)', value=40, step=1)
    current_age=st.number_input('Current age (Years)', value=40, step=1)
    retirement_age=st.number_input('Retirement age (Years)', value=65, step=1)
    average_real_return=st.number_input('Average real return (%)', value=4.0, step=0.1)

    # Calculate the pension benefit after retirement
    pension_value_increase_from_monthly_contribution=current_pension_benefit/12/40

    # Calculate the money value at retirement if invested
    capital_at_retirement_if_invested=monthly_contribution * (1 + average_real_return/100) ** (retirement_age - current_age)
    annual_withdrawal = calculate_annual_withdrawal(capital_at_retirement_if_invested, 
                                                    average_real_return, 
                                                    life_after_retirement)
    st.markdown(f"""# Results
A month contribution increases the annual pension by **{pension_value_increase_from_monthly_contribution:.2f} yen** \n
If invested, you can withdraw **{annual_withdrawal:.2f} yen** annually for {life_after_retirement} years after retirement 
""")

    # Calculate the money value at retirement if invested
    ages=[]
    annual_withdrawals=[]
    for current_age in range(20, retirement_age, 1):
        capital_at_retirement_if_invested=monthly_contribution * (1 + average_real_return/100) ** (retirement_age - current_age)
        annual_withdrawal = calculate_annual_withdrawal(capital_at_retirement_if_invested, 
                                                        average_real_return, 
                                                        life_after_retirement)
        ages.append(current_age)
        annual_withdrawals.append(annual_withdrawal)
    df=pd.DataFrame({'Age':ages, 'Annual Withdrawal':annual_withdrawals})

    st.markdown('# Simulation at different ages')
    fig = px.bar(df, x="Age", y="Annual Withdrawal", 
                title=f'Potential annual withdrawal from a month contribution if invested: Inflation adjusted return = {average_real_return} %')
    fig.add_hline(y=pension_value_increase_from_monthly_contribution, line_dash="dot", annotation_text="Pension value increase from a month contribution", annotation_position="top right")
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)



# git add app.py;git commit -m "debug";git push -u origin main


if __name__ == '__main__':
    main()