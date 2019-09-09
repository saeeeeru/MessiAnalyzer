import json, io

import numpy as np
import pandas as pd

from pandas.io.json import json_normalize

import matplotlib.pyplot as plt
import matplotlib.cm

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.projections import get_projection_class
from matplotlib.patches import Arc

import matplotlib.image as image
from matplotlib import transforms

class PlotSonars():

        
    def __init__(self, match_id, team_no, colormap=None):
        self.match_id = match_id
        self.team_no = team_no
        self.colormap = matplotlib.cm.viridis if colormap is None else colormap
        self.team2_no = 0 if self.team_no == 1 else 1
        

    def Main(self):
        """ Reading event data and creating team-level pass sonars for a team from a match"""
        player_dict = {}
        klist = []
        xlist = []
        ylist = []
        playerposlist = []
        base_link = "C://Users/ADMIN/Desktop/Abhishek/open-data/data/events/"
        fig, ax = plt.subplots()
        
                
        mid, r, cmap, c = self.match_id, self.team_no, self.colormap, self.team2_no
        link = base_link + str(mid) + ".json"
        
        
        with io.open(link, "r", encoding = 'utf-8-sig') as f:
            obj = json.load(f)
        df = json_normalize(obj)
        
        uteams = df["team.name"].unique()
        
        team = df[(df["type.name"]=="Pass") & (df["team.name"]==uteams[r])]
        
        image_link = r"C://Users/ADMIN/Desktop/Abhishek/open-data/stats-bomb-logo.png"
        im = image.imread(image_link)
        image_arr = np.array(im)
        im = image_arr
        for _ in range(3):
            im = np.rot90(im)
        ax.imshow(im, aspect = "auto", extent = (-14,-4,-2,40), zorder = 2, interpolation="nearest")


        for player in df.loc[r,"tactics.lineup"]:
                p = player["player"]
                l = player["position"]
                pos = l["name"]
                name = p["name"]
                playerposlist.append(pos)
                klist.append(name)

        positions_json = r"C:\Users\ADMIN\Desktop\Abhishek\PositionsStatsbomb.json"
        with open(positions_json, "r") as f:
                full_dict = json.load(f) 


        for i in playerposlist:
                x,y = full_dict[i]
                xlist.append(x)
                ylist.append(y)


                
        for x,y,z in zip(xlist, ylist, klist):
            entry = {z:[x,y]}
            player_dict.update(entry)

        norm = plt.Normalize(team["pass.length"].min(), 30) ##Change 30 to whatever you want the upper bound for the length of the pass to be in the colormap. Change to "team["pass.length"].max()" for the maximum
        
        ar = np.array(team["pass.length"])
        sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, orientation="horizontal", fraction=0.046, pad=0.04)
        cbar.ax.set_xlabel("Average length of passes in a direction", fontstyle = "italic", fontsize = 7)
        cbar.ax.xaxis.set_tick_params(color = "xkcd:salmon")
        plt.setp(plt.getp(cbar.ax.axes, "xticklabels"), color = "xkcd:salmon")




        #Pitch Outline
        ax.set_aspect(1)
        
        ax.plot([0,0],[0,80], color="black")
        ax.plot([0,120],[80,80], color="black")
        ax.plot([120,120],[80,0], color="black")
        ax.plot([120,0],[0,0], color="black")

        ax.plot([60,60],[0,80], color="black")

        #Left Penalty Area
        ax.plot([0,18],[18,18], color="black")
        ax.plot([18,18],[18,62], color="black")
        ax.plot([18,0],[62,62], color="black")

        #Right Penalty Area
        ax.plot([102,120],[18,18], color="black")
        ax.plot([102,102],[18,62], color="black")
        ax.plot([102,120],[62,62], color="black")

        #6-yard box left
        ax.plot([114,120],[30,30], color="black")
        ax.plot([114,114],[30,50], color="black")
        ax.plot([114,120],[50,50], color="black")

        #6-yard box right
        ax.plot([0,6],[30,30], color="black")
        ax.plot([6,6],[30,50], color="black")
        ax.plot([0,6],[50,50], color="black")

          
            #Prepare Circles
        centreCircle = plt.Circle((60,40),9.15,color="black",fill=False)
        centreSpot = plt.Circle((60,40),0.8,color="black")
        leftPenSpot = plt.Circle((12,40),0.8,color="black")
        rightPenSpot = plt.Circle((108,40),0.8,color="black")
            
            #Draw Circles
        ax.add_patch(centreCircle)
        ax.add_patch(centreSpot)
        ax.add_patch(leftPenSpot)
        ax.add_patch(rightPenSpot)
            
            #Prepare Arcs
        leftArc = Arc((12,40),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="black")
        rightArc = Arc((108,40),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="black")

        #Goals

        ax.plot([-3,0],[36,36],color="black", linewidth=2)
        ax.plot([-3,-3],[36,44],color="black", linewidth=2)
        ax.plot([-3,0],[44,44],color="black", linewidth=2)

        ax.plot([120,123],[36,36],color="black", linewidth=2)
        ax.plot([123,123],[36,44],color="black", linewidth=2)
        ax.plot([120,123],[44,44],color="black", linewidth=2)

            #Draw Arcs
        ax.add_patch(leftArc)
        ax.add_patch(rightArc)



            #Tidy Axes and Extra information
        ax.axis('off')
        ax.text(125, 42, "PASS SONAR: {}".format(uteams[r]), rotation = -90, fontweight = "bold", fontsize = 12)
        ax.text(122, 59, "vs {}".format(uteams[c]), rotation = -90, fontweight = "bold", fontsize = 7)
        ax.text(1,1,"by Abhishek Sharma\nConcept: Eliot McKinley", rotation= -90, fontsize=4.5, color="k", fontweight="bold")


        for player, loc in player_dict.items():
            ax.text(loc[0]+7, loc[1]-5, player, size = 6, rotation = -90, fontweight = "bold")
            
            local_df = df.copy(deep=True)
            local_df = local_df[local_df["type.name"]=="Pass"]
            local_df = local_df[local_df["player.name"]==player]
            local_df = local_df.dropna(axis=1, how="all")

            df1 = local_df[['pass.angle','pass.length']].copy()
            

            bins = np.linspace(-np.pi,np.pi,24)

            df1['binned'] = pd.cut(local_df['pass.angle'], bins, include_lowest=True, right = True)
            df1["Bin_Mids"] = df1["binned"].apply(lambda x: x.mid)
            A= df1.groupby("Bin_Mids", as_index=False)["pass.length"].agg(['mean', 'count']).reset_index().rename(columns = {"mean": "pass.length", "count": "Frequency"})
            A = A.dropna().reset_index(drop=True)
            A['Bin_Mids'] = A['Bin_Mids'].astype(np.float64)
            A["Bin_Mids"] = A["Bin_Mids"] * -1


            ################


            ax_sub= inset_axes(ax, width=1.1, height=1.1, loc=10, 
                               bbox_to_anchor=(loc[0],loc[1]),
                               bbox_transform=ax.transData, 
                               borderpad=0.0, axes_class=get_projection_class("polar"))
            
            theta = A["Bin_Mids"]
            radii = A["Frequency"]
            length = np.array(A["pass.length"])
            cm = cmap(norm(length))
            bars = ax_sub.bar(theta, radii, width=0.3, bottom=0.0)
            ax_sub.set_xticklabels([])
            ax_sub.set_yticks([])
            ax_sub.yaxis.grid(False)
            ax_sub.xaxis.grid(False)
            ax_sub.spines['polar'].set_visible(False)
            ax_sub.patch.set_facecolor("white")
            ax_sub.patch.set_alpha(0.1)
            for r,bar in zip(cm,bars):
                    bar.set_facecolor(r)

        ax.scatter(xlist, ylist, s=1, alpha=0.0)              

plt.show()
       
