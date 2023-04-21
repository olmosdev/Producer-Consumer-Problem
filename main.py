import time
import random
import threading
from tkinter import *
from tkinter import messagebox as MessageBox

# To center the window on the screen (This is a little Mixin)
class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (w/2))
        y = int((hs/2) - (h/2))
        self.geometry(f"{w}x{h}+{x}+{y}")  

# Generating the main screen
class MainWidow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Program 3 - Producer-Consumer problem")
        self.resizable(0, 0) 
        self.geometry("1000x600")
        self.config(relief="sunken", bd=10)
        self.center()
        self.Build()
        self.bind("<Escape>", lambda something: self.FinishProgram(something))

    # Creating interfaces
    def Build(self):
        # To contain other widgets
        mainFrame = Frame(self)
        mainFrame.grid(row=0, column=0)

        # Producer area
        producerFrame = Frame(mainFrame)
        producerFrame.grid(row=0, column=0)
        producerFrame.config(padx=20, pady=20)

        titleOfProducer = Label(producerFrame, text="SpongeBob")
        titleOfProducer.grid(row=0, column=0)
        titleOfProducer.config(justify="center")
        titleOfProducer.config(font=("Verdana", 15))

        self.bobEsponja = PhotoImage(file="./Assets/BobEsponja.png")
        imageOfProducer = Label(producerFrame, image=self.bobEsponja)
        imageOfProducer.grid(row=1, column=0)
        """If you want a border, the option is borderwidth. You can also choose the relief of the border:
        "flat", "raised", "sunken", "ridge", "solid", and "groove"."""
        imageOfProducer.config(width=258, height=195, relief="solid", borderwidth=3)

        self.infoProducer = Label(producerFrame, text="Sleeping")
        self.infoProducer.grid(row=2, column=0, sticky="ew")
        self.infoProducer.config(background="red", padx=2, pady=2)

        # Space area
        spaceAreaFrame = Frame(mainFrame)
        spaceAreaFrame.grid(row=0, column=1)
        spaceAreaFrame.config(padx=150, pady=20)

        self.startButton = Button(spaceAreaFrame, text="Start", command=self.Execute)
        self.startButton.grid(row=0, column=0)
        self.startButton.config(background="lightpink", font=("Verdana", 15), relief="groove")

        # Consumer area
        consumerFrame = Frame(mainFrame)
        consumerFrame.grid(row=0, column=2)
        consumerFrame.config(padx=20, pady=20)

        titleOfConsumer = Label(consumerFrame, text="Bubble Bass")
        titleOfConsumer.grid(row=0, column=0)
        titleOfConsumer.config(justify="center")
        titleOfConsumer.config(font=("Verdana", 15))

        self.robaloBurbuja = PhotoImage(file="./Assets/RobaloBurbuja.png")
        imageOfConsumer = Label(consumerFrame, image=self.robaloBurbuja)
        imageOfConsumer.grid(row=1, column=0)
        imageOfConsumer.config(width=258, height=195, relief="solid", borderwidth=3)

        self.infoConsumer = Label(consumerFrame, text="Sleeping")
        self.infoConsumer.grid(row=2, column=0, sticky="ew")
        self.infoConsumer.config(background="red", padx=2, pady=2)

        # Container area
        countainerFrame = Frame(mainFrame)
        countainerFrame.grid(row=1, column=0, columnspan=3)
        countainerFrame.config(padx=20, pady=20)

        titleOfContainer = Label(countainerFrame, text="Food container")
        titleOfContainer.grid(row=0, column=0, sticky="ew")
        titleOfContainer.config(font=("Verdana", 15), justify="center")

        self.foodContainer = Frame(countainerFrame)
        self.foodContainer.grid(row=1, column=0, sticky="ew")
        self.foodContainer.config(background="lightpink", padx=20, pady=20)

        # Generating labels dinamically
        self.allLabels = []
        for row in range(2):
            for column in range(10):
                self.allLabels.append(KrabbyPatty(row, column, self.foodContainer))

    def FinishProgram(self, something):
        # Resetting buffer positions
        FoodTable.head = 0
        FoodTable.tail = 0

        # Stopping the threads
        self.producer.Cancel()
        self.consumer.Cancel()

        # Clearing everything on screen
        for label in self.allLabels:
            label.label.config(width=10, height=5, image="")

        self.infoProducer["text"] = "Sleeping"
        self.infoProducer.config(background="red", padx=2, pady=2)
        self.infoConsumer["text"] = "Sleeping"
        self.infoConsumer.config(background="red", padx=2, pady=2)

        # Notifying the user
        MessageBox.showinfo("Notification", "The program was finished.")

        # Unlocking the Start Button
        self.startButton.config(state="normal")

    def Execute(self):
        # Blocking the Start Button
        self.startButton.config(state="disabled")

        # To know who is going to start (Producer or Consumer)
        decision = random.randrange(0,2)

        if decision == 0:
            self.producerSemaphore = threading.Semaphore(1)
            self.consumerSemaphore = threading.Semaphore(0)
        else:
            self.producerSemaphore = threading.Semaphore(0)
            self.consumerSemaphore = threading.Semaphore(1)

        # Initializing the food container (resource to be used)
        FoodTable(self.allLabels)

        # Preparing the producer and consumer
        self.producer = SpongeBob(self.producerSemaphore, self.consumerSemaphore, self.infoProducer, self.infoConsumer)
        self.consumer = BubbleBass(self.producerSemaphore, self.consumerSemaphore, self.infoProducer, self.infoConsumer)
        # Creating threads
        self.producerThread = threading.Thread(target=self.producer.ProduceKrabbyPatties)
        self.producerThread.start()
        self.consumerThread = threading.Thread(target=self.consumer.ConsumeKrabbyPatties)
        self.consumerThread.start()

