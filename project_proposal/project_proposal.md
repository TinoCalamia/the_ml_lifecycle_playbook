# Project proposal
The project proposal file is an overview of all relevant aspects of a machine learning project.

## Problem statement
Describe the observed problem in it's details and cover who is affected in what magnitude.

**Example**: Current marketing email campaigns are sent to all customers which leads to high costs even though it is likely that ony a small fraction will even react to the email.

## Key assumptions
List all assumptions about the business, customers and the potential solution.

**Example**:
* The majority of the customers do not read the received email
* Costs could be optimized  and profit increased if only relevant customers are targeted
* The company is able to identify the relevant customers using machine learning.

## Opportunity/ Use cases
Quantify the opportunity that opens up solving the problem and ideally show a monetary value for the business (only if possible)

**Example**: By targeting only the most relevant 20% of customers (instead of all) costs can be reduced by 10.000$ which will increase the profitability of the campaign by 30%.

## Proposed solution
This section outlines the suggested solution from a technical and business perspective. It is not needed to go in-depth for both but it should give a clear idea of how the outcome should look like.

**Example**: The data science team will design a machine learning model that predicts the probability of a customer reading the email weekly. The model automatically takes the highest 20% and sends these to a database. An automated report pulls the list every Monday so that the marketing team can use the list of customers for their email campaign.


## Why should it be built?
In this section it should be explained why it is useful to start this project. 

**Example**:
* More efficient customer targeting
* Automation of processes
* Cost reduction

## Why shouldn’t it be built?
In this section all reasons against building this product should be listed. Usually already existing tools and workflows are mentioned.

**Example**:
* Developing an own model is more expensive than buying one.
* The assumptions are not backed by data.
* The company already has similar tools.

## Success criteria
This is the section in which the chosen measurement for success is been described. This is in most cases a business metric.

**Example**:

The success of the project will be measured through the campaign profitability and the comparison to historic campaigns.

## Risks
Identify risk that could lead the project to fail.

**Examples**:
* Not enough data to model
* Not enough human resources to work on this project


## Ethical considerations
Describe which ethical considerations have been made and what measure should mitigate these.

**Example**:
The customer base has a focus on North America and almost no Asian customers which leads to a training data set that mostly considers North American customers. To account for the regional imbalance and potential ethnic differences the overall data set size has been reduced to reach a balanced ratio of customers.

## Limitations
List limitations of key assumptions or the technical design.

**Examples**:

Due to the fact that the training data set has been reduced in size to account for regional imbalance, the performance is mediocre.


## Involved stakeholders
List all keyx decision makers and relevant stakeholders. This list can vary from project to project

**Example**:
* Tech lead: ...
* Data lead: ...
* Business lead: ...
* Ethics lead: ...
* Design lead: ...

## Deliverables
Describe how the final deliverable looks like

**Example**:
 The final deliverable will contain a machine learning model that runs weekly and produces scores to the data warehouse. Additionally a report will be created that surfaces the customer list to the marketing team.

## Timeline
Mention the estimated timeline of the project.

**Example**: 01.01.2023 - 31.03.2023

## Relevant resources
List all other resources that could be relevant for a reader.

