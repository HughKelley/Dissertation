# import pandas as pd

file = "C:/Users/Hugh/Documents/UCL_CASA_1819/Dissertation/Analysis/Data/journey_to_work_data.csv"

with open(file, 'r') as f:
	print(f.readline())
	print(f.readline())
	print(f.readline())
	print(f.readline())

# top = pd.read_csv(file, nrows = 20)

# print(top.head(5))

# print(list(top.columns.values))