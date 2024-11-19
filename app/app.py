import streamlit as st
import scipy.stats as stats
import math

st.set_page_config(
    page_title= "A/B Test Calculator"
)

with open('www/style.css') as css:
    st.markdown(f"<style>{css.read()}<style>", unsafe_allow_html= True)

# App title
st.title("A/B Test Calculator")

# Input Section
st.write("Provide the number of visitors and conversions for both control and test.")

col1, col2 = st.columns(2)
with col1:
    with st.container(border= True, key= 'control'):
        st.subheader("Control")
        visitors_a = st.number_input("Visitors (Control)", min_value=1, value=1000)
        conversions_a = st.number_input("Conversions (Control)", min_value=0, value=100)

with col2:
    with st.container(border= True):
        st.subheader("Test")
        visitors_b = st.number_input("Visitors (Test)", min_value=1, value=1000)
        conversions_b = st.number_input("Conversions (Test)", min_value=0, value=120)

# Calculation
if conversions_a > visitors_a or conversions_b > visitors_b:
    st.error("Conversions cannot exceed the number of visitors.")
else:
    # Conversion rates
    rate_a = conversions_a / visitors_a
    rate_b = conversions_b / visitors_b

    # Absolute difference in conversion rates
    diff = rate_b - rate_a

    # Pooled conversion rate for Z-test
    pooled_rate = (conversions_a + conversions_b) / (visitors_a + visitors_b)
    se = math.sqrt(pooled_rate * (1 - pooled_rate) * (1 / visitors_a + 1 / visitors_b))

    # Z-score and p-value
    if se > 0:
        z_score = diff / se
        #p_value = stats.norm.sf(abs(z_score)) * 2  # two-tailed test
        p_value = stats.norm.sf(z_score)  # one-tailed test
    else:
        z_score = None
        p_value = None

    # Results Section
    with st.container(border= True):
        st.subheader("Results")

        st.write("**Null Hypotesis**: Test <= Control")
        st.write("**Alternative Hypotesis**: Test > Control")
        alpha = st.select_slider("Provide confidence level", options=(0.90, 0.95, 0.99), value= 0.95, )
        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Conversion Rate (Control)", f"{rate_a:.2%}")
        with col2:
            st.metric("Conversion Rate (Test)", f"{rate_b:.2%}")
        with col3:
            st.metric("Difference", f"{diff:.2%}")

        st.markdown("#### Statistical Significance")
        if z_score is not None:
            st.write(f"**Z-score**: {z_score:.2f}")
            st.write(f"**P-value**: {p_value:.4f}")
            if p_value < (1 - alpha):
                st.success("The result is statistically significant. We can reject the null hypothesis.")
            else:
                st.info("The result is not statistically significant. We can't reject the null hypothesis.")
        else:
            st.error("Error in calculating statistical significance.")
