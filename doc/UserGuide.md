# User Guide

## Endpoints

EMA runs in http://127.0.0.1:8000

Endpoint documentation can be checked in
http://127.0.0.1:8000/doc

# User Authentication

The provided endpoints need user credentials and basic HTTP authentication.

There are 2 types of user: Admin user, Regular user, Anonymous user.

The following sections shows what are each user able to do.
Please refer to the documentation in http://127.0.0.1:8000/doc for further details

## Anonymous User

This User does not need authentication.  
**NOTE**: Anything which the Anonymous user can do, so do Regular and Admin users.

**Endpoint**|**Use Case** 
-------|----------------
`GET doc/` | Read Endpoint documentation.
`GET api/user/register/`|  Create new Regular user.

## Regular User

This user needs authentication.
**NOTE**: Anything which the Anonymous User can do, so does Admin user.

**Endpoint**|**Use Case** 
-------|----------------
`GET api/user/` | Retrieves user's details: username, email, event user had signed up to..
`GET api/events/`| Lists all events available.
`GET api/events/<event_id>/`| Retrieves event details from given `event_id`: name, date, location...
`PUT api/user/signup-event/<event_id>/`| Signs up the user to even from given `event_id`. Email is used for signup and can signup up once for each event.
`DELETE api/user/signup-event/<event_id>/`| Cancels the user signup for this event.

## Admin User

This user needs authentication.

**Endpoint**|**Use Case** 
-------|----------------
`POST api/events/`| Creates a new event.
`PUT api/events/<event_id>/`| Updates details for a event with given `event_id`. Signups are not touched.
`DELETE api/events/<event_id>/`| Removes the event with given `event_id`. All the event's sign ups are removed altogether.
`GET api/events/<event_id>/signups/`| Lists all sign ups for the event with `event_id`
`POST api/events/<event_id>/signups/`| Signs up email for the event with `event_id`. Email has to be from a register user: Regular or Admin
`GET api/events/<event_id>/signups/<signup_id>/`| Retrieves the details for a signup with given `event_id` and `signup_id`
`PUT api/events/<event_id>/signups/<signup_id>/`| Updates the details for a signup with given `event_id` and `signup_id`
`DELETE api/events/<event_id>/signups/<signup_id>/`| Removes the signup from event with given `event_id` and `signup_id`







