#font size of buttons deosn'T MATTER AT THE MOMENT As im going to change the buttons to images (for bottom buttons)

#Make it so that the user can add exercises rather than building it in your self

# on the adding info section get rid of the menu bars


#Retrieve user input and save it in Workouts database on the press of confirm
#Create a database to save inputed info that has not been confirmed by the user just incase they accidentally go of the screen or the app closes
#Take data from Workouts database and display it in records for (defualt displatys current dates and there is an option for the user to select a date and the screen will then only show records correlating to that date
#Take all data from Workouts database and present it on graphs in analysis

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import *
import sqlite3
import datetime
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivymd.uix.picker import MDDatePicker
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.uix.carousel import Carousel
from kivymd.uix.swiper import MDSwiper


class GTracking(AnchorLayout, GridLayout):
    layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
    root = ScrollView(size_hint=(1, 0.80), size=(Window.width, Window.height), pos_hint={'x': 0, 'y': 0.2})
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Make sure the height is such that there is something to scroll.
        self.layout.bind(minimum_height=self.layout.setter('height'))
        Progress()

        self.root.add_widget(self.layout)
        self.add_widget(self.root)


    def Navigation(self, ID):
        self.layout.clear_widgets()
        Plan.NoteSelection_grid.clear_widgets()

        if ID == "progress":
            self.layout.cols = 1
            self.layout.rows = None
            Progress()

        if ID == "record":
            self.layout.cols = 1
            self.layout.rows = 1
            Record()

        if ID == "plan":
            self.layout.cols = 1
            self.layout.rows = None
            Plan()





