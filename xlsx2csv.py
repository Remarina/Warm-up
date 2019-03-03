import os, openpyxl, csv

'''
convert all .xlsx files in current folder into .csv

'''

folder = '.'

for excel_file in os.listdir(folder):
	if not excel_file.endswith('.xlsx'):
		continue
	else:
		print('\n'+ 'Конвертация файла ' + excel_file + '\n')
		excel_obj = openpyxl.load_workbook(excel_file)
		for sheet_name in excel_obj.sheetnames:
			sheet = excel_obj[sheet_name]
			csv_file_name = excel_file[:-5] +'_' + sheet_name + '.csv'
			with open(csv_file_name, 'w') as csv_file_obj:
				csv_writer = csv.writer(csv_file_obj)
				for row in range(1, sheet.max_row + 1):
					row_data = []
					for column in range(1, sheet.max_column + 1):
						row_data.append(sheet.cell(row = row, column = column).value)				
					csv_writer.writerow(row_data)
				print('\n' + 'Завершение работы с ' + excel_file + '\n' + '-'*50)











