import mpld3 as mpld3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import numpy as np
from itertools import groupby
import wrapit as wrapit
import streamlit.components.v1 as components

# file_loc = "/Users/nidaaziz/python/SKP_survey.xlsx"
file_loc = "/SKPSurvey/SKP_survey.xlsx"

df_channeluse = pd.read_excel(file_loc, sheet_name="Cleaned qualified responses", usecols = "AR:BF", skiprows=[0], )

pd.set_option('display.max_columns', None)
print(df_channeluse)
plt.rcParams.update({'font.size': 25})
plt.rcParams['figure.constrained_layout.use'] = True

# st.title()
st.markdown('<div style="text-align: center; font-size: 30px; font-weight: bold;">Submitting a planning application</div>', unsafe_allow_html=True)
st.title("")
# Add a sidebar
st.sidebar.title('Filters')
category = st.sidebar.selectbox('Category', options=['All', 'Category A', 'Category B'])

colors = ["purple", "blue", "teal", "silver", "darkorange","darkolivegreen"]
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(25, 25), tight_layout = True)

# process data

title_font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'}

# Create a chart
if category == 'All':
    # Channel of application submission
    channel = [df_channeluse['ChannelsUse1r1'].sum(), df_channeluse['ChannelsUse1r2'].sum(),
               df_channeluse['ChannelsUse1r3'].sum(), df_channeluse['ChannelsUse1r4'].sum()]
    options = ['Planning Portal', 'E-mail', 'Post', 'In person']
    bars = axs[0, 0].bar(options, channel, color=colors)
    # Add data labels to the chart
    for bar in bars:
        height = bar.get_height()
        axs[0, 0].annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    axs[0, 0].set_xlabel('Channels')
    axs[0, 0].set_ylabel('Total Responses')
    axs[0, 0].set_title('How do you typically submit your planning applications?', pad=30)
    axs[0, 0].spines['top'].set_color('none')
    axs[0, 0].spines['right'].set_color('none')
    axs[0, 0].spines['left'].set_color('none')
    axs[0, 0].spines['bottom'].set_color('none')
    for i, bar in enumerate(bars.get_children()):
        tooltip = mpld3.plugins.LineLabelTooltip(bar, label=str(i))
        mpld3.plugins.connect(plt.gcf(), tooltip)
    fig.tight_layout(pad=25.0)
    # mpld3.plugins.connect(fig, tooltip)



    # # Reasons for not using the PP
    # axs[1,0].text(0.5, 0.6, "All participants use the Planning Portal \n for their planing applications", horizontalalignment='center',
    #  verticalalignment='center', fontsize=16, color= colors[1])
    # axs[1, 0].spines['bottom'].set_color('none')
    # axs[1, 0].spines['top'].set_color('none')
    # axs[1, 0].spines['left'].set_color('none')
    # axs[1, 0].spines['right'].set_color('none')
    # axs[1, 0].set_xticks([])
    # axs[1, 0].set_yticks([])
    # axs[1, 0].set_xticklabels([])
    # axs[1, 0].set_yticklabels([])

    # Ever used manual submission
    manual = df_channeluse['ManualExperience3'].dropna()
    counts = manual.value_counts()
    manual_labels = ["Yes", "No", "Don't know"]
    print(counts)
    # manual_pie = axs[2,0].pie(counts, autopct='%1.1f%%')
    myexplode = [0.1, 0, 0]
    patches, texts, pcts = axs[0, 1].pie(
        counts, colors=colors, autopct='%.1f%%', pctdistance=1.2, startangle=0,
        textprops={'fontsize': 20}, explode=myexplode)

    axs[0, 1].legend(manual_labels)
    # plt.setp(pcts, color='white', fontweight='bold', fontsize=10)
    axs[0, 1].set_title(" Have you ever made a manual (non-PP) submission?", pad=30)
    fig.tight_layout(pad=25.0)

    # Why not PP for all applications
    other_channels = [df_channeluse['ManualUseReasons4r1'].sum(), df_channeluse['ManualUseReasons4r2'].sum(),
                      df_channeluse['ManualUseReasons4r3'].sum(), df_channeluse['ManualUseReasons4r4'].sum(),
                      df_channeluse['ManualUseReasons4r5'].sum()]
    channel_options = ['Application type not supported', 'Too expensive sometimes', 'Some clients prefer manual apps', 'I prefer manual app', 'Other reasons']
    channel_options = wrapit.wrapit(channel_options)
    print(other_channels)
    channel_bars = axs[1, 0].bar(channel_options, other_channels, color=colors)
    # Add data labels to the chart
    for bar in channel_bars:
        height = bar.get_height()
        axs[1, 0].annotate('{}'.format(height),
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom')
    axs[1, 0].set_xlabel('Reasons')
    axs[1, 0].set_ylabel('Total Responses')
    axs[1, 0].set_title('Why don’t you use the Planning Portal to submit all of your applications?', pad=30)
    axs[1, 0].spines['top'].set_color('none')
    axs[1, 0].spines['right'].set_color('none')
    axs[1, 0].spines['left'].set_color('none')


    # Submission charge for other channels
    manualuse = df_channeluse['ManualUseQuant5']#.dropna()
    manualuse_counts = manualuse.value_counts()
    manualuse_counts = manualuse_counts.reindex([1, 2, 3], fill_value=0)
    print(manualuse_counts)
    manualuse_bars = axs[2, 1].bar( manual_labels, manualuse_counts, color=colors)
    for bar in manualuse_bars:
        height = bar.get_height()
        axs[2, 1].annotate('{}'.format(height),
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom')
    # axs[1, 1].set_xlabel('Reasons')
    axs[2, 1].set_ylabel('Total Responses')
    axs[2, 1].set_title('Submission charge for other channels', pad=30)
    axs[2, 1].spines['top'].set_color('none')
    axs[2, 1].spines['right'].set_color('none')
    axs[2, 1].spines['left'].set_color('none')
    axs[2, 1].autoscale()
    fig.tight_layout(pad=25.0)
# else:
#     filtered_data = df_channeluse[df_channeluse['category'] == category]
#     fig, axs = plt.subplots()
#     filtered_data.plot(kind='bar', x='x', y='y', ax=ax)


# Image
    im = plt.imread('/Users/nidaaziz/python/man_sub.png')
    axs[1,1].imshow(im)
    axs[1,1].axis('off')
# axs[0,1].plot(x, y2)
# axs[1,0].plot(x, y3)
# axs[1,1].plot(x, y4)
# axs[2,0].plot(x, y5)
# axs[2,1].plot(x, y6)


# # Add the chart to the dashboard
st.pyplot(fig)
mpld3.display()

# "Submission through Planning portal incurs extra fee"
# "Needs to be done via credit card"
# "Duplication for assurety"
# "Manual applications can be amended"
# "Some document cannot be submitted via PP and need to be emailed"