class Progress(GTracking, ScrollView):
    #Sections
    MuscleSelection = GridLayout(cols = 1, size_hint_y = None, height =100)
    Upper_MuscleSelection = GridLayout(cols = 4, size_hint_y = None, height = 50)
    Lower_MuscleSelection = GridLayout(cols = 3, size_hint_y = None, height = 50)
    ExerciseSelection = GridLayout(cols = 3, size_hint_y = None, height = 50)
    RepSelection = FloatLayout(size_hint_y = None, height = 50)
    PB_AVG = GridLayout(cols = 3, size_hint = (None,None), height = 100)


    #Widgets
    reps = Spinner(text="Number of  reps?", pos_hint = {"x":0.1, "y":0.2}, size_hint = (0.3,0.6))
    Set = Label(text="set", font_size=16, color="black", size_hint = (None,None), width = 100, height = 50)
    PB_label = Label(text = "Personal best:", color = "black", size_hint = (None,None), width = 150, height = 50)
    AVG_label = Label(text = "Average:", color = "black", size_hint = (None,None), width = 150, height = 50)
    SelectedWorkout_Label = Label(text="Choose muscle", color="black")

    #Variables
    MuscleGroup = ""
    Pos = 0
    setnumber= 1
    plotx = []
    ploty1 = []
    ploty2 = []
    Reps = 0
    GraphCarousel = Carousel(direction='right', size_hint_y=None, height=400)

    #Lists
    Exercises = []


    def __init__(self):
        #Clear any previous widgets
        self.MuscleSelection.clear_widgets()
        self.Upper_MuscleSelection.clear_widgets()
        self.Lower_MuscleSelection.clear_widgets()
        self.ExerciseSelection.clear_widgets()
        self.RepSelection.clear_widgets()
        self.PB_AVG.clear_widgets()
        #Muscle group selection buttons
        self.layout.add_widget(self.MuscleSelection)
        self.MuscleSelection.add_widget(self.Upper_MuscleSelection)
        self.MuscleSelection.add_widget(self.Lower_MuscleSelection)
        musclegroups = ["Chest", "Triceps", "Shoulders", "Legs", "Abs", "Back", "Biceps"]
        for muscle in musclegroups:
            if muscle == "Abs" or muscle == "Back" or muscle == "Biceps":
                btn = Button(text=str(muscle), on_release = lambda muscle = muscle:self.InterfaceData(muscle.text))
                self.Lower_MuscleSelection.add_widget(btn)
            else:
                btn = Button(text=str(muscle), on_release = lambda muscle = muscle:self.InterfaceData(muscle.text))
                self.Upper_MuscleSelection.add_widget(btn)

        #Exercise selection (< [] >)
        self.layout.add_widget(self.ExerciseSelection)
        PreviousWorkout_Button = Button(text = "<-", on_press = lambda *args: self.select_workout("backwards", muscle))
        NextWorkout_Button = Button(text = "->", on_press = lambda *args: self.select_workout("forwards", muscle))
        exercise_selection = [PreviousWorkout_Button, self.SelectedWorkout_Label,NextWorkout_Button ]
        for widget in exercise_selection:
            self.ExerciseSelection.add_widget(widget)

        #Reps selection
        self.layout.add_widget(self.RepSelection)
        self.RepSelection.add_widget(self.reps)




    #Obtaining data for widgets from database
    # Occurs after press musclgroup
    def InterfaceData(self,muscle):
        self.reps.values= ""
        self.Exercises = []
        #Lists
        exercises = []
        reps = []

        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM workout WHERE musclegroup = (?) ORDER BY reps', [(muscle)]):
            # Obtain list of exercises in muscle group
            if row[0] in self.Exercises:
                pass
            else:
                self.Exercises.append(row[0])

            # List of inputed reps
            if row[5] in reps:
                pass
            else:
                reps.append(row[5])

        #If nothing is appended from the database then No exercises is added
        if len(self.Exercises) == 0:
            self.Exercises.append("No exercises added")
            print(self.Exercises)


        con.close()
        self.MuscleGroup = muscle

        for rep in reps:
            self.reps.values.append(str(rep))

        self.select_workout(None, muscle)

    #INterchage between workouts
    #Occurs after InterfaceData is called (interface data is retrieved) or if forward/backwards button is pressed
    def select_workout(self, direction, muscle):
        try:
            print("working")
            if "No exercises found!" in self.Exercises :
                pass
            else:
                self.SelectedWorkout_Label.text = self.Exercises[self.Pos]
                self.DisplayInfo()
                if direction == "backwards":
                    try:
                        self.Pos -= 1
                        self.SelectedWorkout_Label.text = self.Exercises[self.Pos]
                        self.DisplayInfo()
                    except:
                        self.Pos = 0
                        self.SelectedWorkout_Label.text = self.Exercises[self.Pos]
                        self.DisplayInfo()
                elif direction == "forwards":
                    try:
                        self.Pos += 1
                        self.SelectedWorkout_Label.text = self.Exercises[self.Pos]
                        self.DisplayInfo()
                    except:
                        self.Pos = 0
                        self.SelectedWorkout_Label.text = self.Exercises[self.Pos]
                        self.DisplayInfo()
        except:
            pass


    def DisplayInfo(self,*args):

        plt.close("all")

        self.layout.remove_widget(self.PB_AVG)
        self.PB_AVG.clear_widgets()
        self.GraphCarousel.clear_widgets()
        self.layout.remove_widget(self.GraphCarousel)



        #set label
        self.PB_AVG.add_widget(self.Set)
        #spacing after set(Two next to set and 1 before PB)
        for label in range(3):
            self.PB_AVG.add_widget(Label())
        #PB and AVG labels
        self.PB_AVG.add_widget(self.PB_label)
        self.PB_AVG.add_widget(self.AVG_label)

        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()



        NumberOfSets = 0
        for row in cur.execute('SELECT * FROM workout WHERE exercise = (?) AND musclegroup = (?) ORDER BY set_num',[(self.SelectedWorkout_Label.text), (self.MuscleGroup)]):
            NumberOfSets = max(NumberOfSets, row[3])

        #Obtains the max number of sets to use in a for loop to collect the data per set for each session the exercise is done
        for i in range(NumberOfSets):
            y_values_Weight = []
            y_values_Reps = []
            x_values = []


            #Retreive data per set
            for row in cur.execute('SELECT * FROM workout WHERE  set_num = (?) ORDER BY date AND set_num',[(i+1)]):
                y_values_Weight.append(row[4])
                y_values_Reps.append(row[5])
                x_values.append(row[1])


            self.ploty1.append(y_values_Weight)
            self.ploty2.append(y_values_Reps)
            self.plotx.append(x_values)

            #Makes the plot unique to each graph
            plt.figure()

            #Create graph (adding data) and add it to carousel 
            plt.plot(self.plotx[i], self.ploty1[i], 'r.-',markersize=14)
            plt.plot(self.plotx[i], self.ploty2[i], 'b.-')
            #Establishes legend for graph
            plt.legend(["Weight", "Rep"])


            plt.ylabel("Weight")
            plt.xlabel("Date")
            plt.title("set: " + str(row[3]))
            self.GraphCarousel.add_widget(FigureCanvasKivyAgg(plt.gcf()))


        self.layout.add_widget(self.GraphCarousel)












