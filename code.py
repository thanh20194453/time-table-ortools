from ortools.sat.python import cp_model
model=cp_model.CpModel()
tnm=[int(x) for x in input().split(" ")]
t=tnm[0]#so giao vien
n=tnm[1]#so lop
m=tnm[2]#so mon
lopi=[[]]
gvt=[[]]#gv1_mon1,gv2_mon2
mon_gv=[[] for x in range(0,m+1)]
f=0
lop_mon=[[True for mon in range(0,9)] for lop in range(0,4)]
a=[[[0 for h1 in range(1,3)] for lop1 in range(0,4)] for ngay1 in range(0,7)]
mark=[[[] for h2 in range(0,2)] for ngay2 in range(0,7)]
for i in range(1,n+1):
    x=[int(x) for x in input().split(" ")]
    lopi.append(x)
for i in range(1,t+1):
    x = [int(x) for x in input().split(" ")]
    gvt.append(x)
sotietm_1 = [int(x) for x in input().split(" ")]
print(lopi)
print(gvt)
print(sotietm_1)
for i in range(1,t+1):
    for j in range(1,m+1):
        if j in gvt[i]:
            mon_gv[j].append(i)
print(mon_gv)
gvkhongday=[[],[],[],[]]
for i in range(1,t+1):
    for j in range(1,m+1):
        if j not in gvt[i]:
            gvkhongday[i].append(j)
def checkgv_mon(mon):
    m=[]
    m.append(mon_gv[mon][0])
    return m
c={}
for ngay in range(2,7):
    for lop in range(1,n+1):
        for mon in range(1,m+1):
            for gv in range(1,t+1):
                for h in range(0,2):
                    sotiet = sotietm_1[mon-1]
                    c[(ngay,lop,mon,gv,h,sotiet)]=model.NewBoolVar('cngay%ilop%imon%igv%ih%isotiet%i'%(ngay,lop,mon,gv,h,sotiet))
#neu gv day ko dung mon thi bang 0
for gv in range(1,t+1):
    model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)] for ngay in range(2,7) for lop in range(1,n+1) for h in range(0,2) for mon in gvkhongday[gv] for sotiet in [sotietm_1[mon-1]])==0)
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
            model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)] for mon in range(1,m+1) for lop in range(1,n+1) for sotiet in [sotietm_1[mon-1]])<=1)
#neu gv day tai h=0 co 3 tiet thi khong duoc trung voi h=1 cung ngay
for ngay in range(2,7):
    for gv in range(1,t+1):
        for mon in range(1,m+1):
            for lop in range(1,n+1):
                h=0
                sotiet = sotietm_1[mon-1]
                if sotiet==3:
                    model.Add(sum((c[(ngay,lop1,mon1,gv,h1,sotiet1)] for h1 in range(1,2) for mon1 in range(1,m+1) for lop1 in range(1,n+1) for sotiet1 in [sotietm_1[mon1-1]]),c[(ngay,lop,mon,gv,h,sotiet)])<=1)

#moi lop hoc 8 mon it nhat 1 lan
for mon in range(1,m+1):
    for lop in range(1, n + 1):
        sotiet = sotietm_1[mon - 1]
        model.Add(sum(c[(ngay,lop,mon,gv,h,sotiet)] for h in range(0, 2) for ngay in range(2,7) for gv in mon_gv[mon] ) >= 1)

#in ket qua
solver = cp_model.CpSolver()
solver.Solve(model)
a=[[[[] for h01 in range(1,3)] for lop01 in range(0,4)] for ngay01 in range(0,7)]
for ngay in range(2,7):
    for lop in range(1,n+1):
        for mon in range(1,m+1):
            for gv in mon_gv[mon]:
                for h in range(0,2):
                    sotiet = sotietm_1[mon-1]
                    if solver.Value(c[(ngay,lop,mon,gv,h,sotiet)]) == 1:
                        a[ngay][lop][h]=[mon,gv]
tabledata=[["lớp 1"],["lớp 2"],["lớp 3"]]
for lop in range(1,n+1):
    for ngay in range(2,7):
        tabledata[lop-1].append("%s"%(a[ngay][lop]))
thu=["","thứ 2","thứ 3","thứ 4","thứ 5","thứ 6"]
print("{: ^20} {: ^20} {: ^20} {: ^20} {: ^20} {: ^20}".format(*thu))
for row in tabledata:
    print("{: ^20} {: ^20} {: ^20} {: ^20} {: ^20} {: ^20}".format(*row))
print()
print('Statistics')
print('  - wall time       : %f s' % solver.WallTime())
