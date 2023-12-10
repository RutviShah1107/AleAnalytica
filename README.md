# Customer Insights and Growth Project

## Overview

Welcome to the Customer Insights and Growth Project repository! This project is a strategic initiative for a thriving billion-dollar enterprise in beer brewing industry, to harness valuable insights from customer survey responses. Through meticulous preprocessing, feature selection, and clustering techniques, we've crafted personas for distinct customer segments. This not only aids in understanding customer behavior but also facilitates targeted marketing strategies. The repository also includes a visually appealing dashboard showcasing the key findings and actionable recommendations derived from our analysis.
[Find the PPT here](https://github.com/RutviShah1107/AleAnalytica/blob/7fc209a87ab75b51bcce5696b3a6b37074ef3710/Capstone%20Final%20Presentation%20(2).pptx)

## Results

Each cluster has been labeled to facilitate easy reference and communication. These labels serve as shorthand for the distinct customer personas, aiding in the implementation of targeted strategies.
 <img width="955" alt="Screenshot 2023-12-10 at 5 14 13 PM" src="https://github.com/RutviShah1107/AleAnalytica/assets/86033480/8964580f-524a-4004-ad33-0d8818220b24">

## Key Features
- **Data Preprocessing:** Raw customer survey data has been preprocessed to ensure accuracy and reliability in subsequent analyses. This involves handling missing values, standardizing formats, and cleaning the dataset for optimal results.

- **Clustering:** Utilizing advanced clustering algorithms, we segmented the customer base into distinct groups. These clusters form the foundation for our customer personas, enabling a nuanced understanding of diverse customer needs, preferences, and behaviors.
  <img width="811" alt="Screenshot 2023-12-10 at 5 07 00 PM" src="https://github.com/RutviShah1107/AleAnalytica/assets/86033480/24da9937-2f29-4622-95a4-6452d92a18fe">

  
-  **Feature Selection:** To focus on the most influential factors, we employed feature selection techniques to narrow down the dataset. This step ensures that our analysis is centered on the most pertinent variables for persona creation and strategy formulation.
    <img width="571" alt="Screenshot 2023-12-10 at 5 08 02 PM" src="https://github.com/RutviShah1107/AleAnalytica/assets/86033480/fe06e2d8-42bc-480a-8033-3313d640661b">


- **Persona Creation:** Based on the clustered data, we've crafted personas for each identified segment. These personas provide detailed snapshots of customer characteristics, helping to humanize and understand the unique traits of each group.
  <img width="697" alt="image" src="https://github.com/RutviShah1107/AleAnalytica/assets/86033480/f2d88ffe-7837-48dc-a255-2293e2680c95">
  <img width="697" alt="image" src="https://github.com/RutviShah1107/AleAnalytica/assets/86033480/fc0e3231-3f0d-43f9-b4e8-2ff5b553691a">


- **Dashboard:** The project includes an interactive dashboard that visually represents key insights, cluster characteristics, and persona details. This dashboard is designed to be user-friendly, allowing stakeholders to intuitively grasp the findings and make informed decisions.
   HeatMap representing Attitudes of the Customers.
   <img width="733" alt="Screenshot 2023-12-10 at 5 17 21 PM" src="https://github.com/RutviShah1107/AleAnalytica/assets/86033480/2dad583f-7ef0-4239-987e-8a480f2a34ea">


- **Recommendations:** To drive positive growth, we've derived actionable recommendations based on the insights gained from the personas and clusters. These recommendations serve as strategic guidelines for refining marketing approaches, product development, and overall customer engagement.
[Results and Recommendations](https://github.com/RutviShah1107/AleAnalytica/blob/46d622bdc440c1d4ab12596a2517f405d1507951/Research%20Paper%20-%20Results%20and%20Recommendation%20(2).pdf)


Thank you.

## Steps to run and install the Project:

Prerequisites: [Poetry](https://python-poetry.org/docs/)
1. From the cmd run ```poetry shell``` to activate the virtual environment.
2. Use ```poetry install``` to install all the dependencies.
3. Run ```poetry run flask run``` to start the project.

## Steps to generate the preprocessed file:
Run the [preprocessing.py](./app/src/preprocessing.py) file to generate the preprocessed file used to clustering.
```
python ./app/src/preprocessing.py
```