class Record(GTracking):
    #Layout
    Layout = FloatLayout(size_hint_y = None)
    PreviousSessionLayout = GridLayout(cols=2, size_hint=(None, None), width=330, pos_hint={"x": 0.1, "y": 0.01})
    #Calander
    CalanderButtonLoad = Button(text="Date?", size_hint=(None, None), width=100, height=50, pos_hint = {"x": 0.1, "y":0.1})
    CalanderButtonADD = Button(text="Date?", size_hint=(None, None), width=100, height=50, pos_hint={"x": 0.1, "y": 0.1})

    WorkoutInput = TextInput(multiline=False, font_size=16, padding_x=20, height=30, width=200, size_hint=(None, None))

    #Variables
    set = 0
    SetInputs = []
    SetsToDelete = []


    #Retrieve data
    DataBase = sqlite3.connect('Workouts.db')
    cursor = DataBase.cursor()
    Values = []
    # Here we will add previously added workouts saved in database
    Values.append("Add workout")

    for row in cursor.execute('SELECT * FROM exercises ORDER BY exercise'):
        # index removes brackets, appostraphies and commas
        Values.append(str(row[0]))

    DataBase.commit()
    DataBase.close()

    def __init__(self):
        #Clear any current widgets
        self.Layout.clear_widgets()

        #Calander widget and function
        self.CalanderButtonLoad.text = "Date?"
        self.CalanderButtonLoad.bind(on_press=self.ShowDatePicker)

        #Add widgets
        self.layout.add_widget(self.Layout)
        self.Layout.add_widget(self.CalanderButtonLoad)


        #designing button as an image
        btn = Button(
                     background_normal='Add_Button.png',
                     background_down='Add_Button.png',
                #Size hint is what cause the image to vary in size and for the hit marker on the button to be small
                #size_hint overides height and width
                     size_hint_y = None,
                     size_hint_x = None,
                     height= 100,
                     width = 120,
                     on_press = self.add,
                     pos_hint = {"x": 0.7, "y":0.1}
                     )
        self.Layout.add_widget(btn)
        self.Layout.add_widget(self.PreviousSessionLayout)

    #Occurs once add button is pressed
    def add(self, *args):
        self.layout.clear_widgets()
        self.forum(None, None, None)

    #Opens popup of calander picker
    #Activated on press date button
    def ShowDatePicker(self, button):
        SelectedDate = MDDatePicker()
        SelectedDate.open()
        SelectedDate.bind(on_save=self.on_save, on_cancel=self.on_cancel)

    #Activated on pressing save on the calander picker
    def on_save(self, instance, value, date_range):
        #Set the chosen date to be the text for the button
        self.CalanderButtonLoad.text = str(value)
        self.CalanderButtonADD.text = str(value)
        self.DisplayPreviousSessions(value)

    def DisplayPreviousSessions(self, date):
        self.PreviousSessionLayout.clear_widgets()
        #If PreviousSessionLayout is not in layout, add it
        try:
            self.Layout.add_widget(self.PreviousSessionLayout)
        except:
            pass
        #To structure previoussession buttons bellow add button and date button
        self.PreviousSessionLayout.add_widget(Label(size_hint_y = None, height =150))
        self.PreviousSessionLayout.add_widget(Label(size_hint_y=None, height=150))

        #open data base
        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()

        #Retrieve and display previous sessions in a button with the exercise and date on the button text
        for row in cur.execute('SELECT * FROM workout WHERE date = (?) ORDER BY set_num', [(date)]):
            #Get only one bit of data for a recorded session
            if row[3] == 1:
                name = row[0]
                #Lambda passes in different buttons created in the loop not variables
                session = Button(text= str(row[0]),
                                     color="black", font_size=16, height=50, width=320, size_hint=(None, None),
                                     on_press=lambda row = row: self.Load(row.text, date))
                #Need to pass a variable in lamdbda for the button and the variable that changes with the for loop
                delete = Button(text="X", color="black", on_press=lambda row = row, name=name:self.DeleteWorkout(name,date), size_hint=(None, None),height=50, width=50)
                self.PreviousSessionLayout.add_widget(session)
                self.PreviousSessionLayout.add_widget(delete)


        # Save (commit) the changes
        con.commit()
        con.close()

    def Load(self,name,date):
        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()
        #Retrieve data for selected session
        cur.execute('SELECT * FROM workout WHERE date = (?) AND exercise = (?)', [(str(date)),(str(name))])
        data = []
        for i in cur.fetchall():
            for element in i:
                data.append(element)
        self.forum(data, name, date)

    #Does nothing as calander closes anyway
    def on_cancel(self, instance, value):
        pass

    def DeleteWorkout(self, name, date):
        con=sqlite3.connect('Workouts.db')
        cur = con.cursor()
        cur.execute("DELETE FROM workout where exercise = (?) AND date = (?)", [(name), (date)])
        con.commit()
        con.close()
        self.DisplayPreviousSessions(date)


    def SaveChanges(self,name,date):
        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()
        Info = []
        Data = []
        UpdatededRecrods = []
        workout = ""
        set_num = 0

        #Retrieve data (sets)
        for set in (self.SetInputs):
            for input in set:
                if isinstance(input, TextInput):
                    Info.append(input.text)


        #Retrieve all data 
        for child in reversed(self.layout.children):
            if isinstance(child,Spinner):
                Data.append(child.text)
            if isinstance(child,TextInput):
                Data.append(child.text)
        Data.append(self.CalanderButtonADD.text)

        #Obtain updated info
        set_num = 0
        for element in range(0, len(Info),2):
            set_num+=1
            try:
                UpdatededRecrods.append((Data[0], self.CalanderButtonADD.text, Data[len(Data)-2],int(set_num),int(Info[element]), int(Info[element +1]),Data[1]))
            #If an integer was not enter in the weight and reps inputboxes then show a popup to notify the user
            except ValueError:
                Factory.IncorrectDataTypePopup().open()
                return False

        #Delete the previous Record
        cur.execute("DELETE FROM workout where exercise = (?) AND date = (?)", [(name), (date)])
        for Record in UpdatededRecrods:
            print(Record)
            cur.execute("INSERT INTO workout VALUES (?,?,?,?,?,?,?)", Record)

        con.commit()
        con.close()
        self.ReturnAfterSave(self.CalanderButtonADD.text)

    def forum(self,data, name, date):
        self.layout.clear_widgets()
        self.SetInputs = []
        self.set = 0

        #Reset date button
        self.CalanderButtonADD.text = "Date?"

        #widgets
        WorkoutLabel = Label(text="                     Workout:", color="black", font_size=20, size_hint=(None, None),height=40, width=150)
        WorkoutInput_DropDownList= Spinner(values=self.Values, size_hint=(None, None), height=30, width=200)
        MuscleGroup = Spinner(text="Muscle group",values=('Chest', 'Triceps', 'Shoulders', 'Legs', 'Abs', 'Back', 'Biceps'),size_hint=(None, None), height=30, width=200)
        DateLabel = Label(text="                          Date:", color="black", font_size=20, size_hint=(None, None),height=40, width=150)

        NotesInput = TextInput(size_hint=(None, None), height=80, width=200)
        NoteLabel = Label(text="              Notes:", color="black", font_size=16, size_hint=(None, None), height=40,width=150)

        RemoveButton = Button(text=" Remove set", color="black", size_hint=(None, None), height=40, width=150,on_release=self.remove_set)
        Add_Set = Button(text=" Add set", color="black", size_hint=(None, None), height=40, width=150,on_release= lambda data = None:self.add_set(None))

        ConfirmButton = Button(text="Confirm", color="black", on_release= lambda *args:self.SaveForum(WorkoutInput_DropDownList.text, MuscleGroup.text, NotesInput.text),size_hint=(None, None), height=50, width=200)
        Blank_label = Label()
        save = Button(text="Save", color="black", on_release =lambda *args: self.SaveChanges(name,date), size_hint=(None, None), height=50, width=200)


        if data != None:
            #Input all data into forum
            total =len(data)
            WorkoutInput_DropDownList.text = data[0]
            self.CalanderButtonADD.text = data[1]
            NotesInput.text = data[2]
            MuscleGroup.text = data[total- 1]
            #Retrieve set data
            SetData = []
            for set in range(3,total,7):
                if data[set] != data[total-1]:
                    SetData.append([data[set], data[set + 1], data[set + 2]])
            #Load forum widgets
            ListOfWidgets_ADD = [WorkoutLabel, WorkoutInput_DropDownList, MuscleGroup, DateLabel,self.CalanderButtonADD, RemoveButton, Add_Set, NoteLabel, NotesInput,Blank_label, save]
        else:
            ListOfWidgets_ADD = [WorkoutLabel, WorkoutInput_DropDownList, MuscleGroup, DateLabel,self.CalanderButtonADD, RemoveButton, Add_Set, NoteLabel, NotesInput, ConfirmButton]

        #Binds
        WorkoutInput_DropDownList.bind(text=self.show_selected_value)
        self.CalanderButtonADD.bind(on_press=self.ShowDatePicker)

        #Structure of layout
        GTracking.layout.cols = 2
        self.layout.rows = None
        self.layout.spacing = 30

        #Labels for positioning of widgets
        for i in range(2):
            lbl = Label()
            self.layout.add_widget(lbl)



        for widget in ListOfWidgets_ADD:
            if widget == MuscleGroup :
                self.layout.add_widget(Label())
                self.layout.add_widget(widget)
            elif widget == ConfirmButton:
                self.layout.add_widget(Label(size_hint_y =None, width =  50))
                self.layout.add_widget(widget)
            else:
                self.layout.add_widget(widget)

        if data != None:
            for set in SetData:
                self.add_set(set)

    def SaveForum(self, WorkoutInput, MuscleGroupInput, NotesInput):
        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()

        Info = []
        Record = []

        set_num = 0



        #Missing info errors and corrections
        #Displays popup notifying user to enter missing info
        if self.WorkoutInput.text == "" and WorkoutInput == "":
            Factory.MissingValuesExercisePopup().open()
        elif len(self.SetInputs) == 0:
            Factory.MissingValuesSetPopup().open()
        elif self.CalanderButtonADD.text == "Date?":
            Factory.MissingValuesSetPopup().open()
        elif MuscleGroupInput == "Muscle group":
            Factory.MissingValuesMuscleGroupPopup().open()

        #If all info is entered
        else:
            #If there is a blank space it automatically become 0
            for set in (self.SetInputs):
                for input in set:
                    if isinstance(input, TextInput):
                        if input.text == "":
                            input.text = "0"

            # Gets weight and rep inputs for sets
            for set in (self.SetInputs):
                for input in set:
                    if isinstance(input, TextInput):
                        try:
                            Info.append(int(input.text))
                        # If an integer was not enter in the weight and reps inputboxes then show a popup to notify the user
                        except ValueError:
                            Factory.IncorrectDataTypePopup().open()
                            return False

            #In case of a new exercise being added
            if WorkoutInput == 'Add workout':
                for pos in range(0, len(Info), 2):
                    set_num += 1
                    Record.append((str(self.ManageDuplicates(None)), self.CalanderButtonADD.text, str(NotesInput), str(set_num), Info[pos],Info[pos + 1], str(MuscleGroupInput)))
                    #Add values to workout table
                    cur.executemany("INSERT INTO workout VALUES (?,?,?,?,?,?,?)", Record)
                    #Add new exercise to exercises table
                    cur.execute("INSERT INTO exercises VALUES (?)",[(self.WorkoutInput.text)])


            else:
                #Get the Weight Input and RepInput for each set and append it to Info list
                #Could just use this to add records
                for pos in range(0,len(Info),2):
                    set_num +=1
                    Record.append((str(self.ManageDuplicates(WorkoutInput)), self.CalanderButtonADD.text,str(NotesInput), str(set_num),Info[pos],Info[pos+1], str(MuscleGroupInput)))
                cur.executemany("INSERT INTO workout VALUES (?,?,?,?,?,?,?)",Record)
            con.commit()
            con.close
            self.ReturnAfterSave(self.CalanderButtonADD.text)


    #Checks database table for duplicate exercises on that date
    #Gives the saved exercise a number
    def ManageDuplicates(self, typed):
        if typed == None:
            workout = self.WorkoutInput.text
        else:
            workout = typed

        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()
        exercises = []

        highest = 0

        # Retrieve all the exercise names that have been added for that date
        for exercise in cur.execute('SELECT * FROM workout WHERE date = (?) AND set_num = (?) ORDER BY exercise',
                                    [(self.CalanderButtonADD.text), (1)]):
            name = exercise[0]

            #Loactes number in name
            for character in name:
                if character == "(":
                    FirstBracket = name.index(character)
                if character == ")":
                    SecondBracket = name.index(character)

            #numbers are compared to find the highest; indicating how many duplicates there are
            value = int(name[FirstBracket+1:SecondBracket  :])
            print(str(value) + " " + str(highest))

            #Compares number to find the highest
            #Indicating how many duplicates there are
            if value > highest:
                highest = value

        try:
            #Add one to accommodate for the one being added now by the user
            workout = workout + "(" + str(highest +1) + ")"
        # If there is no duplicates currently in table then there will be an error as duplicates is not referenced
        # So duplicates is assigend 0 and 2 is added to give the (2) to the second one
        except:
            duplicates = 0
            workout = workout + "(" + str(duplicates + 2) + ")"


        con.close()
        return workout

    def ReturnAfterSave(self, date):
        # Clear any current widgets
        self.layout.clear_widgets()
        self.Layout.clear_widgets()

        # Calander widget and function
        self.CalanderButtonLoad.text = date
        self.CalanderButtonLoad.bind(on_press=self.ShowDatePicker)

        # Add widgets
        self.layout.add_widget(self.Layout)
        self.Layout.add_widget(self.CalanderButtonLoad)

        # designing button as an image
        btn = Button(
            background_normal='Add_Button.png',
            background_down='Add_Button.png',
            # Size hint is what cause the image to vary in size and for the hit marker on the button to be small
            # size_hint overides height and width
            size_hint_y=None,
            size_hint_x=None,
            height=100,
            width=120,
            on_press=self.add,
            pos_hint={"x": 0.7, "y": 0.1}
        )
        self.Layout.add_widget(btn)
        self.DisplayPreviousSessions(date)



    def add_set(self, data):

        self.set += 1

        #SetInput widgets to be added
        SetLabel = Label(text="Set " + str(self.set) + ")", color="black")
        Label1 = Label()
        WeightLabel = Label(text="                 Weight:", color="black")
        RepLabel = Label(text="                    Reps:", color="black")
        WeightInput = TextInput(multiline=False, font_size=16, padding_x=20, height=30, width=75,size_hint=(None, None))
        RepInput = TextInput(multiline=False, font_size=16, padding_x=20, height=30, width=75,size_hint=(None, None))
        #append next set of SetInputs to a list of tuples
        self.SetInputs.append((SetLabel,Label1,WeightLabel,WeightInput,RepLabel,RepInput))

        #Remove widgets in layout
        widgets = []
        for widget in reversed(self.layout.children):
            widgets.append(widget)
            self.layout.remove_widget(widget)

        #Add widgets before and including CalanderButton then add SetInputs and finally add the remaining widgets
        for widget in widgets:
            if widget == self.CalanderButtonADD:
                self.layout.add_widget(widget)
                #Add all SetInputs
                for input in self.SetInputs:
                    for child in input:
                        self.layout.add_widget(child)
            else:
                try:
                    self.layout.add_widget(widget)
                except:
                    pass

        if data != None:
            SetLabel.text = "Set " + str(data[0])
            WeightInput.text = str(data[1])
            RepInput.text = str(data[2])


    def remove_set(self, *args):
        #Try and except incase user accidentally tries to remove a set without a set being present ]
        try:
            #removes the last SetInputs added and returns them as a tuple
            removed = self.SetInputs.pop()
            #Looks for removed SetInputs in layout and removes them
            for child in reversed(self.layout.children):
                if child in removed:
                    self.layout.remove_widget(child)

            #lists of sets to delete from table
            #If table doesn't have set then it will pass on deleting it
            self.SetsToDelete.append(self.set)

            self.set -= 1
        except:
            pass
        print(self.SetsToDelete)

    #Activated once an option in the workout dropdown list has been selected
    def show_selected_value(self, spinner, text):
        #Input box is cleared so it is ready for user input if neccassary
        self.WorkoutInput.text = ""

        #Dropdwon list is replaced with an inputbox for the user to enter a new workout
        if text == 'Add workout':
            children = []
            #Removes all widgets currently in layout
            #Puts them in a list (addin the TextInput in desired position
            #Add widgets in list onto layout
            for child in reversed(self.layout.children):
                children.append(child)
            self.layout.clear_widgets()
            for child in children:
                if child == spinner:
                    self.layout.add_widget(self.WorkoutInput)
                else:
                    self.layout.add_widget(child)



