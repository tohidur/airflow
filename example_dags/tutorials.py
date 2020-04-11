from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['ariflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minute=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_time': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


dag = DAG(
    'tutorial',
    default_args=dfault_args,
    description='TEST - A simple tutorial DAG',
    schedule_internval=timedelta(days=1)
)


t1 = BashOperator(task_id='print_date', bash_command='date', dag=dag)
t2 = BashOperator(task_id='sleep', depends_on_past=False, bash_command='sleep 5', retries=3, dag=dag)


dag.doc_md = __doc__
t1.doc_md = """\
    #### Task Documentation
    You can document your task using the attributes  `doc_md` (markdown),
    `doc` (palain text), `doc_rst`, `doc_json`, `doc_yaml`, which gets rendered
    in the UI's Task Instnace Details page.
    ![img](http://example.com/example.png)
    """

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7) }}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(task_id='templated', depends_on_past=False, bash_command=templated_command,
                  params={"my_param": "Parameter I passed in"}, dag=dag)

t1 >> [t2, t3]
