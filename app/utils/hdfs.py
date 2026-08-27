from pyspark.sql import SparkSession


HDFS_NAMENODE = "hdfs://namenode:9000"


def get_spark():
    """
    Crée une SparkSession pour lire les données HDFS.
    """

    return (
        SparkSession.builder
        .appName("Space-DataLake-Dashboard")
        .getOrCreate()
    )


# ============================================================
# GAIA
# ============================================================

def read_gaia_global():

    spark = get_spark()

    path = f"{HDFS_NAMENODE}/gold/source=gaia/global_kpis"

    return spark.read.parquet(path)


def read_gaia_temperature():

    spark = get_spark()

    path = f"{HDFS_NAMENODE}/gold/source=gaia/temperature_bands"

    return spark.read.parquet(path)


def read_gaia_magnitude():

    spark = get_spark()

    path = f"{HDFS_NAMENODE}/gold/source=gaia/magnitude_bands"

    return spark.read.parquet(path)


def read_gaia_distance():

    spark = get_spark()

    path = f"{HDFS_NAMENODE}/gold/source=gaia/distance_bands"

    return spark.read.parquet(path)


# ============================================================
# NEOWS
# ============================================================

def read_neows_global():

    spark = get_spark()

    path = f"{HDFS_NAMENODE}/gold/source=neows/global_kpis"

    return spark.read.parquet(path)


def read_neows_by_date():

    spark = get_spark()

    path = f"{HDFS_NAMENODE}/gold/source=neows/by_date"

    return spark.read.parquet(path)


def read_neows_hazard():

    spark = get_spark()

    path = f"{HDFS_NAMENODE}/gold/source=neows/hazard_analysis"

    return spark.read.parquet(path)