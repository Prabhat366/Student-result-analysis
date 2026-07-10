import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt#install plotly
import plotly.express as px
from streamlit_option_menu import option_menu

st.header("Student Result Analysis")
st.write("Welcome to app")
with st.sidebar:
    selected=option_menu(
        menu_title="📌Menu",
        options=["Raw Data", "Student Result", "Topper", "Search Student", "Subject Analysis"],
        icons=["table", "bar-chart", "trophy", "search", "book"],
        menu_icon="menubutton-wide",
        default_index=0
    )
df=pd.read_csv(r"C:\Users\prabh\OneDrive\Documents\StreamlitProjets\data\student_data.csv")
if(selected=="Raw Data"):
    st.subheader("📑Raw Data")
    st.dataframe(df)
elif(selected=="Student Result"):
    st.subheader("📈Student performance Summary")
    
    total_marks=df.groupby("Name")['Marks'].sum()
    avg_marks=df.groupby("Name")['Marks'].mean()

    result=pd.DataFrame({"Total marks":total_marks,"Average Marks":avg_marks}).reset_index()
    st.dataframe(result)

    fig=px.bar(result,x="Name",y="Total marks",color="Total marks",title="Total Marks of the students")
    st.plotly_chart(fig)
    
    #Stacked bar chart 
    st.subheader("Subject wise marks of students")
    pivot_df=df.pivot_table(index="Name",columns="Subject",values="Marks",aggfunc="sum").reset_index()
    
    fig,ax=plt.subplots(figsize=(8,5))
    pivot_df.plot(x="Name",kind="bar",stacked=True,ax=ax)
    
    ax.set_title("Student Marks by subject")
    ax.set_xlabel("Student Name")
    ax.set_ylabel("Total Marks")
    st.pyplot(fig)
    
elif(selected=="Topper"):
    total=df.groupby("Name")['Marks'].sum().sort_values(ascending=False)
    num=st.number_input("Enter how many toppers you want to see",min_value=1,max_value=len(total),value=3)
    st.subheader(f"🏆Top {num} Students")
    st.dataframe(total.head(num))
    
    #line chart for Topper
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot(total.index,total.values,marker="o")
    ax.set_title(f"Top {num} Students")
    ax.set_xlabel("Student Name")
    ax.set_ylabel("Total Marks")
    st.pyplot(fig)
    
elif(selected=="Search Student"):
    st.subheader("🔍Search Student")
    name=st.text_input("Enter student name")
    if name:
        filtered_df=df[df['Name'].str.contains(name,case=False)]
        
        if not filtered_df.empty:
            st.success(f"Showing results for {name}")
            st.dataframe(filtered_df)

            total_marks=filtered_df.groupby("Name")['Marks'].sum()
            average_marks=filtered_df.groupby("Name")['Marks'].mean()
            st.write(f"Total Marks: {total_marks.values[0]}")
            st.write(f"Average Marks: {average_marks.values[0]}")
                            
            fig=px.bar(filtered_df,x="Subject",y="Marks",color="Marks",title=f"{name}'s Marks by Subject")
            st.plotly_chart(fig)
        else:
            st.warning("No student found with that name.")
            