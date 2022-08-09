# PortfolioTracker
Assets porftolio tracker

**Usage:** Each .py file updates the corresponding .csv file using API calls to exchanges (each one corresponds to one exchange). Each .csv file in the working directory contains a time series tracking assets on one exchange. The file TOTAL.txt holds the sum of assets on all exchanges and is generated via TOTAL.py. 

Assets on exchanges are updated using API calls on scheduled times (cron job on the server).

index.php collects all the information and displays the time series of selected assets and the pie chart breakdown of all the assets held on different exchanges.
