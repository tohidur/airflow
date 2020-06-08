### Getting Started

- File can also be passed in bash_command.

- Template - Possible to define your template_searchpath as pointing to any
  folder location in DAG constructor call.

- Template - user_defined_macros and user_defined_filters

*Setting up dependencies*
```
t1.set_downstream(t2)

# equivalent to
t2.set_upstream(t1)

# OR with shift operator
t1 >> t2 >> t3
t2 << t1

# Set list of tasks as dependencies
t1.set_downstream([t2, t3])
[t2, t3] << t1

# Airflow will throw error if there is a cycle,
# Or if dependency is referenced more than once.
```

*Basic Testing*  
`python ~/airlfow/dags/tutorials.py`


*Metadata validation*  
```
airlfow list_dags

airflow list_tasks tutorial

airflow list_tasks tutorail --tree
```  

*Test Run*  
Command layout: command sub-command dag_id task_id date    

`airflow test tutorial print_date 2015-06-01`

*Backfill*  
- If you use `depends_on_past=True`, individual task instances will depend on the success of their previous task
  instance (that is previous according to execution_date)
  
- `wait_for_downstream=True` will cause a task instance to also wait for all task instances immediately
  downstream of previous task instance to succeed.

`airflow backfill tutorial -s 2015-06-01 -e 2015-06-07`


### Setting configuration options
- Use airflow.cfg file.
```
[core]
sql_alchemy_conn = my_conn_string
```

Also possible through environment variables by using this format `$AIRFLOW__{SECTION}__{KEY}`  
`export AIRFLOW__CORE__SQL_ALCHEMY_CONN=my_conn_string`   

Also possible at runtime by appending `_cmd` to the key   
```
[core]
sql_alchemy_conn_cmd = bash_command_to_run
   ```

    ```
    Supported cmd version configuration

    - sql_alchemy_conn in [core]
    - fernet_key in [core]
    - broker_url in [core]
    - flower_basic_auth in [celery]
    - result_backend in [celery]
    - password in [atlas]
    - smtp_password in [smtp]
    - bind_password in [ldap]
    - git_password in [kubernetes]


    Also possible by export
    export AIRFLOW__CORE__SQL_ALCHEMY_CONN_CMD=bash_command_to_run
    ```

*Configuration order or precedence*  
- Env variable
- command env variable
- airflow.cfg
- command line in airflow.cfg
- Airflow default's    


### Initialize a DB backend
*MySQL*  
```
in my.cnf under [mysqld]
explicit_defaults_for_timestamp=1
```

Once setup alter the SqlAlchemy connection string, `executor` settings to use
"LocalExecutor".


### Using operators
A operator represents a single, ideally idempotent, task