# Class to create labels and handle their own states (appareance by screen)
class KrabbyPatty(Tk):
    def __init__(self, row, column, where):
        self.label = Label(where)
        self.label.config(width=10, height=5, background="lightgray", relief="groove", borderwidth=7)
        self.label.grid(row=row, column=column)
        self.isKrabbyPatty = False

    # To be a simple Krabby Patty
    def ChangeApparence(self):
        self.krabbyPatty = PhotoImage(file="./Assets/Krabby-Patty.png")
        self.krabbyPatty = self.krabbyPatty.subsample(5)
        self.label.config(image=self.krabbyPatty, width=71, height=76)
        self.isKrabbyPatty = True

    # To be a simple empty label
    def OriginalChange(self):
        self.label.config(width=10, height=5, image="")
        self.isKrabbyPatty = False

# To manage the buffer (resource area)
class FoodTable:
    # Handling buffer positions to handle inserts and deletes
    head = 0
    tail = 0

    def __init__(self, buffer):
        FoodTable.buffer = buffer

    # To add something in the share area (food container)
    def AddKrabbyPatty():
        if FoodTable.head == 20:
            FoodTable.head = 0
        FoodTable.buffer[FoodTable.head].ChangeApparence()
        
        FoodTable.head += 1

    # To delete something in the share area (food container)
    def EatKrabbyPatty():
        if FoodTable.tail == 20:
            FoodTable.tail = 0
            
        FoodTable.buffer[FoodTable.tail].OriginalChange()

        FoodTable.tail += 1

    # To count the number of available Krabby Patties there are
    def GetNumberOfKrabbyPatties():
        counter = 0

        for krabbyPatty in FoodTable.buffer:
            if krabbyPatty.isKrabbyPatty == True:
                counter += 1
        return counter  

# Producer class
class SpongeBob:
    def __init__(self, producerSemaphore, consumerSemaphore, infoProducer, infoConsumer):
        self.producerSemaphore = producerSemaphore
        self.consumerSemaphore = consumerSemaphore
        self.infoProducer = infoProducer
        self.infoConsumer = infoConsumer
        self.cancelThis = False

    # Primary producer action
    def ProduceKrabbyPatties(self):
        # To keep working the thread
        while True:
            # Request to access the resource
            self.producerSemaphore.acquire()
            # To know how long the producer will work
            numberOfKrabbyPatties = random.randrange(1,20)

            signal = True # To handle inserts
            counter = 0 # To count seconds
            
            # To display the current states on screen
            self.infoProducer["text"] = "Acting"
            self.infoProducer.config(background="green", padx=2, pady=2)
            self.infoConsumer["text"] = "Sleeping"
            self.infoConsumer.config(background="red", padx=2, pady=2)
            
            # To make insertions while there is opportunity
            while FoodTable.GetNumberOfKrabbyPatties() <= 20 and signal:   
                FoodTable.AddKrabbyPatty()
                counter += 1
                time.sleep(1)

                # To finish the current thread when the user press the ESC key
                if self.cancelThis:
                    return 

                # When all the elements have been placed, the role is changed
                if counter == numberOfKrabbyPatties:
                    signal = False
                    self.consumerSemaphore.release()
                    break
                
                # To change the role when there is no longer an opportunity to add something
                if FoodTable.GetNumberOfKrabbyPatties() == 20:
                    self.infoProducer["text"] = "Trying"
                    self.infoProducer.config(background="orange", padx=2, pady=2)
                    time.sleep(1)
                    signal = False
                    self.consumerSemaphore.release()
                    break

    # To finish the current thread        
    def Cancel(self):
        self.cancelThis = True
            

class BubbleBass:
    def __init__(self, producerSemaphore, consumerSemaphore, infoProducer, infoConsumer):
        self.producerSemaphore = producerSemaphore
        self.consumerSemaphore = consumerSemaphore
        self.infoProducer = infoProducer
        self.infoConsumer = infoConsumer
        self.cancelThis = False

    def ConsumeKrabbyPatties(self):
        # To keep working the thread
        while True:
            # Request to access the resource
            self.consumerSemaphore.acquire()
            # To know how long the consumer will work
            numberOfKrabbyPatties = random.randrange(1,20)

            signal = True # To handle inserts
            counter = 0 # To count seconds

            # This is a simple validation when the consumer is the first person to modify the resources area 
            # And there is nothing to take
            if FoodTable.GetNumberOfKrabbyPatties() == 0:
                time.sleep(1)
                self.producerSemaphore.release()
            else:
                # To display the current states on screen
                self.infoConsumer["text"] = "Acting"
                self.infoConsumer.config(background="green", padx=2, pady=2)
                self.infoProducer["text"] = "Sleeping"
                self.infoProducer.config(background="red", padx=2, pady=2)

                # To make extractions while there is opportunity
                while FoodTable.GetNumberOfKrabbyPatties() > 0 and signal: 
                    FoodTable.EatKrabbyPatty()
                    counter += 1
                    time.sleep(1)

                    # To finish the current thread when the user press the ESC key
                    if self.cancelThis:
                        return 

                    # When all the elements have been taken, the role is changed
                    if counter == numberOfKrabbyPatties:
                        signal = False
                        self.producerSemaphore.release()
                        break
                    
                    # To change the role when there is no longer an opportunity to take something
                    if FoodTable.GetNumberOfKrabbyPatties() == 0:
                        self.infoConsumer["text"] = "Trying"
                        self.infoConsumer.config(background="orange", padx=2, pady=2)
                        time.sleep(1)
                        self.producerSemaphore.release()
                        break   
    
    # To finish the current thread  
    def Cancel(self):
        self.cancelThis = True  

# Running everything
if __name__ == "__main__":
    app = MainWidow()
    app.mainloop()


    