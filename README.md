Dynamic Update DNS for namesilo.
===============
Use namesilo API and parsing XML response to update the DNS in a given time interval written in python.

How to Use : 
---------------
1. Download the source folder.

2. Edit the config.ini for your purpose. API key can be obatined from the API manager in namesilo website. **Note that quotes are not needed in the config file.**

3. Install requirements by using following command under the source folder: <pre><code> pip install -r requirements.txt </code></pre>

4. Run the program by <pre><code> python namesilo_DDNS_Update.py </code></pre>
All output will be logged in ***DDNS_Update.log*** file in the source folder.

You can modify it to run in the background depending on your operating system and preference.
You can also comment out the <code>time.sleep(check_interval)</code> line and use <code>crontab</code>to archive the same effects.
