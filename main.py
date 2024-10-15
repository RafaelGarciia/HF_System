from Source import window, frames


app = window.Window()
app.active_frame = frames.Company_registration_screen(app)
app.show_frame()
app.mainloop()