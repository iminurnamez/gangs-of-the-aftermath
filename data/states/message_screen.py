import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup


class MessageScreen(tools._State):
    def __init__(self):
        super(MessageScreen, self).__init__()
        self.window_img = prepare.GFX["ui-window"]
        self.window = self.window_img.get_rect(topleft=(400, 40))
        self.buttons = ButtonGroup()
        idle = prepare.BUTTONS["OK-idle"]
        hover = prepare.BUTTONS["OK-hover"]
        left = self.window.centerx - 64
        top = self.window.bottom - 64
        self.ok_button = Button((left, top), self.buttons, idle_image=idle, hover_image=hover,
                                              call=self.confirm)
                                              
    def confirm(self, *args):
        self.done = True
        self.next = "CITYMAP"
        
    def startup(self, persistent):
        self.persist = persistent
        msgs = self.persist["messages"]
        self.make_labels(msgs)
        
    def make_labels(self, msgs):    
        self.labels = pg.sprite.Group()
        cx = self.window.centerx
        num = len(msgs)
        height = sum((label.rect.height for label in msgs))
        top = self.window.centery - (height // 2)
        for msg in msgs:
            msg.rect.midtop = (self.window.centerx, top)
            self.labels.add(msg)
            top += msg.rect.height
                    
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.buttons.get_event(event)
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        surface.blit(self.window_img, self.window)
        self.labels.draw(surface)
        self.buttons.draw(surface)