from airflow.utils import timezone

from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping


DBT_PROJECT_DIR = "/opt/airflow/dbt/greenery"

profile_config = ProfileConfig(
    profile_name="greenery",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
        conn_id="bigquery_dbt",
        profile_args={
            "schema": "dbt_sun",
            "location": "asia-southeast1",
        },
    ),
)

greenery_dbt_project = DbtDag(
    dag_id="greenery_dbt_dag",
    schedule_interval="@daily",
    start_date=timezone.datetime(2023, 3, 17),
    catchup=False,
    project_config=ProjectConfig(DBT_PROJECT_DIR),
    profile_config=profile_config,
    tags=["DEB", "Skooldio"],
)