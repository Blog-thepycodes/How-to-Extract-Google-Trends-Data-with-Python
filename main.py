from pytrends.request import TrendReq
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import time


# Set the styling for the plots
sns.set_style("whitegrid")




def initialize_trends():
   """Initialize the Google Trends request object."""
   return TrendReq(hl="en-US", tz=360)




def create_widgets(root, pytrends):
   Label(root, text="Google Trends Data Extraction", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2,
                                                                                  pady=10)


   Label(root, text="Enter Keywords (comma-separated):").grid(row=1, column=0, padx=10, pady=5, sticky=E)
   keywords_entry = Entry(root, width=50)
   keywords_entry.grid(row=1, column=1, padx=10, pady=5)


   Label(root, text="Enter Timeframe (default is 'all'):").grid(row=2, column=0, padx=10, pady=5, sticky=E)
   timeframe_entry = Entry(root, width=50)
   timeframe_entry.grid(row=2, column=1, padx=10, pady=5)


   Button(root, text="Get Interest Over Time",
          command=lambda: get_interest_over_time(pytrends, keywords_entry, timeframe_entry)).grid(row=3, column=0,
                                                                                                  columnspan=2,
                                                                                                  pady=10)


   Button(root, text="Get Interest by Region", command=lambda: get_interest_by_region(pytrends, keywords_entry)).grid(
       row=4, column=0, columnspan=2, pady=10)


   Button(root, text="Get Related Topics", command=lambda: get_related_topics(pytrends, keywords_entry)).grid(row=5,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              pady=10)


   Button(root, text="Get Related Queries", command=lambda: get_related_queries(pytrends, keywords_entry)).grid(row=6,
                                                                                                                column=0,
                                                                                                                columnspan=2,
                                                                                                                pady=10)


   Button(root, text="Get Suggestions", command=lambda: get_suggestions(pytrends, keywords_entry)).grid(row=7,
                                                                                                        column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)


   Button(root, text="Get Trending Searches", command=lambda: get_trending_searches(pytrends)).grid(row=8, column=0,
                                                                                                    columnspan=2,
                                                                                                    pady=10)


   Button(root, text="Get Real-Time Trending Searches", command=lambda: get_realtime_trending_searches(pytrends)).grid(
       row=9, column=0, columnspan=2, pady=10)




def handle_request(func):
   """Decorator to handle request rate limiting."""
   def wrapper(*args, **kwargs):
       try:
           return func(*args, **kwargs)
       except Exception as e:
           if "429" in str(e):
               messagebox.showinfo("Rate Limit Exceeded", "Rate limit exceeded. Waiting for 60 seconds.")
               time.sleep(60)
               return func(*args, **kwargs)
           else:
               messagebox.showerror("Error", str(e))
   return wrapper




@handle_request
def get_interest_over_time(pytrends, keywords_entry, timeframe_entry):
   keywords = keywords_entry.get().split(',')
   timeframe = timeframe_entry.get() or "all"


   pytrends.build_payload(keywords, timeframe=timeframe)
   interest_over_time_df = pytrends.interest_over_time()
   plot_interest_over_time(interest_over_time_df, "Interest Over Time")




@handle_request
def get_interest_by_region(pytrends, keywords_entry):
   keyword = keywords_entry.get().split(',')[0]


   pytrends.build_payload([keyword], timeframe="all")
   region_interest = pytrends.interest_by_region(resolution="COUNTRY", inc_low_vol=True, inc_geo_code=True)
   sorted_regions = region_interest[keyword].sort_values(ascending=False).reset_index()
   display_data(sorted_regions)




@handle_request
def get_related_topics(pytrends, keywords_entry):
   keyword = keywords_entry.get().split(',')[0]


   pytrends.build_payload([keyword], timeframe="all")
   related_topics = pytrends.related_topics()
   display_data(related_topics[keyword]["top"].reset_index())




@handle_request
def get_related_queries(pytrends, keywords_entry):
   keyword = keywords_entry.get().split(',')[0]


   pytrends.build_payload([keyword], timeframe="all")
   related_queries = pytrends.related_queries()
   display_data(related_queries[keyword]["top"].reset_index())




@handle_request
def get_suggestions(pytrends, keywords_entry):
   keyword = keywords_entry.get().split(',')[0]


   suggestions = pytrends.suggestions(keyword)
   display_data(pd.DataFrame(suggestions))




@handle_request
def get_trending_searches(pytrends):
   trending_searches = pytrends.trending_searches(pn="united_kingdom")
   display_data(trending_searches.reset_index())




@handle_request
def get_realtime_trending_searches(pytrends):
   realtime_trending_searches = pytrends.realtime_trending_searches()
   display_data(realtime_trending_searches.reset_index())




def plot_interest_over_time(data, title):
   ax = data.plot(figsize=(12, 8), title=title)
   ax.set_xlabel("Date")
   ax.set_ylabel("Interest")
   plt.legend(title="Keywords")
   plt.show()




def display_data(data):
   top = Toplevel()
   top.title("Data Display - The Pycodes")


   # Create a treeview with vertical and horizontal scrollbars
   frame = Frame(top)
   frame.pack(fill=BOTH, expand=1)


   tree = ttk.Treeview(frame, columns=list(data.columns), show="headings")
   tree.pack(side=LEFT, fill=BOTH, expand=1)


   vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
   vsb.pack(side=RIGHT, fill=Y)


   hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
   hsb.pack(side=BOTTOM, fill=X)


   tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)


   for col in data.columns:
       tree.heading(col, text=col)
       tree.column(col, width=100)


   for index, row in data.iterrows():
       tree.insert("", "end", values=list(row))


   top.geometry("600x400")
   top.mainloop()




if __name__ == "__main__":
   root = Tk()
   root.title("Google Trends Data Extraction App - The Pycodes")
   pytrends = initialize_trends()
   create_widgets(root, pytrends)
   root.mainloop()
