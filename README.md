# Instabot

Determine whether a user is genuine or a bot, based on their follower/following ratio, name, and bio

This is an example of a 'fake' account:
<img src="https://raw.githubusercontent.com/ethanzh/instabot/master/static/fake_account.png" width=200>


### TODO
- [x] Get basic information from account, given username 
- [x] Populate CSV with all account information
- [ ] Make screenshot module only run if a screenshot doesn't already exist
- [ ] Decide on a reliable list of accounts to crawl
- [ ] Determine which features are most important when classifying accounts as real or fake

## Usage

1. Clone the repository
2. Create a virtual environment and run ```pip install -r requirements.txt```
3. Run via command line ```python run.py <file-name> <ig-username1> <ig-username2> ... ```

Upon completion, a CSV file with the supplied name will be generated within the current directory