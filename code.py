from ortools.sat.python import cp_model
model=cp_model.CpModel()
from datetime import datetime
start_time = datetime.now()
def read_file():
    f = open("data8.txt",'r')
    Ti = [[]]
    Ci = [[]]
    a = [[int(num) for num in line.split()] for line in f]
    T = a[0][0]
    N = a[0][1]
    M = a[0][2]
    #print(T, N, M)
    Ci=[[]]+a[1:N+1]
    #print(Ci)
    Ti=[[]]+a[N+1:N+T+1]
    #print(Ti)
    Di = a[N+T+1:][0]
    #print(Di)
    f.close()
    return T,N,M,Ci,Ti,Di
t,n,m,lopi,gvt,sotietm_1 = read_file()
lop_mon=[[True for mon in range(0,9)] for lop in range(0,n+1)]
mon_gv=[[] for x in range(0,m+1)]
for i in range(1,t+1):
    for j in range(1,m+1):
        if j in gvt[i]:
            mon_gv[j].append(i)
gvkhongday=[[] for gv in range(0,t+1)]
for i in range(1,t+1):
    for j in range(1,m+1):
        if j not in gvt[i]:
            gvkhongday[i].append(j)
c={}
for ngay in range(2,7):
    for lop in range(1,n+1):
        for mon in range(1,m+1):
            for gv in range(1,t+1):
                for h in range(0,2):
                    sotiet = sotietm_1[mon-1]
                    c[(ngay,lop,mon,gv,h,sotiet)]=\
                    model.NewBoolVar('c%i%i%i%i%i%i'%(ngay,lop,mon,gv,h,sotiet))
#neu gv day ko dung mon thi bang 0
for gv in range(1,t+1):
    model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)] for ngay in range(2,7)
                                                    for lop in range(1,n+1)
                                                        for h in range(0,2)
                                                            for mon in gvkhongday[gv]
                                                                for sotiet in [sotietm_1[mon-1]])==0)
#so tiet moi ngay-moi lop khong qua 5, lon hon 2/////trong 1 ngay-1 lop chi co duy nhat 1 h=0 va co the co h=1
for ngay in range(2,7):
    for lop in range(1,n+1):
        model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)]*sotiet for h in range(0,2) for mon in range(1,m+1) for gv in range(1,t+1) for sotiet in [sotietm_1[mon-1]])<=5)
        model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)]*sotiet for h in range(0,2) for mon in range(1,m+1) for gv in range(1,t+1) for sotiet in [sotietm_1[mon-1]])>=2)
        model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)] for h in range(0,1) for mon in range(1,m+1) for gv in range(1,t+1) for sotiet in [sotietm_1[mon-1]])==1)
        model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)] for h in range(1,2) for mon in range(1,m+1) for gv in range(1,t+1) for sotiet in [sotietm_1[mon-1]])<=1)
# 1gv trong 1 ngay trong 1 h chi day nhieu nhat 1 lop, 1 mon
for ngay in range(2,7):
    for gv in range(1,t+1):
        for h in range(0, 2):
            model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)] for mon in range(1,m+1)
                                                            for lop in range(1,n+1)
                                                                for sotiet in [sotietm_1[mon-1]])<=1)
#neu gv day tai h=0 co >=3 tiet thi khong duoc trung voi h=1 co >=3 tiet cung ngay
for ngay in range(2,7):
    for gv in range(1,t+1):
        for mon in range(1,m+1):
            for lop in range(1,n+1):
                h=0
                sotiet = sotietm_1[mon-1]
                if sotiet>=3:
                    model.Add(sum((c[(ngay,lop1,mon1,gv,1,sotiet1)] for mon1 in range(1,m+1)
                                                                        for lop1 in range(1,n+1)
                                                                            for sotiet1 in [sotietm_1[mon1-1]]
                                                                                if sotiet1>=3),c[(ngay,lop,mon,gv,h,sotiet)])<=1)

#moi lop hoc 8 mon it nhat 1 lan
for lop in range(1, n + 1):
    for mon in lopi[lop]:
        sotiet = sotietm_1[mon - 1]
        model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)] for h in range(0, 2)
                                                        for ngay in range(2,7)
                                                            for gv in mon_gv[mon])==1)

#in ket qua
solver = cp_model.CpSolver()
solver.Solve(model)
a=[[[[] for h01 in range(1,3)] for lop01 in range(0,n+1)] for ngay01 in range(0,7)]
for ngay in range(2,7):
    for lop in range(1,n+1):
        for mon in range(1,m+1):
            for gv in mon_gv[mon]:
                for h in range(0,2):
                    sotiet = sotietm_1[mon-1]
                    if solver.Value(c[(ngay,lop,mon,gv,h,sotiet)]) == 1:
                        a[ngay][lop][h]=[mon,gv]
tabledata=[]
for lop in range(1,n+1):
    v="lớp %s"%(lop)
    tabledata.append([v])
for lop in range(1,n+1):
    for ngay in range(2,7):
        tabledata[lop-1].append("%s"%(a[ngay][lop]))
thu=["","thứ 2","thứ 3","thứ 4","thứ 5","thứ 6"]
print("{: ^20} {: ^20} {: ^20} {: ^20} {: ^20} {: ^20}".format(*thu))
for row in tabledata:
    print("{: ^20} {: ^20} {: ^20} {: ^20} {: ^20} {: ^20}".format(*row))
print()
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
