import pandas as pd

art_df1 = pd.read_csv('../../data/NYT_Russia_Ukraine.csv')
art_df2 = pd.read_csv('../../data/Guardians_Russia_Ukraine.csv')

art_df1 = art_df1[['articles']]
art_df2 = art_df2[['articles']]

art_df = pd.concat([art_df1, art_df2], axis=0, ignore_index=True)

# art_df.to_csv('../../articles.csv')