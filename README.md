# Food Delivery Dashboard

As the name suggests, this repository enables an individual to visualize a dashboard for food delivery companies.

## Installation

The project has been coded in Python 3.8.10 and can be run with a Jupyter notebook and on the terminal. Given below are a set of instructions to access the project:

1. Install [Python](https://realpython.com/installing-python/) (if not installed already).
2. Install [pandas](https://pandas.pydata.org/docs/getting_started/install.html), [streamlit](https://docs.streamlit.io/library/get-started/installation),  [pydeck](https://pydeck.gl/installation.html) and [geopy](https://geopy.readthedocs.io/en/stable/#installation) libraries.
3. Clone the repository to your local machine.

## Usage

1. From your terminal, navigate to the directory where the files have been cloned.
2. Create a directory called 'data' (`mkdir data`) and upload csv files of database. 
3. Open 'merge_tables_in_one.ipynb' and run the notebook to get one full csv file. 
4. Type - `streamlit run main.py` to run the project. 
5. The dashboard should be visible on a web browser interface. 
6. Navigate through the dashboard and select options based on preferences. 

Steps 2 and 3 are only required before first use. Depending on your computer power, running the whole notebook script shouldn't take more than 30 minutes. 

## Future Releases (To-do)
1. Add docstrings for functions. 
2. Optimize codebase. 
3. Implement code to visualize heatmap of restaurant orders, customer ordering patterns, orders made by customers from competitor restaurants. 
4. Provide additional insights for allergies. 

## Contributors
1. Anzeem Arief
2. Kivanc Gunduz
3. Nemish Mehta
4. Tony Anciaux
