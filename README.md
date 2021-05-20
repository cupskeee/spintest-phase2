## Getting Started

This is a project for a test/assessment.

I am using Python 3.9.0 for the programming language and also the python library RQ for queueing jobs and processing them and backed by Redis.

### Prerequisites
- Python 3 (preferably `Python 3.9.0`)
- Redis (you can find how to setup on [Redis Quickstart](https://redis.io/topics/quickstart)
- MongoDB
- Unix OS

NP: For the sake of developing time for this project, I picked RQ for a simple approach on queueing tasks on flask. But, with a downside that it needed to be run on Unix-based OS

### Setup

1. Clone the repository
`git clone https://github.com/cupskeee/python-near-location.git`

2. Install the necessary packages by running `pip install -r requirements.txt`

3. Run a Redis service.
(for me by executing `redis-server`)

4. Run the RQ service by executing `rq worker spintest2` (the rq package is included in the `requirements.txt`)

5. Run the project with `python run.py`

### Postman Collection
I also provided the postman collection that you can import to your own postman in the project folder called `SPIN Test2.postman_collection.json`
