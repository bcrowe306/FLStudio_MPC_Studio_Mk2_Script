from framework.component import Component
from mpc_studio_mk2.controls import Controls

class BrowserNavigationComponent(Component):
    def __init__(self, name: str = 'BrowserNavigationComponent'):
        super(BrowserNavigationComponent, self).__init__(name=name)
        self.jog_wheel = Controls.jog_wheel
        self.jog_button = Controls.jog_button
        self.selected_channel = None
        self.sample_select_button = Controls.sample_select_button
        self.minus_button = Controls.minus_button
        self.plus_button = Controls.plus_button
        self.jog_shift_button = Controls.jog_shift_button
        self.sample_start_button = Controls.sample_start_button
    
    @Component.subscribe('plus_button', 'pressed')
    def _on_plus_button_pressed(self, pressed):
        self.plus_button.set_light(
            'FULL_1') if pressed else self.plus_button.set_light('DIM_1')

    @Component.subscribe('minus_button', 'pressed')
    def _on_minus_button_pressed(self, pressed):
        self.minus_button.set_light(
            'FULL_1') if pressed else self.minus_button.set_light('DIM_1')

    @Component.subscribe('plus_button', 'toggled')
    def _on_plus_button_toggled(self, toggled):
        if self.fl.patterns.patternNumber() < self.fl.patterns.patternMax():
            self.fl.patterns.jumpToPattern(self.fl.patterns.patternNumber() + 1)
            
    @Component.subscribe('minus_button', 'toggled')
    def _on_minus_button_toggled(self, toggled):
        if self.fl.patterns.patternNumber() > 1:
            self.fl.patterns.jumpToPattern(self.fl.patterns.patternNumber() - 1)

    @Component.subscribe('sample_start_button', 'toggled')
    def _on_sample_start_button_toggled(self, _):
        nodeFileType = self.fl.ui.getFocusedNodeFileType()
        if nodeFileType == 7:
            self.fl.ui.selectBrowserMenuItem()
            for _ in range(9):
                self.fl.transport.globalTransport(
                    41, 1, self.fl.midi.PME_System | self.fl.midi.PME_FromMIDI)
            self.fl.transport.globalTransport(
                80, 1, self.fl.midi.PME_System | self.fl.midi.PME_FromMIDI)

    @Component.subscribe('sample_select_button', 'toggled')
    def _on_sample_browser_select_toggled(self, _):
        self._open_in_new_channel()

    def _open_in_new_channel(self):
        nodeFileType = self.fl.ui.getFocusedNodeFileType()
        if nodeFileType == 7:
            self.fl.ui.selectBrowserMenuItem()
            self.fl.transport.globalTransport(
                41, 1, self.fl.midi.PME_System | self.fl.midi.PME_FromMIDI)
            self.fl.transport.globalTransport(
                41, 1, self.fl.midi.PME_System | self.fl.midi.PME_FromMIDI)
            self.fl.transport.globalTransport(
                80, 1, self.fl.midi.PME_System | self.fl.midi.PME_FromMIDI)

    @Component.subscribe('jog_shift_button', 'toggled')
    def _on_jog_shift_button_toggled(self, _):
        self.fl.transport.globalTransport(
            81, 1, self.fl.midi.PME_System | self.fl.midi.PME_FromMIDI)

    @Component.subscribe('jog_button', 'toggled')
    def _on_jog_button_toggled(self, _):
        self.show_focus_browser()
        nodeFileType = self.fl.ui.getFocusedNodeFileType()
        if nodeFileType == -1:
            return
        elif nodeFileType <= -100:
            self.fl.ui.setFocused(self.fl.midi.widBrowser)
            self.fl.transport.globalTransport(
                80, 80, self.fl.midi.PME_System)
            
        elif self.fl.ui.isInPopupMenu() == 1:
            self.fl.ui.enter()
        else:
            self.fl.ui.selectBrowserMenuItem()

    @Component.subscribe('jog_wheel', 'inc')
    def _on_jog_wheel_inc(self, value):
        self.show_focus_browser()
        self.fl.ui.navigateBrowserMenu(1, True)
    
    @Component.subscribe('jog_wheel', 'dec')
    def _on_jog_wheel_dec(self, value):
        self.show_focus_browser()
        self.fl.ui.navigateBrowserMenu(-1, True)
    
    def activate(self):
        self.show_focus_browser()
        return super().activate()
    
    def show_focus_browser(self):
        visibleWindow = self.fl.ui.getVisible(self.fl.midi.widBrowser)
        focusedWindow = self.fl.ui.getFocused(self.fl.midi.widBrowser)
        if visibleWindow != 1:
            print(visibleWindow)
            self.fl.ui.showWindow(self.fl.midi.widBrowser)
        if focusedWindow !=1:
            self.fl.ui.setFocused(self.fl.midi.widBrowser)