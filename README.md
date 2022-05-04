  In our project, we created a dataclass called TwitchDataGame that has attributes for all the columns in the
twitch game data csv file and we stored the information from the dataset into TwitchDataGame objects. For this
dataclass, we created a function load data game that filters through the dataset and returns a list of TwitchDataGame
objects only for one game within input years. Similar processes were done for the TwitchDataGlobal dataclass which
transforms the twitch global csv, and the CovidData dataclass which transforms the covid by year csv. For the
1
Covid data we created an algorithm to help us get the total cases in a month for a country, by splitting the date
string into year month and day, and adding to a local variable until it reaches the last day of the month, in which the
value is then returned. Our program shows our results on various graphs, showing the viewership on Twitch over the
months, streams being broadcasted, Covid cases over time, and also graphs showing the growth of different games
during the pandemic. Our dropdown menu allows the user to look at different years of the data, the Covid situation
of multiple countries, and the viewership of various games. Utilizing Dash, we were able to create an interactive
dashboard, allowing us to illustrate the trends in viewership, and streams while comparing them to the growth of
the pandemic. With Dash core components, we used .graph( ) and plotly.express.line( ) to create our graph, with a
line connecting all the points together. With .Dropdown( ) we were able to give the user the option to change the
information shown on the graph, allowing them to compare different sets of data together. Additionally, Dash made
it easy for us to design the dashboard with its built in html components.
