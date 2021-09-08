x='http://localhost:8181'
s='server'
l=True
k=False
j='key'
i=open
b=''
a=input
L='authToken'
C=print
import pickle as c,json as H,inspect as M,random as d,string as e
N=b.join((d.choice(e.ascii_letters)for A in range(20)))
n='name'
f='failed'
O=a(f'{s} {n}?: ')
if O!=b:C(f'setting {n}');N=O
import requests as P
with i('data.pickle','rb')as f:Q=c.load(f)[j]
def m():0
class E:
	n=b;I={};o={};p=0;q=None;r='GET'
	def __init__(C,**A):
		for B in A.keys():setattr(C,B,A[B])
	def run(A):
		A.q=P.request(A.r,A.n,headers=A.I);A.p=A.q.status_code
		try:A.o=H.loads(A.q.content)
		except H.JSONDecodeError:pass
from servLIB import classes as R
S=[]
T=P.post(f'{x}/{s}',headers={L:Q,'opt':H.dumps({'Name':N})})
A=H.loads(T.content)
if T.status_code!=200:C(f"ohno it {f} message: '{A['message']}'");exit()
U=A['output']
J=U[j]
id=U['id']
F=[]
B=dir(R.server)
B.reverse()
for A in B:
	if not A.startswith('_'):
		V=getattr(R.server,A)
		if M.isfunction(V):
			W=k;X=M.signature(V).parameters;I=[];C(f"firing: {A}")
			for G in list(X)[1:]:
				Y=X[G]
				if Y.kind==Y.VAR_KEYWORD:W=l
				else:I.append(G)
			if W:
				K={}
				for G in I:K[G]=a(f"need a value for {G}: ")
				K[L]=J;F.append(E(I=K,n=f"{x}/{s}/{id}/{A}"))
D={}
D[L]=Q
D['File']='test.txt'
D['Data']='foobar___owo'
p='public'
F.append(E(I=D,n=f'{x}/{p}/lsFiles'))
F.append(E(I=D,n=f'{x}/{p}/putFile'))
F.append(E(I=D,n=f'{x}/{p}/getFile'))
for A in F:
	A.run();C(f"""uri: {A.n} 
status: {A.p} 
args: {A.I} 
output: {A.o}

""")
	if A.p!=200:S.append(A)
g=str.lower(a(f'delete {s}?: ')).strip()
Z=k
if g in['yes','y','1','true']:Z=l
if not Z:
	C(f'writing {s} key/id to file')
	with i(f'log_{s}s.txt','a')as h:h.write(f"sid: {id} key: {J}\n")
else:C(f'deleting {s}');B=E(I={L:J},n=f"{x}/{s}/{id}",r='DELETE');B.run();C(f"""uri: {B.n} 
status: {B.p} 
args: {B.I} 
output: {B.o}

""")
C(f'the following endpoints {f}: ')
for A in S:C(A.url)