#df.to_csv( 'E:/temp/Thema/Input/Demand_Profiles3.csv', sep=',', index=False)
#df.to_csv( 'E:/temp/Thema/Input/Demand_Profiles3.csv', sep=',', index=False)

from pandas import DataFrame

input = DataFrame.from_csv('E:/temp/Thema/Input/Demand_Profiles3.csv')
input.index.names = [' ']
newColsMap = dict(zip(input.columns, [x + ' ' * (len(str(input[x][1])) -2) for x in input.columns]))
input.rename(columns=newColsMap, inplace=True)
csv = input.to_csv(sep='\t', float_format='%.9f')
resultString = '''len
* Demand Profiles exported by Excel

Sets
Demand_Profile_ID            / 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 /
;

TABLE Demand_Profiles(Hours_ID,Demand_Profile_ID) Demand Profiles exported by Excel

%s;
''' % csv
resultStringReplaced = resultString.replace("\t", "\t\t")

with open('E:/temp/Thema/Input/Demand_Profiles.gms', 'w') as fileOutput:
    fileOutput.write(resultStringReplaced)