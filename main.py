import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
df = pd.read_csv('output.csv')

# Ensure 'Start Date' and 'End Date' columns are parsed as datetime objects
df['Start Date'] = pd.to_datetime(df['Start Date'])
df['End Date'] = pd.to_datetime(df['End Date'])

# Split and explode 'Resources' column if it contains lists of resources
df['Resources'] = df['Resources'].str.split(', ')
df = df.explode('Resources').reset_index(drop=True)

# Streamlit app
st.title('Resource Management Dashboard')

# Date range selector
start_date = st.date_input('Start Date', value=df['Start Date'].min().date())
end_date = st.date_input('End Date', value=df['End Date'].max().date())

if start_date > end_date:
    st.error('End date must be after start date.')
else:
    # Filter data based on date range
    filtered_df = df[(df['Start Date'] <= pd.to_datetime(end_date)) &
                     (df['End Date'] >= pd.to_datetime(start_date))].copy()

    # Adjust Start Date and End Date within the selected range
    filtered_df['Start Date'] = filtered_df['Start Date'].apply(lambda x: max(x, pd.to_datetime(start_date)))
    filtered_df['End Date'] = filtered_df['End Date'].apply(lambda x: min(x, pd.to_datetime(end_date)))

    # Show the filtered data
    st.write(f'Busy periods from {start_date} to {end_date}')
    st.dataframe(filtered_df)

    # Resource Selection
    selected_resource = st.selectbox('Select a Resource', options=filtered_df['Resources'].unique())

    # Filter data by selected resource
    resource_filtered_df = filtered_df[filtered_df['Resources'] == selected_resource].copy()

    # Calculate Busy Days per Project
    resource_filtered_df['Duration'] = (resource_filtered_df['End Date'] - resource_filtered_df['Start Date']).dt.days + 1
    busy_days_per_project = resource_filtered_df.groupby('Project Name').agg({
        'Duration': 'sum',
        'Start Date': 'min',
        'End Date': 'max'
    }).reset_index()
    busy_days_per_project.columns = ['Project', 'Busy Days', 'Start Date', 'End Date']

    # Create hover text with date information
    busy_days_per_project['Hover Text'] = busy_days_per_project.apply(
        lambda row: f"Project: {row['Project']}<br>Busy Days: {row['Busy Days']}<br>Start Date: {row['Start Date'].strftime('%Y-%m-%d')}<br>End Date: {row['End Date'].strftime('%Y-%m-%d')}",
        axis=1
    )

    # Show the busy days per project
    st.write(f'Busy Days for Resource: {selected_resource}')
    st.dataframe(busy_days_per_project)

    # Pie Chart: Distribution of Busy Days
    st.subheader(f'Pie Chart of Busy Days for Resource: {selected_resource}')
    fig = px.pie(busy_days_per_project, names='Project', values='Busy Days',
                 title=f'Busy Days Distribution for Resource: {selected_resource}',
                 hover_name='Project', hover_data={'Start Date': True, 'End Date': True, 'Busy Days': True})
    fig.update_traces(textinfo='label+percent', hovertemplate=busy_days_per_project['Hover Text'])
    st.plotly_chart(fig)
    st.subheader(f'Bar Chart of Busy Days for Resource: {selected_resource}')
    fig = px.bar(busy_days_per_project, x='Project', y='Busy Days',
                 title=f'Busy Days Distribution for Resource: {selected_resource}',
                 labels={'Busy Days': 'Number of Busy Days'},
                 text='Busy Days')
    fig.update_layout(showlegend=False)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(yaxis_title='Number of Busy Days',
                      xaxis_title='Project')
    st.plotly_chart(fig)
    st.subheader(f'Gantt Chart of Busy Days for Resource: {selected_resource}')
    fig = px.timeline(resource_filtered_df, x_start="Start Date", x_end="End Date", y="Project Name",
                      title=f'Gantt Chart of Busy Days for Resource: {selected_resource}',
                      labels={"Start Date": "Start Date", "End Date": "End Date", "Project Name": "Project"})
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig)
    st.subheader(f'Interactive Table of Busy Days for Resource: {selected_resource}')
    st.dataframe(busy_days_per_project)
    # Assuming you have a Date column in your data
    heatmap_df = resource_filtered_df.copy()
    heatmap_df['Date'] = heatmap_df.apply(lambda row: pd.date_range(start=row['Start Date'], end=row['End Date']),
                                          axis=1)
    heatmap_df = heatmap_df.explode('Date')
    heatmap_df['Count'] = 1

    # Convert Periods to strings
    heatmap_df['Date'] = heatmap_df['Date'].astype(str)

    st.subheader(f'Heatmap of Busy Days for Resource: {selected_resource}')
    heatmap_pivot = heatmap_df.pivot_table(index=heatmap_df['Date'], columns='Project Name', values='Count',
                                           aggfunc='sum', fill_value=0)
    fig = px.imshow(heatmap_pivot, labels=dict(x="Project", y="Date", color="Busy Days"),
                    title=f'Heatmap of Busy Days for Resource: {selected_resource}')
    st.plotly_chart(fig)

