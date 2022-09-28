This directory has a few examples to demonstrate how to write asynchronous and threaded Ray actors. Some code snippets and ideas are borrowed from the following sources:
 * https://docs.ray.io/en/latest/ray-core/actors/async_api.html#asyncio-concurrency-for-actors
 * https://github.com/shantnu/Open-Gigabyte-File-Python
 * Fluent Python by Luciano Ramalho (for the flag downloads)

 You need to pip install the following Python packages.
 `pip install -r requirements.txt`

 Also, the npi database csv file is a 7GB file and not part of this GitHub. You will need
 to download the `.csv` and create the Sqlite DB yourself. The code is included to create it, and the URL is  http://download.cms.gov/nppes/NPI_Files.html

 Cheers
 Jules