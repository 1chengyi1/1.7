import streamlit as st
import pandas as pd
import plotly.express as px

# 设置页面标题
st.title("科研人员信用风险预警查询")

# 读取Excel文件
df_paper = pd.read_excel('data2.xlsx', sheet_name='论文')
df_project = pd.read_excel('data2.xlsx', sheet_name='项目')
df_risk = pd.read_excel('data2.xlsx', sheet_name='风险值')

query_name = st.text_input("请输入查询名字：")

# 定义闪烁效果的 CSS
blink_css = """
<style>
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
.blink {
    animation: blink 1s infinite;
    color: red;
    font-weight: bold;
}

/* 表格样式优化 */
.dataframe {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.dataframe th, .dataframe td {
    padding: 8px;
    text-align: left;
    border: 1px solid #ddd;
    max-width: 300px; /* 限制列宽 */
    white-space: normal; /* 允许换行 */
    word-wrap: break-word; /* 允许单词内换行 */
}
.dataframe th {
    background-color: #f2f2f2;
    font-weight: bold;
}

/* 添加滚动条 */
.dataframe-wrapper {
    max-height: 400px; /* 设置最大高度 */
    overflow-y: auto; /* 添加垂直滚动条 */
    margin-bottom: 20px;
}
</style>
"""

# 添加闪烁效果的 CSS
st.markdown(blink_css, unsafe_allow_html=True)

if query_name:
    # 在论文表中寻找姓名等于查询输入的名字
    result_paper = df_paper[df_paper['姓名'] == query_name]
    # 在项目表中寻找姓名等于查询输入的名字
    result_project = df_project[df_project['姓名'] == query_name]
    # 在风险值表中寻找作者等于查询输入的名字
    result_risk = df_risk[df_risk['作者'] == query_name]

    # 生成论文查询结果表格
    if not result_paper.empty:
        st.markdown("### 论文查询结果")
        # 将表格转换为 HTML，并添加滚动条
        html_table1 = result_paper.to_html(index=False, escape=False, classes='dataframe')
        st.markdown(f"<div class='dataframe-wrapper'>{html_table1}</div>", unsafe_allow_html=True)
    
    # 生成项目查询结果表格
    if not result_project.empty:
        st.markdown("### 项目查询结果")
        # 将表格转换为 HTML，并添加滚动条
        html_table2 = result_project.to_html(index=False, escape=False, classes='dataframe')
        st.markdown(f"<div class='dataframe-wrapper'>{html_table2}</div>", unsafe_allow_html=True)

    # 生成风险值查询结果
    if not result_risk.empty:
        st.markdown("### 风险值查询结果")
        risk_value = result_risk.iloc[0]['风险值']
        
        # 根据风险值显示不同的提示信息
        if risk_value > 2.5:
            st.markdown(f"<p class='blink'>作者: {result_risk.iloc[0]['作者']}, 风险值: {risk_value}（高风险）</p>", unsafe_allow_html=True)
        else:
            st.write(f"作者: {result_risk.iloc[0]['作者']}, 风险值: {risk_value}（低风险）")
    else:
        st.write("暂时没有相关记录。")
