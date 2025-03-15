import tkinter
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('TkAgg')
import numpy as np
import scipy as sp

def isfloat(s):
    try:
        float(s)
    except:
        return False
    return True


def listdist(listA,listB):
    assert(len(listA)==len(listB))
    S=0
    for s in range(len(listA)):
        S+=(listA[s]-listB[s])**2
    return np.sqrt(S)

def read_bandstructure_CP2K(bandfile):
    filestr=open(bandfile)
    filevec=[]
    Kvec=[]
    Klen=[0]
    bind=0
    for x in filestr:
        xsp=x.split()
        if xsp==[]:
            continue
        if ((xsp[0][0]=="k") or (xsp[1][0]=="P")):
            Kvec.append([eval(xsp[3]),eval(xsp[4]),eval(xsp[5])])
            if (len(Klen)!=0):
                Klen.append(Klen[-1]+listdist(Kvec[-1],Kvec[0]))
            else:
                Klen=[0]
            filevec.append([])
            bind+=1
            continue
        if (isfloat(xsp[0])):
            filevec[-1].append([bind]+[float(s) for s in xsp if isfloat(s)])
    bandvec2=np.array(filevec)
    return bandvec2


def plotband(ELIM=5):
    mpl.rcParams.update({'font.size': 24})
    fig = plt.figure()
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    bandCP2K=read_bandstructure_CP2K("bandstructure_SCF_and_G0W0_plus_SOC")
    nbCP2K=np.size(bandCP2K,1)
    plt.ylim([-ELIM,ELIM])
    plt.plot(bandCP2K[:,:,-1]-0.218,'b')
    plt.ylabel("Energy (eV)")
    xtick=[0,159,318]
    ticks=[r"$\leftarrow$ K",r"$\Gamma$",r"M $\rightarrow$"]
    plt.title(r"$\mathrm{Bi_2Te_3}$")
    plt.xticks(xtick,ticks)
    ax=plt.gca()
    ax.tick_params(width=2,size=10)
    handles, labels=plt.gca().get_legend_handles_labels()
    labels, ids = np.unique(labels, return_index=True)
    handles = [handles[i] for i in ids]
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    fig=plt.gcf()
    #plt.show()
    fig.set_size_inches(figManager.window.winfo_screenwidth()/2/fig.dpi,figManager.window.winfo_screenheight()/2/fig.dpi)
    plt.savefig("Bi2Te3.png",dpi=fig.dpi)
    #print("BGWQE", MAE(KBGWFF,KQE,bandBGWFF[BGWsortlist,:,2],bandQE[:,:],gapBGWFF,gapQE))
    #print("QEC2K", MAE(KQE,CP2Kxlist,bandQE[:,:],bandCP2K[:,:,3],gapQE,gapCP2K))
    #print("BGWC2K", MAE(KBGWFF,CP2Kxlist,bandBGWFF[BGWsortlist,:,2],bandCP2K[:,:,3],gapBGWFF,gapCP2K))
    #print(MAE(KQE,CP2Kxlist,bandQE[QEsortlist,:],bandCP2K[:,:,3],gapQE,gapCP2K),MAE(KQE,KBGWFF,bandQE[QEsortlist,:],bandBGWFF[BGWsortlist,:,2],gapQE,gapBGWFF),MAE(KBGWFF,99/38*(bandCP2K[:,0,0]-1),bandBGWFF[BGWsortlist,:,2],bandCP2K[:,:,3],gapBGWFF,gapCP2K))

#tol=["3e-2","1e-2","3e-3","1e-3","3e-4","1e-4","3e-5","1e-5"]
plotband(ELIM=0.1)
