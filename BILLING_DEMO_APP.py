import streamlit as st


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smart Billing System",
    page_icon="🧾",
    layout="centered"
)


# ==========================================
# BLUE THEME
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #f4f9ff;
}

/* Main heading */
.main-title {
    text-align: center;
    color: #0d47a1;
    font-size: 40px;
    font-weight: 700;
}

.subtitle {
    text-align: center;
    color: #607d8b;
    font-size: 16px;
    margin-bottom: 30px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    height: 42px;
    background-color: #1976d2;
    color: white;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #0d47a1;
    color: white;
}

/* Total box */
.total-box {
    background-color: #1565c0;
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin-top: 20px;
}

.total-label {
    font-size: 16px;
}

.total-value {
    font-size: 32px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# PRICE CALCULATOR
# ==========================================

def price_calculator(item_price, item_quantity, offer_per):

    final_price = (
        item_price * item_quantity
    ) * (1 - offer_per / 100)

    return final_price


# ==========================================
# SESSION STATE
# ==========================================

if "bill_items" not in st.session_state:
    st.session_state.bill_items = []


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🧾 Smart Billing System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Simple and easy billing calculator'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# ADD ITEM
# ==========================================

st.subheader("🛍️ Add Item")


# Item Name
item_name = st.text_input(
    "Item Name",
    placeholder="Enter item name"
)


# Price and Quantity
col1, col2 = st.columns(2)

with col1:

    item_price = st.number_input(
        "Price (₹)",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

with col2:

    item_quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1,
        step=1
    )


# Discount
offer_per = st.number_input(
    "Discount (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0
)


# ==========================================
# ADD ITEM BUTTON
# ==========================================

if st.button("➕ Add Item"):

    if item_name.strip() == "":
        st.warning("Please enter the item name.")

    elif item_price <= 0:
        st.warning("Please enter a valid price.")

    else:

        # Calculate final price
        final_price = price_calculator(
            item_price,
            item_quantity,
            offer_per
        )

        # Add item to list
        st.session_state.bill_items.append({
            "Item": item_name,
            "Price": item_price,
            "Quantity": item_quantity,
            "Discount": offer_per,
            "Final Amount": final_price
        })

        st.success(
            f"{item_name} added successfully!"
        )


# ==========================================
# CURRENT BILL
# ==========================================

if st.session_state.bill_items:

    st.subheader("🛒 Current Bill")


    # --------------------------------------
    # Display Items
    # --------------------------------------

    for i, item in enumerate(
        st.session_state.bill_items
    ):

        col1, col2, col3, col4, col5 = st.columns(
            [2, 1.3, 1, 1.2, 1]
        )

        with col1:
            st.write(f"**{i + 1}. {item['Item']}**")

        with col2:
            st.write(
                f"₹{item['Price']:.2f}"
            )

        with col3:
            st.write(
                item["Quantity"]
            )

        with col4:
            st.write(
                f"{item['Discount']:.0f}%"
            )

        with col5:

            st.write(
                f"₹{item['Final Amount']:.2f}"
            )


        # Remove button
        if st.button(
            f"❌ Remove {i + 1}",
            key=f"remove_{i}"
        ):

            st.session_state.bill_items.pop(i)

            st.rerun()


        st.divider()


    # ======================================
    # TOTAL BILL CALCULATION
    # ======================================

    bill_amount = sum(
        item["Final Amount"]
        for item in st.session_state.bill_items
    )


    # ======================================
    # TOTAL BILL DISPLAY
    # ======================================

    st.markdown(
        f"""
        <div class="total-box">

            <div class="total-label">
                💰 Bill Amount Till Now
            </div>

            <div class="total-value">
                ₹{bill_amount:,.2f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ======================================
    # FINISH / NEW BILL
    # ======================================

    st.write("")

    col1, col2 = st.columns(2)


    with col1:

        if st.button("✅ Finish Bill"):

            st.success(
                f"🎉 Final Bill Amount: "
                f"₹{bill_amount:,.2f}"
            )


    with col2:

        if st.button("🔄 New Bill"):

            st.session_state.bill_items = []

            st.rerun()


# ==========================================
# EMPTY BILL
# ==========================================

else:

    st.info(
        "Enter item details above and click "
        "**Add Item** to start billing."
    )