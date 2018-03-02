import xlwings as xw
import pandas as pd
myBook = xw.Book()

df1 = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6], 'c':[1,2,3], 'd':[4,5,6]})
df1.set_index(['a','b'], inplace=True)
df2 = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6], 'c':[2,2,3], 'd':[4,5,7]})
df2.set_index(['a','b'], inplace=True)

dfdiff = df1.diff(df2, )

xw.Range('A2').value=[
    [r'=sum(1,2,3)', r'=sum(1,3,3)', r'=sum(1,2,5)',],
    [r'=sum(2,2,3)', r'=sum(1,3,3)', r'=sum(1,22,5)',],
    [r'=sum(4,2,3)', r'=sum(1,3,33)', r'=sum(11,2,5)',],
]


ss = pd.Series(range(2, 100002))

df = pd.DataFrame({
        'a': ss,
        'b': 'dummy',
        'c': 'dummy',
})                 

for i in range(3):
    df.iloc[:, i] = "=INDIRECT(\"'\" & $A$1 & \"'!\" & ADDRESS(" + ss.astype(str) + "," + str(i+1) + "))"
    
book=xw.Book('Book4')
book.sheets['Sheet1'].range('A2').value = df
book.