class Plan(GTracking):
    #Layouts
    AddNote_layout = GridLayout(cols = 3, size_hint_y = None, height = 50)
    PreviousNotes_layout = GridLayout(cols =4, size_hint_y = None, height =300)
    NoteSelection_grid = GridLayout(cols = 3, size_hint_y = None, height = 50)
    Label_grid = GridLayout(cols=1, size_hint_y=None, height=350)
    save_grid = GridLayout(cols=4, size_hint_y=None, height=50)

    NoteName = TextInput(size_hint = (None,None), width = 200, height = 50, multiline = False)
    max_characters = 15


    NotesInput = TextInput(size_hint_y = None, height =350)



    Current_name = ""

    notes = []
    Pos = 0

    con = sqlite3.connect('Workouts.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Notes'):
        notes.append(row[0])
        print(row[0])

    con.commit()
    con.close()
    def __init__(self):
        self.AddNote_layout.clear_widgets()
        self.layout.clear_widgets()
        self.layout.add_widget(self.AddNote_layout)
        self.PreviousNotes_layout.clear_widgets()

        for i in range(2):
            lbl = Label()
            self.AddNote_layout.add_widget(lbl)
        NoteBtn = Button(
            background_normal='Add_Button.png',
            background_down='Add_Button.png',
            # Size hint is what cause the image to vary in size and for the hit marker on the button to be small
            # size_hint overides height and width
            size_hint_y=None,
            size_hint_x=None,
            height=100,
            width=120,
            on_release=self.AddNote
        )
        self.AddNote_layout.add_widget(NoteBtn)
        self.layout.add_widget(self.PreviousNotes_layout)

        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()
        phase = "load"
        for row in cur.execute('SELECT * FROM Notes'):
            name = str(row[0])
            self.PreviousNotes_layout.add_widget(Button(text = str(row[0]), size_hint= (None, None), width = 150, height = 70, on_press = lambda name=name: self.LoadNote(name, phase)))
            self.PreviousNotes_layout.add_widget(Label(size_hint = (None,None), width = 100))
        con.commit()
        con.close()
    def LoadNote(self, name, phase):
        #Clear previous content
        self.PreviousNotes_layout.clear_widgets()
        self.Label_grid.clear_widgets()
        self.NoteSelection_grid.clear_widgets()
        self.layout.clear_widgets()
        self.save_grid.clear_widgets()

        self.Pos = self.notes.index(name.text)
        self.AddNote_layout.clear_widgets()
        left = Button(text="<-", on_press=lambda *args: self.note("backwards"))
        right = Button(text="->", on_press=lambda *args: self.note("forwards"))
        self.NoteSelection_grid.add_widget(left)
        self.NoteSelection_grid.add_widget(self.NoteName)
        self.NoteSelection_grid.add_widget((right))
        self.layout.add_widget(self.NoteSelection_grid)

        self.NoteName.bind(text=lambda *args: self.insert_text())

        self.Label_grid.add_widget(self.NotesInput)
        self.layout.add_widget(self.Label_grid)

        self.save_grid.cols = 4
        self.save_grid.add_widget(Label())
        DeleteNote_button = Button(text="Delete", size_hint=(None, None), width=100, height=50, on_press= Factory.PopupContent().open)
        self.save_grid.add_widget(DeleteNote_button)
        phase = "load"
        SaveNote_button = Button(text="Save", size_hint=(None, None), width=100, height=50, on_press=lambda *args: self.save(phase))
        self.save_grid.add_widget(SaveNote_button)
        self.save_grid.add_widget(Label())
        self.layout.add_widget(self.save_grid)
        self.display(name.text)

    def AddNote(self, *args):
        # Clear previous content
        self.layout.clear_widgets()
        self.PreviousNotes_layout.clear_widgets()
        self.Label_grid.clear_widgets()
        self.NoteSelection_grid.clear_widgets()
        self.save_grid.clear_widgets()
        self.AddNote_layout.clear_widgets()

        #Clear any previous inputs
        self.NoteName.text = ""
        self.NotesInput.text = ""

        #structuring labels
        left = Label()
        right = Label()

        #widgets for choosing between notes
        self.NoteSelection_grid.add_widget(left)
        self.NoteSelection_grid.add_widget(self.NoteName)
        self.NoteSelection_grid.add_widget((right))
        self.layout.add_widget(self.NoteSelection_grid)

        #Ensures number of characters for note name doesn't exeed limit to where its too many
        self.NoteName.bind(text=lambda *args: self.insert_text())

        self.Label_grid.add_widget(self.NotesInput)
        self.layout.add_widget(self.Label_grid)

        self.save_grid.cols = 3
        self.save_grid.add_widget(Label())
        phase = "Create new"
        SaveNote_button = Button(text="Save", size_hint=(None, None), width=100, height=50, on_press= lambda *args: self.save(phase))
        self.save_grid.add_widget(SaveNote_button)
        self.save_grid.add_widget(Label())
        self.layout.add_widget(self.save_grid)

    #Prevents number of characters in textinput for note name to exeed max_characters
    def insert_text(self):
        #Limint number of characters in textinput to max_character
        if len(self.NoteName.text) > self.max_characters:
            input = []
            for char in self.NoteName.text:
                input.append(char)
            input.pop()
            self.NoteName.text = ""
            for char in input:
                self.NoteName.text = self.NoteName.text + str(char)

    #Saves note
    def save(self, phase):
        print(phase)
        print(self.notes)
        #If the user is trying to add a note and they are using a name of a note already used then they will be told in the textinput box that the name is already taken
        if (self.NoteName.text in self.notes or self.NoteName.text == "Name already used") and phase == "Create New":
            self.max_characters = 30
            self.NoteName.text = "Name already used"
            self.NoteName.foreground_color ="red"
        #If a name hasn't been entered
        elif self.NoteName.text == "":
            self.NoteName.text = "Enter a name"
            self.NoteName.foreground_color = "red"
        #If there are not issues with the name
        elif phase == "Create new":
            con = sqlite3.connect('Workouts.db')
            cur = con.cursor()
            #save inputs
            cur.execute('INSERT INTO Notes Values (?,?)', [(self.NoteName.text), (self.NotesInput.text)])

            self.notes.append(self.NoteName.text)

            con.commit()
            con.close()

            Plan()

        #saves note loaded
        elif phase == "load":
            con = sqlite3.connect('Workouts.db')
            cur = con.cursor()
            #Update note
            cur.execute('UPDATE Notes SET name = (?) WHERE name = (?)', [(self.NoteName.text),(self.Current_name)])
            con.commit()
            con.close()

            con = sqlite3.connect('Workouts.db')
            cur = con.cursor()
            cur.execute('UPDATE Notes SET notes = (?) WHERE name = (?)',[(self.NotesInput.text), (self.NoteName.text)])
            con.commit()

            #refresh list of notes
            self.notes = []
            for row in cur.execute('SELECT * FROM Notes'):
                self.notes.append(row[0])

            con.close()
            Plan()


    #delete note
    def delete(self):
        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()
        cur.execute('DELETE FROM Notes WHERE name = (?)', [(self.NoteName.text)])
        con.commit()
        con.close()
        Plan()

    #Alternate between notes using left and right buttons
    def note(self, direction):
        if direction == "backwards":
            try:
                self.Pos -= 1
                self.NoteName.text = self.notes[self.Pos]
                self.display(self.NoteName.text)
            except:
                self.Pos = 0
                self.NoteName.text = self.notes[self.Pos]
                self.display(self.NoteName.text)
        elif direction == "forwards":
            try:
                self.Pos += 1
                self.NoteName.text = self.notes[self.Pos]
                self.display(self.NoteName.text)
            except:
                self.Pos = 0
                self.NoteName.text = self.notes[self.Pos]
                self.display(self.NoteName.text)

    #Showcase info on widgets
    def display(self, name):
        con = sqlite3.connect('Workouts.db')
        cur = con.cursor()
        for row in cur.execute("""SELECT * FROM Notes WHERE name = (?)""", [(name)]):
            self.NoteName.text = row[0]
            self.NotesInput.text = row[1]
        con.commit()
        con.close()
        self.Current_name = self.NoteName.text

#app class
class TrackingApp(MDApp):
    def build(self):
        return GTracking()

if __name__ == "__main__":
    TrackingApp().run()
