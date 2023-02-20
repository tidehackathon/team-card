import pandas as pd

msg_df1 = pd.read_csv('../../data/russian_invasion_of_ukraine.csv')
msg_df2 = pd.read_csv('../../data/Russian_border_Ukraine.csv')
msg_df3 = pd.read_csv('../../data/StandWithUkraine2.csv', sep=';')
msg_df4 = pd.read_csv('../../data/Ukraine_nato2.csv', sep=';')
msg_df5 = pd.read_csv('../../data/Ukraine_border2.csv', sep=';')
msg_df6 = pd.read_csv('../../data/Russian_troops.csv')
msg_df7 = pd.read_csv('../../data/Russia_invade2.csv', encoding='cp1252',sep=';')
msg_df8 = pd.read_csv('../../data/Ukraine_war2.csv',sep=';')

msg_df1 = msg_df1['body'].rename("content")
msg_df2 = msg_df2['content']
msg_df3 = msg_df3['content']
msg_df4 = msg_df4['content']
msg_df5 = msg_df5['content']
msg_df6 = msg_df6['content']
msg_df7 = msg_df7['content']
msg_df8 = msg_df8['content']

msg_df = pd.concat([msg_df1, msg_df2, msg_df3, msg_df4, msg_df5, msg_df6, msg_df7, msg_df8], axis=0, ignore_index=True)
msg_df = msg_df.dropna().reset_index(drop=True)

msg_df.to_csv('../../messages.csv')