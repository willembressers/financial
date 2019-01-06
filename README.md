# Financial

My custom Python Dash app (dashboard) for my personal financial data. It gives me insight in my financial status based on my transaction history.

If you want to use it:
 
 - create a data folder
 - add a csv file (annotated.csv)
 
The csv file should have the following columns:

- date (a valid python datetime format)
- amount (float)
- label (string)
  
Run the dashboard
```bash
python index.py 
```