# Weather comparison 

Simple program that I put together as part of the 'Python for Everybody' specialisation on Coursera (The capstone project course). My primary objective was to use APIs, databases and JSON to manipulate data.  It's nothing ground breaking and can probably be done in more concise / better ways, but everyone has to start somewhere!

The high-level flow of the program is:

1) Prompts a user for two addresses (could be anywhere in the world), uses the Google GeoCode API to look them up and provide latitude and longitude coordinates.
2) Look up the coordinates in the Meteostat API to find the nearest weather station for each address.  Store in the database.
3) Prompt the user for a date range and pull down weather data for both weather stations. Store in the database.

At the time or writing, still deciding what to do with the data, but think I'll calculate the mean, median and mode for each location across the duration and output that as a comparison.

