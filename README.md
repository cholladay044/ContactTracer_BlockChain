# **Contract Tracing Blockchain**

**V1.21**

**Prepared by:**

Timothy Smith, Jordan Renaud, Olivia Wojcik,

Cole Holladay, Zachary Philipp, Ross Dillard

**Southeast Missouri State University**

**1st**  **March 2021**

**Table of Contents**

1. **Introduction**

1. **Purpose pg 3**
2. **Scope**
3. **References**

1. **Design**

1. **Design Introduction pg 4**
2. **Design Entity**** pg 5**

1. **Design Description Organization pg 6**

1. **Design Views**
2. **Detail Description**** pg 8**
3. **Dependency Description pg 9**

1. **Use Cases**  **pg 10**

1. **Use Case Diagrams**
2. **System Flow**  **pg 11**

# 1. Introduction

## 1.1 Purpose

The purpose of this document is to provide a description of the software being created to facilitate analysis, planning, implementation and decision-making for the project, &quot;Contact Tracing Blockchain.&quot; This document will be used as a source for expressing the software design information and used as a blueprint for further implementation. The intended audience for this SDD is our clients, the developers and designers of the software, and future personnel for the Contact Tracing Blockchain software.

## 1.2 Scope

This Software Design Document is for the initial release of a base level system which will work as a proof of concept for the use of building a system with functionalities to show feasibility for further applications. The design of this software will provide a preliminary system to showcase the critical parts of Contact Tracing Blockchain. The immediate goal for the design of this system is to be able to create a currency that is automatically traded between users within a certain distance to assist with contact tracing. The major design of the system will rely on blockchain technologies.

## 1.3 References

The users of this SDD may need the following documents for reference:

Dillard, R., Holladay, C., Philipp, Z., Renaud, J., Smith, T., &amp; Wojcik, O. (2021). Software Requirements Specification for Contract Tracing Blockchain: V1.0. [https://semo0-my.sharepoint.com/:w:/g/personal/cholladay1s\_semo\_edu/Ef3nDUUGVK9OvDlMcVmv9TEBxvFS5ul83lhIXnfw0C07zg?e=aB27M8](https://semo0-my.sharepoint.com/:w:/g/personal/cholladay1s_semo_edu/Ef3nDUUGVK9OvDlMcVmv9TEBxvFS5ul83lhIXnfw0C07zg?e=aB27M8)

## 2. Design

## 2.1 Design Introduction

Our design is based around ideas of simplicity. We are in a time of change with requirements on this project, so this is subject to change as well. In our current system ideas of automation have been scrapped to promote user privacy. Users should feel as if they can contribute to the system when they want. Main areas of user tracking will indicate current perceived risk level as well as the number of contacts made. Details of those contacts can be found out with administrative privileges.

## 2.2 Design Entity

![](.README_images/entity.png)

#

# 3. Design Description Organization

## 3.1 Design Views

Decomposition Description

User-interface

Allows the users to interact with the software on their mobile device.

![](.README_images/d33f4828.png)

Webservices

Handles requests from the application (REST)

![](.README_images/3489fda5.png)
![](.README_images/4b17af3d.png)
Blockchain Backend Implementation

Encapsulates the data that makes up the various entities of blockchain technologies – block, transaction, etc.

Dependency Description

Client/Viewer Web Service endpoint access

The client app must be able to send location updates and request risk level updates from the server.

Data Processing

The data processor will require libraries such as pandas and numpy to effectively filter and search the large datasets.

Interface Description

GPS

Application will need access to user&#39;s location data in order to

provide usable information

Webservice

The application will need access to many of the entities to make

appropriate REST calls.

Detail Description

TracerWebService - Handles web service calls between a client app and the backend server

User - Represents a user object

Viewer - Represents a user that can use the viewer website

Blockchain - The actual blockchain

Transaction - Represents a transaction (confirmed contact by proximity)

Block - Stores transactions in chronological order

DatabaseManager - Manages database connection, inserts, selects, etc. methods for all required operations

PositiveCase - Represents a singular positive covid case instance

UserLocationProcessor - Processes the daily location updates on a set interval, checks locations for proximity with other users within short/exact time intervals and generates transactions for the blockchain

UserRiskFinder

- Gathers Positive Covid cases reported within the specified date range
- Gathers confirmed direct contact transactions from the blockchain for each positive case (1 week)
- Generates a 4 level tree rooted off of the user&#39;s contacts, and their contacts, and their contacts, etc.. in the specified period
- Traverse the tree by breadth and schedule notifications for each person on each risk level

ViewerWebServer - Like the TracerWebService, using Flask to serve http content on port 80/443, but serves templated html content to authorized Viewer users.

# 4. Use Cases

## 4.1 Use Case Diagrams

![](.README_images/9ce1b5e5.png)
![](.README_images/12803918.png)
Users will download an application from their respective app store. Upon opening, the user will be prompted to create and account or sign into an existing account. next, it will request permissions from the user. The user will have access to a settings screen, allowing them to turn off location tracking when they choose. The user can also choose to uninstall the app to get the same effect. While the app is running in the background and the user has opted into tracing, periodic GPS coordinate updates will be sent to the server. The server will record these location updates indexed by datetime and userid.

Once, at the end of each day, the server will run algorithms over the data it has collected, searching for people who have been within a specified range R of each other at the same time. If contact is confirmed between two people via the algorithm&#39;s analysis, a token will be generated and logged in the blockchain, containing the two users&#39; internal ID numbers, the datetime and coordinates that were used in the calculations of the algorithm, and any other relevant data. These transactions will be sorted by datetime, allowing the blockchain to be amended chronologically. This will also allow for easier searching, using date range filters to filter out irrelevant date intervals.

The viewer app will allow certain people, given permissions, to view different pieces of information in the blockchain. This data is completely anonymized by only showing a user ID, datetime and location of contact. A database will exist, allowing users of the viewer app (doctors, nurses, etc) to submit positive cases of covid, referencing a user&#39;s id . The user that tested positive could also potentially have the ability to report their case within the app, however this could be abused. The User application can query the server for positive contacts. This is done by querying the blockchain for all of a user&#39;s contacts/contact tree in a certain date range, then checking to see if any of those users are present in the covid-positive database table. Based on the degree of separation from direct contact, each affected user&#39;s risk level will be updated. The client app will periodically check for risk level changes, and if one is detected, it should display a notification and update the app theme to reflect the user&#39;s risk level.

Ideally, the user should be able to view anonymized statistics about the contact they&#39;ve made, such as close contacts per day, average/listed out degrees of separation from covid cases, number of covid cases within a separation degree of 4, number of people potentially infected by their own positive case of covid pre-testing, etc.

Wallets and transfer of tokens aren&#39;t practical, as transactions would need to represent a transfer of currency/goods from one wallet to another, whereas this system records two people meeting up as a singular event, rather than a transfer.
