import org.apache.spark.sql.SparkSession

object SparkConfig {
	def main(args: Array[String]) {
		// create a session
		val spark = SparkSession.builder
  			.config("spark.sql.shuffle.partitions", 5)
  			.config("spark.executor.memory", "2g")
  			.master("local[*]")
				.appName("SparkConfig")
				.getOrCreate()

		// get conf
		val mconf = spark.conf.getAll
		// print them
		for (k <- mconf.keySet) { println(s"${k} -> ${mconf(k)}\n") }
	}
}