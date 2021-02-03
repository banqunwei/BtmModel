
import math

def countWeight(all_dataframe,outputfile_name):

    # all_dataframe = pd.DataFrame(np.arange(15).reshape(3, 5), index=['d1', 'd2', 'd3'],columns=['a', 'b', 'c', 'd', 'e'])
    print(all_dataframe)
    d = all_dataframe.shape[0]  # 行数，文档数D
    n = all_dataframe.shape[1]  # 列数，词汇数N
    print('rows:',d)
    print('cols:',n)

    # 构建weight矩阵
    print('====create weight matrix====')
    weight_dataframe = all_dataframe.copy()
    weight_dataframe = weight_dataframe.astype('float32')

    for i in range(0,d):
        for j in range(0,n):
            weight_dataframe.values[i][j] = 0.0
    print(weight_dataframe)

    # 计算weight
    sum_all = 0.0
    for i in range(0, d):
        for j in range(0, n):
            sum_all += all_dataframe.values[i][j]
    print('sum_all=',sum_all)

    print('====a b c weight====')
    for i in range(0, d):
        for j in range(0, n):
            print(i,j,'----')
            n_ij = all_dataframe.values[i][j]
            print('n_ij=',n_ij)
            a = 0
            b = 0
            c = 0
            sum_row = 0
            sum_col = 0
            if n_ij == 0:
                c = 0
            if n_ij > 0:
                c = -(n_ij / sum_all) * math.log10(n_ij / sum_all)
                for x in range(0, n):
                    sum_row += all_dataframe.values[i][x]
                print('sum_row =', sum_row)
                try:
                    a = math.pow((math.log10(n_ij / sum_row) + 1.0), 0.1)
                except Exception as e:
                    print('Error!!!!')
                    a = 0
                for y in range(0, d):
                    sum_col += all_dataframe.values[y][j]
                print('sum_col =',sum_col)
                try:
                    b = math.log10(math.pow(sum_all/sum_col, 2))
                except Exception as e:
                    print('Error!!!!')
                    b = 0
            print('a,b,c  =',a,b,c)
            weight = a * b * c
            print('weight =',weight)
            weight_dataframe.values[i][j] = weight

    print('====Final weight matrix====')
    print(weight_dataframe)

    print('====Write weight matrix====')

    weight_dataframe.to_csv(outputfile_name)

