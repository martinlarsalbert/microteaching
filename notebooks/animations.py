import numpy as np
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import transforms

class BallAnimation(animation.TimedAnimation):
    def __init__(self, ts, positions):
        fig,axes = plt.subplots(ncols=2)
        fig.set_size_inches(12,8)
        self.fig = fig
        self.axes=axes

        self.t = ts
        self.y = positions
         
        ax = axes[0]
        ax.set_ylim(-500,0)
        ax.set_xlim(0,0)
        ax.set_ylabel('Position [m]')
        ax.grid(True)
        
        ax = axes[1]
        ax.set_ylim(-500,0)
        ax.set_xlim(0,self.t[-1])
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Position [m]')
        ax.grid(True)
                
        self.ball = Line2D([], [], linestyle='', marker='o',color='b', ms=20)
        self.ball_time = Line2D([], [], color='red', linewidth=2)
        
        axes[0].add_line(self.ball)
        axes[1].add_line(self.ball_time)
        
        return animation.TimedAnimation.__init__(self, fig, interval=50, blit=True)

    def _draw_frame(self, framedata):
        i = framedata
        x = 0
        position=self.y[i]
        y = position
            
        self.ball.set_data(x, y)
        
        times = np.arange(i, dtype=int)
        self.ball_time.set_data(self.t[times],self.y[times])  
        
        self._drawn_artists = [self.ball,self.ball_time]
                
    def new_frame_seq(self):
        return iter(range(self.t.size))

    def _init_draw(self):
        lines = [self.ball,self.ball_time]

        for l in lines:
            l.set_data([], [])


def add_ship(ax):
    beam=1
    height=0.5
    ship = Rectangle(xy=(-beam/2,-height/2),width=1,height=0.5)
    ax.add_patch(ship)
    
    ax.axis('equal')
    xlim=1.3*beam/2*np.array([-1,1])
    ax.set_xlim(xlim)
    ax.set_ylim(xlim)
    
    ax.plot(xlim,[0,0],'b-');
    
    return ship
    
def rotate_ship(ship,ax,angle):
    t2 = transforms.Affine2D().rotate_deg(-np.rad2deg(angle)) + ax.transData
    ship.set_transform(t2)

class RollDecayAnimation(animation.TimedAnimation):
    def __init__(self, ts, phis):
        
        fig,axes = plt.subplots(ncols=2)
        fig.set_size_inches(12,8)
        self.fig = fig
        self.axes=axes
        
        self.t = ts
        self.phis = phis
        
        ax = axes[0]
        self.ship=add_ship(ax=ax)
        
        ax = axes[1]
        ax.set_ylim(np.min(np.rad2deg(self.phis)),np.rad2deg(np.max(self.phis)))
        ax.set_xlim(0,self.t[-1])
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('roll [deg]')
        ax.grid(True)
    
        
        self.phi_time = Line2D([], [], color='red', linewidth=2)
        
        #axes[0].add_line(self.ball)
        axes[1].add_line(self.phi_time)
        
        return animation.TimedAnimation.__init__(self, fig, interval=30, blit=True)

    def _draw_frame(self, framedata):
        i = framedata
        
        phi=self.phis[i]
        times = np.arange(i, dtype=int)
        self.phi_time.set_data(self.t[times],np.rad2deg(self.phis[times]))  
        
        rotate_ship(ship=self.ship, ax=self.axes[0], angle=phi)
        
        self._drawn_artists = [self.phi_time, self.ship]
                
    def new_frame_seq(self):
        return iter(range(self.t.size))

    def _init_draw(self):
        lines = [self.phi_time]

        for l in lines:
            l.set_data([], [])


class ParametricRollAnimation(animation.TimedAnimation):
    def __init__(self, ts, phis, Cs):
        
        fig,axes = plt.subplots(ncols=2)
        fig.set_size_inches(12,8)
        self.fig = fig
        self.axes=axes
        
        self.t = ts
        self.phis = phis
        self.Cs = Cs
        
        ax = axes[0]
        self.ship=add_ship(ax=ax)
        
        ax = axes[1]
        
        ax_C = ax.twinx()

        ax.set_ylim(np.min(np.rad2deg(self.phis)),np.rad2deg(np.max(self.phis)))
        ax.set_xlim(0,self.t[-1])
        ax.set_xlabel('Time [s]')
        #ax.set_ylabel('roll [deg]')
        #ax.grid(True)
            
        self.phi_time = Line2D([], [], color='red', linewidth=4, label='roll')
        self.C_time = Line2D([], [], color='green', linewidth=4, label='stability')

        ax.add_line(self.phi_time)
        ax_C.add_line(self.C_time)
        
        ax_C.set_ylim(np.min(self.Cs),np.max(self.Cs))
        ax_C.set_xlim(0,self.t[-1])
        ax_C.legend(loc='upper right')
        ax.legend(loc='upper left')
        
        return animation.TimedAnimation.__init__(self, fig, interval=30, blit=True)

    def _draw_frame(self, framedata):
        i = framedata
        
        phi=self.phis[i]
        times = np.arange(i, dtype=int)
        self.phi_time.set_data(self.t[times],np.rad2deg(self.phis[times]))  
        self.C_time.set_data(self.t[times],self.Cs[times])  
        

        rotate_ship(ship=self.ship, ax=self.axes[0], angle=phi)
        
        self._drawn_artists = [self.phi_time, self.C_time, self.ship]
                
    def new_frame_seq(self):
        return iter(range(self.t.size))

    def _init_draw(self):
        lines = [self.phi_time]

        for l in lines:
            l.set_data([], [])