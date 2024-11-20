# python-aerothermal

python-aerothermal is a solution to acquire house consumptions data from i-DE (spanish electricity distribution company) and send it to Zabbix

You have to prepare a server to create a daily job to launch the bash script which calls the Python script

## Installation

The first thing you must do is creating a credentials file to access the frontend of i-DE. You have an .ini example in the distribution and could be copied into */etc* with access only available to the user without privileges.
To track the success of the script we need to establish a logfile in */var/log/*. Again we need to give access to the user previously configured and add a *logrotate* file, also in the repository, to avoid the growth of the file withou control.
Another thing you must do is creating a *Python* virtual environment in order to run the script (always with the unprivileged user):

```bash
python -m venv ~/.venv
```

The *bash* script will check the sanity of the environment before calling the *Python* script.

## Usage

Once you've setup everything you can create the *cronjob* just for the user:

```text
0 8 * * *   /bin/bash /home/metrics/python-aerothermal/zabbix_iber.sh -c /etc/credentials.ini -l /var/log/zabbix-iber.log >/dev/null 2>&1
```

In the previous line, established with the command ```crontab -e```, you can see the files referred before.

The configuration of the *Zabbix* server and the agent can be consulted in my [blog](https://libreadmin.es/new-post-just-to-remember-using-david-bowie-lets-dance/) and in [my related GitHub repository](https://github.com/darkschneider16/home-infrastructure). In the future I'll share in my blog the item where the script sends the data inside the template which draws the state of the house.

## Testing

In the repository you'll find a preliminar test to develop the whole project with a BDD (Behaviour Driver Development) strategy using the *Python* library *behave*. If you want to try this, or better, contribute with the rest of the tests, you must install it in the virtual environment:

```bash
(.venv) pip install behave
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

I've included the library from the user [hectorespert](https://github.com/hectorespert) called [python-oligo](https://github.com/hectorespert/python-oligo).

I licensed my code in the same way and i've added two new methods to the class. I hope that everything will be alright with it since the library is frozen in *GitHub*.
