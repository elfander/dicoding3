import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from library import DataAnalyzer
sns.set(style='darkgrid')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_backgroundColor="#0000"
# Dataset



datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
data_keseluruhan = pd.read_csv("../dashboard/proyek_ahir.csv")
data_keseluruhan.sort_values(by="order_approved_at", inplace=True)
data_keseluruhan.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('../dashboard/geolocation.csv')


for col in datetime_cols:
    data_keseluruhan[col] = pd.to_datetime(data_keseluruhan[col])

min_date = data_keseluruhan["order_approved_at"].min()
max_date = data_keseluruhan["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("M.Wahyu Elfander")

    # Logo Image
    st.image("../dashboard/ubuntu.png")

    # Date Range
    start_date, end_date = st.date_input(
        label="",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        disabled=True
    )

# Main
main_df = data_keseluruhan[(data_keseluruhan["order_approved_at"] >= str(start_date)) & 
                 	    (data_keseluruhan["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)


daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

# judul
st.header("Data E-Commerce brazil")


# Produk Apa yang Paling Banyak dan Paling Sedikit Terjual?
#pertanyaan 1
st.subheader("**Produk Apa yang Paling Banyak dan Paling Sedikit Terjual?**")
#pertanyaan 1")
tab1, tab2 = st.tabs(["data produk","Penjelasan"])
#tab1,tab2 = st.tabs(["Negara Bagian", "Penjelasan"])

with tab1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total: **{total_items}**")
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"item rata-rata: **{avg_items}**")

with tab2:
	st.write('dari data  bisa dilihat bahwa yang paling banyak terjual adalah bad_bath_table dan yang paling sedikit terjual adalah auto')


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

colors = ["orange", "white", "white", "white", "red"]

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("penjualan", fontsize=50)
ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)
ax[0].set_facecolor('navy')





colors = ["navy", "#D3D3D3", "#D3D3D3", "white", "red"]
sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Penjualan", fontsize=50)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
ax[1].set_facecolor('orange')


st.pyplot(fig)

# Berapa rating yang diberikan pelanggan? Bisakah kamu tampilkan rating tertinggi hingga terendah? berapa mayoritas rating dari skala 1-5?
#pertanyaan2
st.subheader("**Berapa rating yang diberikan pelanggan? Bisakah kamu tampilkan rating tertinggi hingga terendah? berapa mayoritas rating dari skala 1-5?**")
col1,col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Ulasan Rata-Rata: **{avg_review_score}**")

with col2:
    most_common_review_score = review_score.value_counts().index[0]
    st.markdown(f"Ulasan Terbanyak: **{most_common_review_score}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=review_score.index, 
            y=review_score.values, 
            order=review_score.index,
            palette=["yellow" if score == common_score else "red" for score in review_score.index]
            )

plt.title("Ulasan Pelanggan", fontsize=15)
plt.xlabel("Ulasan")
plt.gca().set_facecolor('navy')
plt.ylabel("Pelanggan")
plt.xticks(fontsize=12)
st.pyplot(fig)

# Customer Demographic
st.subheader("Customer Demographic")
tab3,tab4 = st.tabs(["Negara Bagian", "Penjelasan"])


with tab3:
    most_common_state = state.customer_state.value_counts().index[0]
    st.markdown(f"Most Common State: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state.customer_state.value_counts().index,
                y=state.customer_count.values, 
                data=state,
                palette=["yellow" if score == most_common_state else "white" for score in state.customer_state.value_counts().index]
                    )

    plt.gca().set_facecolor('black')
    plt.title("Pelanggan Berdasarkan negara bagian di brazil", fontsize=15)
    plt.xlabel("Negara Bagian")
    plt.ylabel("jumlah pelanggan")
    plt.xticks(fontsize=12)
    st.pyplot(fig)


with tab4:
        st.write('Pada grafik dapat dilihat bahwa, SP atau sao paulo merupakan user terbanyak. Sao paulo sendiri merupakan negara bagian terbesar. Sehingga e-commerce ini sudah populer.')
        
