# read O/D/Mode xlsx file, split sheets to dataframe, melt matrixes, push to DB

import pandas as pd 

file = 'Data/cleaned_jtw_by_mode_by_borough.xlsx'

xls = pd.ExcelFile(file)


sheets = pd.read_excel(xls, sheet_name = None)

name_list = ['all', 'home', 'metro','train','bus','taxi','motorcycle','drive','van','bicycle','foot','other']

df_list = []

melted_df_list = []

main_df = pd.DataFrame()

for i, item in enumerate(sheets):

	print('sheet number: ', i)

	print('sheet name: ', item)

	df = sheets[item]

	df_list.append(df)

	melted_df = pd.melt(df, id_vars = ['name'])

	melted_df['mode'] = item

	melted_df_list.append(melted_df)

	file_name = str(item) + '.csv'

	# melted_df.to_csv(file_name)

	if i < 1:
		main_df = melted_df
	else:

		main_df = main_df.append(melted_df)

	# main_df.append(melted_df)

main_df.to_csv('main_df.csv')


