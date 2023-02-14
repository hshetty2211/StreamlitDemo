#@st.cache
def fin_data():
    df = pd.read_excel("ExData/Data Manipulation Worksheet.xlsx", sheet_name = "Financing Table Clean", 
                    parse_dates=["DATE"], index_col=[0])
    return df

finDeals = fin_data() 

pick = st.sidebar.radio("Which chart type do you want?",("Bar", "Box & Whisker", "Sunburst", "Tree Map"))

headers = list(df)

if pick[1] == "Bar":
    x_axis = st.sidebar.selectbox("Pick coloumn for X-axis", df[header])
else: 
    st.write("N/A") 
