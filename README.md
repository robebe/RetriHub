# RetriHub
#### Interrogating [Github's API](https://developer.github.com/v3/) and visualizing data using [D3.js](https://d3js.org/)


## Run Demos
```
#data retrieval
chmod +x demo_data_retrieval.sh
./demo_data_retrieval.sh

#visualization
chmod +x demo_visualization.sh
./demo_visualization.sh
```
## Data retrieval
The folder *data_retrieval* contains contains scripts to interrogate the API. Executing *main.py* as follows:
```
python main.py user_name
```
will result in a shell prompt asking for a Github account to generate a 0-auth-token. The token will be stored in *0AuthToken.txt* for future user. Alternatively
```
python main.py user_name auth_token
```
can be executed, if a 0-auth-token has already been created. As a next step the function *acqu_users()* will recursively search for user names until interrupted by the ENTER key (see shell prompts for guidance).
*repo_commits.py* will then retrieve the information that is defined in the function *_get_commit_data()* for each repository of each user. The *max_repos* variable is set to 20 repositories by default to speed up the process.
The data stored in CSV format can be found in the respective repository (see *data/user_name/repo_name*). A log file which is generated for each user keeps track of the repository downloading progess (see *log_files/*).

## Data visualization

The code for visualization of additions/deletions of a Github project over time was copied from a tutorial provided on [www.cacheflow.ca](https://github.com/DeBraid/www.cacheflow.ca) created by [Derek Braid](https://github.com/DeBraid). Some alterations have been made to the JavaScript files in order to fit the present CSV data. I do not claim ownership to any JavaScript or CSS file contained in *d3_visualize*. 
