---
name: apache-superset
description: Deploy, configure, and automate Apache Superset business intelligence dashboards, chart creation, SQL Lab queries, and database connections via REST API and superset-api-client. Use when creating BI dashboards, managing data visualization layers, or automating Superset resources.
license: Apache-2.0
metadata:
  origin: General-Gemini
tools: Read, Write, Edit, Bash, Grep, Glob
---

# Apache Superset BI & Dashboard Skill

Production automation and management for Apache Superset (cloud-native business intelligence, semantic data exploration, and interactive analytics dashboards).

## When to Activate

- Designing or deploying Apache Superset BI dashboards, charts, and metric slices
- Automating dataset synchronization, calculated columns, and metrics via `superset-api-client`
- Connecting enterprise databases (PostgreSQL, ClickHouse, BigQuery, MySQL, SQLite, DuckDB)
- Configuring docker-compose or Kubernetes Helm deployments for Superset infrastructure
- Writing and automating SQL Lab analytical queries

---

## 1. Automated Python API Integration (`superset-api-client`)

Connect and automate dashboards programmatically:

```python
from supersetapiclient.client import SupersetClient

# Initialize authenticated client
client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin_password"
)

# 1. Connect or query a Database
databases = client.databases.find(database_name="Main_Postgres")
if not databases:
    db = client.databases.create(
        database_name="Main_Postgres",
        sqlalchemy_uri="postgresql+psycopg2://user:pass@localhost:5432/analytics"
    )
else:
    db = databases[0]

# 2. Register a Dataset from table or custom SQL
datasets = client.datasets.find(table_name="daily_active_users")
if not datasets:
    dataset = client.datasets.create(
        database=db.id,
        schema="public",
        table_name="daily_active_users"
    )
else:
    dataset = datasets[0]

# 3. Create or Update a Dashboard
dashboards = client.dashboards.find(dashboard_title="Executive Growth Metrics")
if not dashboards:
    dashboard = client.dashboards.create(
        dashboard_title="Executive Growth Metrics",
        published=True
    )
```

---

## 2. Standard Database SQLAlchemy Connection Strings

| Engine | Driver / Scheme | SQLAlchemy URI Template |
| :--- | :--- | :--- |
| **PostgreSQL** | `psycopg2` | `postgresql+psycopg2://user:password@host:port/database` |
| **ClickHouse** | `clickhouse-connect` | `clickhousedb://user:password@host:8123/database` |
| **Google BigQuery**| `pybigquery` | `bigquery://project-id/dataset?credentials_path=/path/to/key.json` |
| **MySQL** | `mysqlclient` / `pymysql` | `mysql+pymysql://user:password@host:3306/database` |
| **SQLite / Local** | native | `sqlite:////absolute/path/to/local.db` |
| **DuckDB** | `duckdb_engine` | `duckdb:////path/to/duck.db` |

---

## 3. Deployment Patterns

### A. Turnkey Docker Compose (Recommended)
From the local repository at `C:\tools\superset`:
```powershell
cd C:\tools\superset

# 1. Initialize environment
docker compose -f docker-compose-non-dev.yml pull
docker compose -f docker-compose-non-dev.yml up -d

# 2. Setup initial admin user
docker compose -f docker-compose-non-dev.yml exec superset superset fab create-admin `
  --username admin `
  --firstname Superset `
  --lastname Admin `
  --email admin@superset.org `
  --password admin

# 3. Initialize database and roles
docker compose -f docker-compose-non-dev.yml exec superset superset db upgrade
docker compose -f docker-compose-non-dev.yml exec superset superset init
```
Default URL: `http://localhost:8088` (Credentials: `admin` / `admin`).

---

## 4. Dashboard Design & SQL Lab Best Practices

1. **Semantic Metrics First**: Define reusable metrics (e.g. `SUM(revenue) / COUNT(DISTINCT user_id)`) directly in the Superset Dataset layer rather than ad-hoc inside each chart.
2. **Filter Scoping**: Use Cross-Filtering and Global Dashboard Filters configured at the parent tab level to prevent conflicting SQL `WHERE` clauses.
3. **Partitioning & Caching**: Enable Redis caching (`CACHE_CONFIG` / `DATA_CACHE_CONFIG`) for queries that aggregate across millions of rows to achieve sub-second dashboard rendering.

---

## 5. Local References

- **Upstream Repository Source**: `C:\tools\superset\`
- **API Client Package**: `superset-api-client` (installed in Python virtualenv)
