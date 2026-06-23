import time, winsound, threading 
import tkinter as tk

running = False
thread = None
start_time = None

def update_timer():
    if running and start_time is not None:
        elapsed = int(time.time() - start_time)

        minutes = elapsed // 60
        seconds = elapsed % 60

        status_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        root.after(1000, update_timer)

def wait_with_stop(seconds):
    global running

    for _ in range(seconds):
        if not running:
            return False
        time.sleep(1)

    return True

def pausing():

    winsound.Beep(500, 1000)
    
    return wait_with_stop(300)

def long_pause():

    winsound.Beep(300, 400)
    winsound.Beep(400, 400)
    winsound.Beep(500, 400)
    winsound.Beep(600, 400)
    winsound.Beep(500, 200)
    winsound.Beep(600, 200)
    winsound.Beep(500, 400)
    winsound.Beep(600, 1000)
    return wait_with_stop(900)

def start_again():
    winsound.Beep(523, 180)   
    winsound.Beep(659, 180)   
    winsound.Beep(784, 300)    

def pomodoro_cycle():
    global running

    count = 0

    while running:
        
        if not wait_with_stop(1500):
            break

        count += 1

        if count % 4 == 0:
            if not long_pause():
                break
        else:
            if not pausing():
                break

        if running:
            start_again()

    running = False        
        
def start_program():
    global running, thread, start_time

    winsound.Beep(3000, 100)
    winsound.Beep(3000, 100)
    winsound.Beep(3000, 100)

    start_time = time.time()

    if not running:
        running = True
        thread = threading.Thread(target=pomodoro_cycle, daemon=True)
        thread.start()
        status_label.config(text="Cycle started!", fg="green")

    update_timer()    

def stop_program():
    global running, thread, start_time

    start_time = None
    running = False

    if thread is not None:
        thread.join(timeout=2)

    status_label.config(text="Cycle stopped!", fg="red")        


# ------- GUI --------

root = tk.Tk()
root.title("Pomodoro Beeper")
root.geometry("200x200")

status_label = tk.Label(root, text="Ready", font=("Arial", 12))
status_label.pack(pady=20)

btn_start   = tk.Button(root,
                        text="Start Cycle",
                        font=("Arial", 12, "bold"),
                        bg="#4CAF50",
                        fg="white",
                        width=10,
                        height=1,
                        command=start_program)
btn_start.pack(pady=10)

btn_stop = tk.Button(root,
                     text="Stop Cycle",
                     font=("Arial", 12, "bold"),
                     bg="#f44336",
                     fg="white",
                     width=10,
                     height=1,
                     command=stop_program)
btn_stop.pack(pady=10)

root.mainloop()

