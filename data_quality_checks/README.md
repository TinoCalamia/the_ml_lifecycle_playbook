# Data quality checks

This folder contains code for standardizing data quality checks in various projects. The goal is to make it easy for everyone to implement consistent and reliable data quality checks in their own projects.

The code provided here serves as a template and can be easily customized to fit the specific needs of each project. The data quality checks included cover a wide range of areas, including data completeness, accuracy, and timeliness. The checks are designed to be run automatically, ensuring that data quality is monitored in real-time or batch.

I believe that standardizing data quality checks will not only improve the accuracy and reliability of the data, but also save time and effort in the long run. By using a consistent and reliable set of checks, teams can focus on analyzing and interpreting the data, rather than worrying about the quality of the data itself.

I hope that this code snippets will be useful to data scientists, data engineers, and anyone who is responsible for ensuring the quality of their data. If you have any questions or suggestions, please don't hesitate to reach out.

Thank you for using the Data Quality Checks repository. Happy data checking!

## How to use it

1. Choose the quality tests which need to be performed
2. Eventually modify the base code to meet other project's edge cases
3. Perform all tests
4. Add up all boolean flags that are return after the test has been performed and divide by the number of tests
5. Use the overall quality score as evaluation for the dataset
