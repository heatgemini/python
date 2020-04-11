# -*- coding: UTF-8 -*-
import plotly.graph_objects as go
import plotly.io as io


# 生成表格图片
def generate_table(table_head, table_list, file_name):
    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=table_head,
            line_color='darkslategray',
            fill_color=headerColor,
            align=['left', 'center'],
            font=dict(color='white', size=13)
        ),
        cells=dict(
            values=table_list,
            line_color='darkslategray',
            # 2-D list of colors for alternating rows
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor] * 5],
            align=['left', 'center'],
            font=dict(color='darkslategray', size=12)
        ))
    ])
    io.write_image(fig, file_name)
    # fig.show()
