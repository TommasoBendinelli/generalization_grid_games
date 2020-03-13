from generalization_grid_games.envs import TwoPlayerGeneralizationGridGame

class PlayingXYZGeneralizationGridGame(TwoPlayerGeneralizationGridGame):
    fig_scale = 0.5

    def __init__(self, layout, interactive=False, record_video=False, video_out_path='out.mp4'):
        self.layout = np.array(layout, dtype=object)

        self.initial_layout = layout.copy()
        self.current_layout = layout.copy()

        self.interactive = interactive
        self.action = []
        self.layout_demo = []
        if record_video:
            self.start_recording_video(video_out_path)
        else:
            self.record_video = False
        
        height, width = layout.shape
        self.width, self.height = width, height

        self.observation_space = spaces.MultiDiscrete(self.num_tokens * np.ones((height, width)))
        self.action_space = spaces.MultiDiscrete([self.height, self.width])
        self.counter = 0
        if interactive:
            self.action_lock = False

            # # Create the figure and axes
            self.fig, self.ax, self.textbox = self.initialize_figure(height, width)
            self.drawings = []
            self.render_onscreen()
            self.current_text_value = None

            # Create event hook for mouse clicks
            self.fig.canvas.mpl_connect('pick_event', self.button_press)
            
            # Create event for keyboard
            self.textbox.on_submit(self.submit)

            print("Initial Step")
            plt.show()

    def step(self, action):
        self.last_action = action

        next_layout = self.transition(self.current_layout, action)
        reward = self.compute_reward(self.current_layout, action, next_layout)
        done = self.compute_done(next_layout)
        self.current_layout = next_layout
        
        if self.record_video:
            for i in range(4):
                self.recorded_video_frames.append(self.render())
        if self.interactive:
            self.render_onscreen()
        
        return next_layout.copy(), reward, done, {}
    
    ### Main stateful methods
    def reset(self):
        self.current_layout = self.initial_layout.copy()

        self.last_action = None

        if self.record_video:
            for i in range(2):
                self.recorded_video_frames.append(self.render())
        if self.interactive:
            self.render_onscreen()

        return self.current_layout.copy()
    
    def render_onscreen(self):
        #if self.last_actio
        #self.fig, self.ax = initialize_figure(self.height, self.width)
        return self.get_image(self.current_layout)

    @classmethod
    def initialize_figure(cls, height, width):
        fig = plt.figure(figsize=((width + 2) * cls.fig_scale , (height) * cls.fig_scale + 2 ))
        ax = fig.add_axes((0.05, 0.1, 0.9, 0.9),
                                    aspect='equal', frameon=False,
                                    xlim=(-0.05, width + 0.05),
                                    ylim=(-0.05, height + 0.05))
        ax.set_picker(True)
        ax.name = "Grid"
        axbox = fig.add_axes([0.1, 0.02, 0.8, 0.075], xlim=(-0.05, width + 0.05),
                                    ylim=(height + 0.05, height + 0.10))
        axbox.set_picker(True)
        axbox.name = "TextBox"
        text_box = TextBox(axbox,"", initial=" ")
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_formatter(plt.NullFormatter())
            axis.set_major_locator(plt.NullLocator())

        return fig, ax, text_box

    @staticmethod
    def compute_reward(layout0, action, layout1):
        return 
    
    @staticmethod
    def compute_done(layout):
        return 0

    ### Helper stateless methods
    @classmethod
    def get_image(cls, observation, mode='human', close=False):
        height, width = observation.shape

        fig, ax, useless = cls.initialize_figure(height, width)

        for r in range(height):
            for c in range(width):
                token = observation[r, c]
                cls.draw_token(token, r, c, ax, height, width)

        # if action is not None:
        #     cls.draw_action(action, ax, height, width)

        im = fig2data(fig)
        plt.close(fig)

        return im

    @classmethod
    def draw_action(cls, action, ax, height, width):
        r, c = action
        if not (isinstance(r, int) or isinstance(r, np.int8) or isinstance(r, np.int64)):
            r -= 0.5
            c -= 0.5
        oi = OffsetImage(cls.hand_icon, zoom = 0.3 * cls.fig_scale * (2.5 / max(height, width)**0.5))
        box = AnnotationBbox(oi, (c + 0.5, (height - 1 - r) + 0.5), frameon=False)
        ax.add_artist(box)
   

    def submit(self, text_at_submit):
        if str.split(text_at_submit) and (str.split(text_at_submit)[0] in ('xyz') or text_at_submit.strip() == "pass"):
            self.current_text_value = str.split(text_at_submit)[0]
        else: self.current_text_value = None 

    def button_press(self, event):
        if event.artist.name == "Grid" and event.mouseevent.button==1 : #Mouse Left
            if self.current_text_value != None and event.mouseevent.key != 'd':
                event = event.mouseevent
                if self.action_lock:
                    return
                if (event.xdata is None) or (event.ydata is None):
                    return
                i, j = map(int, (event.xdata, event.ydata))
            
                if (i < 0 or j < 0 or i >= self.width or j >= self.height):
                    return

                self.action_lock = True
                c, r = i, self.height - 1 - j
                if event.button == 1:
                    self.action.append((self.current_text_value,(r, c)))
                    self.layout_demo.append(self.current_layout.copy()) 
                    print("Step {} recorded".format(self.counter))
                    self.counter += 1
                    self.step((self.current_text_value,(r, c)))
                #self.fig.canvas.draw()
                self.action_lock = False
            elif event.mouseevent.key == 'd': #Delete element
                event = event.mouseevent
                if self.action_lock:
                    return
                if (event.xdata is None) or (event.ydata is None):
                    return
                i, j = map(int, (event.xdata, event.ydata))
            
                if (i < 0 or j < 0 or i >= self.width or j >= self.height):
                    return

                self.action_lock = True
                c, r = i, self.height - 1 - j
                if event.button == 1:
                    self.action.append((self.current_text_value,(r, c)))
                    self.layout_demo.append(self.current_layout.copy()) 
                    print("Step {} recorded".format(self.counter))
                    self.counter += 1
                    self.step(('empty',(r, c)))
                self.action_lock = False
            else: 
                return
        elif event.artist.name == "Grid" and event.mouseevent.button == 3: #Mouse Right
            pass
        else: 
            return
