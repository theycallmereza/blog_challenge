# Blog Challenge Backend

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Project Description

This project is the backend of a blog application, developed as part of a challenge for an interview process with a company. The backend handles data management and API endpoints necessary to support the frontend of the blog application. It manages the retrieval and display of blog posts, along with handling user ratings for each post.

## Features

- **Show a list of blog posts with average ratings and the number of ratings:**  
  Retrieve a list of blog posts, including each post's average rating and the total number of ratings. To handle potentially large numbers of ratings efficiently, the average rating and count are preprocessed and stored. This preprocessing ensures quick and efficient retrieval of these metrics without having to compute them on-the-fly each time a request is made.

- **View detailed information for each post**
- **Users can add ratings to each post**
- **Uses Docker for containerization**
- **PostgreSQL is used for database management**
- **Redis is used for caching and managing data**
- **Handles fake ratings by users to ensure the integrity of the ratings system:**
  - **Read Time Calculation:** Estimates the time required to read a blog post and monitors how quickly users submit their ratings. If a user rates a post before the calculated read time has elapsed, the rating is flagged as potentially fake.
  - **User Interaction Analysis:** Uses Redis to store and analyze user interaction data with the blog posts. This includes tracking metrics such as time spent on posts and engagement patterns. Ratings submitted with unusual interaction patterns, such as rapid submissions, are flagged for further review.

- **Mitigates impact of social media influence on ratings:**  
  When a post link is shared on social media platforms like Telegram, it can lead to a surge in ratings that might skew the overall rating. To address this, an approach is implemented where the average rating is calculated per hour, and then an average of these hourly averages is computed. This method helps to smooth out the impact of sudden rating spikes and ensures that the total rating remains more representative of genuine user feedback.

- **Profiling endpoint using Django Silk to monitor and analyze performance**

## Installation

To get this project running locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/theycallmereza/blog_challenge.git

2. Navigate to the project directory:
    ```bash
   cd blog_challenge

3. Create a `.env` file by copying the contents of `.env.sample`:
    ```bash
    cp .env.sample .env

4. Build and start the application using Docker:
    ```bash
   docker-compose up --build

5. Run database migrations:
    ```bash
   docker-compose exec blog_web python blog/manage.py migrate

## Usage
The application can be accessed at the following base URL:
- Base URL: http://localhost:8585