[[_TOC_]]

# **Overview**
---

This project contains a script to change vlans if necessary and the module that it depends on. 
We make use of an input file that contains our switch information and an environment variable file to contain secrets.

```
 :::  ===  === ::: :::= ===          == ==  :::  ===  === :::=====  == :::====  :::=====      :::=====  :::===== :::==== :::==== ::: :::= === :::=====       :::====  :::===== :::==== :::==== :::===== :::====  == == 
 :::  ===  === ::: :::===== ========  == == :::  ===  === :::      ==  :::  === :::           :::       :::      :::==== :::==== ::: :::===== :::            :::  === :::      :::==== :::==== :::      :::  ===  == ==
 ===  ===  === === ========                 ===  ===  === ======       =======  ======        === ===== ======     ===     ===   === ======== === =====      =======  ======     ===     ===   ======   =======        
  ===========  === === ==== ========         ===========  ===          === ===  ===           ===   === ===        ===     ===   === === ==== ===   ===      ===  === ===        ===     ===   ===      === ===        
   ==== ====   === ===  ===                   ==== ====   ========     ===  === ========       =======  ========   ===     ===   === ===  ===  =======       =======  ========   ===     ===   ======== ===  ===       
                                                                                                                                                                                                                       
```

# **Requirements**
---

1. .env file for environment variables

- Python-dotenv is used to minimize hardcoding and to store secrets
- The variables should be in the following format:

```
key=value
```

2. Input csv file with all needed information 

3. Jinja Template for interface config comparison

- The Jinja2 template here is simple but more in-depth reading can be found here:

[Jinja2 Templates](https://jinja.palletsprojects.com/en/3.1.x/)

4. We must make sure that all python packages are installed

```
pip install python-dotenv
pip install jinja2
pip install tqdm
```

5. All files must be in the same directory as well

# **The Nitty Gritty**
---

- In your terminal emulator, navigate to the file path of the script to be ran.

```
cd <FILE PATH>
```

- Run the script with the following command:

```
python vlan_change.py
```

- This one won't talk to you much but you have a progress bar to keep an eye on.

# **Changelog**
---

## 1.0.0 (June 18, 2022)

FEATURES:
* Changelog started
* Initial version

ENHANCEMENTS:

BUG FIXES:

---
