import requests
import tkinter as tk
import webbrowser as wb


#Gets Info from API website
response = requests.get("http://api.covid19api.com/summary")
r = response.json()


#Parent app class, used to intialize some variables.
class App:
    #__init__ method, initalizing variables. Try not to change variables or risk bricking the script.
    def __init__(self, root):
        self.root = root
        self.url = "https://en.wikipedia.org/wiki/COVID-19"
        self.new = 1
        self.url2 = "https://api.covid19api.com/summary"
        self.new2 = 2

#Child class to display and process info in tkinter window.
class API_Harvest(App):
    # __init__ method, initializing variables. Try not to change variables or risk bricking the script.
    def __init__(self, root):
        super(API_Harvest, self).__init__(root)
        self.country_entry = tk.Entry(window, width=10)
        self.country_entry.grid(row=0, column=0)
        self.search_button = tk.Button(window, text="Search", command=self.get_countries)
        self.search_button.grid(row=0, column=1)
        self.country = tk.Label(window, text='', font=("Comic Sans", 30), bg=("#c91010"))
        self.country.grid(row=1)
        self.confirmed = tk.Label(window, text='', font=("Comic Sans", 20), bg=("#ff0000"))
        self.confirmed.grid(row=2)
        self.deaths = tk.Label(window, text='', font=("Comic Sans", 20), bg=("#ff0000"))
        self.deaths.grid(row=3)
        self.new_confirmed = tk.Label(window, text='', font=("Comic Sans", 20), bg=("#ff0000"))
        self.new_confirmed.grid(row=4)
        self.new_recovered = tk.Label(window, text='', font=("Comic Sans", 20), bg=("#ff0000"))
        self.new_recovered.grid(row=5)
        self.button = tk.Button(window, text="COVID-19 Info", command=self.open_wikipedia)
        self.button.grid(row=6)
        self.button1 = tk.Button(window, text="COVID-19 API Source", command=self.open_api_source)
        self.button1.grid(row=7)
        self.legend = tk.Label(window, text="Red = Active infections are rising, Green = Active infections are dropping, Yellow =  Active infections are stable")
        self.legend.grid(row=8)
        self.get_countries()

    #Methods for opening webpage, called by lines in the __init__ class
    def open_wikipedia(self):
        wb.open(self.url, new=self.new)

    def open_api_source(self):
        wb.open(self.url2, new=self.new2)

    #Actual getting of the info and displaying, along with some visual indicator processing.
    def get_countries(self):
        self.country_name = self.country_entry.get()
        lower_country = self.country_name.lower()
        #Website showing caching in progress, this line checks for it.
        if r['Message'] == "Caching in progress":
            quit("Error: " + r['Message'])
        else:
            for i in r["Countries"]:
                if i["Country"].lower() == lower_country:
                    self.country.configure(text=self.country_name.upper())
                    total_confirmed = i["TotalConfirmed"]
                    self.confirmed.configure(text="Total Confirmed COVID-19 Cases: " + str(total_confirmed))
                    total_dead = i["TotalDeaths"]
                    self.deaths.configure(text="Total COVID-19 Deaths: " + str(total_dead))
                    total_new_confirmed = i["NewConfirmed"]
                    self.new_confirmed.configure(text="Total New Confirmed COVID-19 Cases: " + str(total_new_confirmed))
                    total_new_recovered = i["NewRecovered"]
                    self.new_recovered.configure(text="Total New Recovered COVID-19 Cases: " + str(total_new_recovered))
                    if total_new_confirmed > total_new_recovered:
                        self.country.configure(bg="#ff0000")
                        self.confirmed.configure(bg="#ff0000")
                        self.deaths.configure(bg="#ff0000")
                        self.new_confirmed.configure(bg="#ff0000")
                        self.new_recovered.configure(bg="#ff0000")
                    elif total_new_confirmed < total_new_recovered:
                        self.country.configure(bg="#0eff0a")
                        self.confirmed.configure(bg="#0eff0a")
                        self.deaths.configure(bg="#0eff0a")
                        self.new_confirmed.configure(bg="#0eff0a")
                        self.new_recovered.configure(bg="#0eff0a")
                    elif total_new_confirmed == total_new_recovered:
                        self.country.configure(bg="#ffff00")
                        self.confirmed.configure(bg="#ffff00")
                        self.deaths.configure(bg="#ffff00")
                        self.new_confirmed.configure(bg="#ffff00")
                        self.new_recovered.configure(bg="#ffff00")


#Running the program upon start.
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Covid Search Engine")
    api = API_Harvest(window)
    tk.mainloop()