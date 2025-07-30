   def on_role_hover_enter(self, event, role):
        event.widget.config(image=self.role_photos[role]['hover'])

    def on_role_hover_leave(self, event, role):
        event.widget.config(image=self.role_photos[role]['normal'])