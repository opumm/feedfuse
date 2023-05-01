# FeedFuse - Another RSS feed manager

### Setup

- Download and unzip the project.
- Build Docker images.
  ```sh
  make build
  ```
- Strat docker container to initialize the project.
  ```sh
  make run
  ```
- Create migration script.
  ```sh
  make migrate
  ```
- Initialize the db.
  ```sh
  make setup-db
  ```
- Start API container.
  ```sh
  docker compose up -d app
  ```
- Migrate database.
  ```sh
  make migrate
  ````
- Start Scheduler.
  ```sh
  docker compose up -d scheduler
  ```
- Start Workers.
  ```sh
  docker compose up -d worker

## Database design

Database tables for the RSS feed service:

**User**

Table name: `user`

| Column Name | Data Type | Constraints      | Description                  |
|-------------|-----------|------------------|------------------------------|
| id          | integer   | primary key      | Unique identifier for a user |
| email       | string    | not null, unique | Email address of the user    |
| full_name   | string    | unique           | Full name of the user        |
| password    | string    | not null         | Password of the user         |

**Subscription**

Table name: `subscription`

| Column Name | Data Type | Constraints                       | Description                                               |
|-------------|-----------|-----------------------------------|-----------------------------------------------------------|
| id          | integer   | primary key                       | Unique identifier for a subscription                      |
| user_id     | integer   | foreign key to User(id), not null | Foreign key to the `user` table                           |
| feed_id     | integer   | foreign key to Feed(id), not null | Foreign key to the `feed` table                           |
| is_active   | boolean   | default true                      | Flag indicating whether the subscription is active or not |

**Feed**

Table name: `feed`

| Column Name       | Data Type | Constraints  | Description                                              |
|-------------------|-----------|--------------|----------------------------------------------------------|
| id                | integer   | primary key  | Unique identifier for a feed                             |
| title             | string    | not null     | Title of the feed                                        |
| url               | string    | not null     | URL of the feed                                          |
| description       | string    | not null     | Description of the feed                                  |
| last_built_at     | datetime  | default null | Timestamp of the last time the feed was built            |
| is_update_enabled | boolean   | default true | Flag indicating whether updates are enabled for the feed |
| created_at        | datetime  | not null     | Timestamp of when the feed was created                   |

**Item**

Table name: `item`

| Column Name  | Data Type | Constraints                       | Description                              |
|--------------|-----------|-----------------------------------|------------------------------------------|
| id           | integer   | primary key                       | Unique identifier for an item            |
| feed_id      | integer   | foreign key to Feed(id), not null | Foreign key to the `feed` table          |
| title        | string    | not null                          | Title of the item                        |
| url          | string    | not null                          | URL of the item                          |
| guid         | string    | not null                          | Globally unique identifier of the item   |
| description  | string    | default null                      | Description of the item                  |
| published_at | datetime  | not null                          | Timestamp of when the item was published |

**ReadStatus**

Table name: `read_status`

| Column Name | Data Type | Constraints                       | Description                                           |
|-------------|-----------|-----------------------------------|-------------------------------------------------------|
| id          | integer   | primary key                       | Unique identifier for a read status                   |
| user_id     | integer   | foreign key to User(id), not null | Foreign key to the `user` table                       |
| item_id     | integer   | foreign key to Item(id), not null | Foreign key to the `item` table                       |
| is_read     | boolean   | default false                     | Flag indicating whether the item has been read or not |

This schema includes the following:

- **User**: table to store user information, including email, full_name and password.
- **Subscription**: table to store user-subscribed feeds, including the feed id, user id, and an indicator whether the subscription is active or not.
- **Feed**: table to store feed information, including title, url, description, last built date, whether updates are enabled, and created date.
- **Item**: table to store items, including the item id, feed id, title, url, guid, description, and publish date.
- **ReadStatus**: table to store read status of items, including user id, item id, and a flag indicating whether the item has been read or not.


