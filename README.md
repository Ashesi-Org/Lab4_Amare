# WEB TECH LAB 4 : BUILD AND RUN A REST API

## VOTER ROUTES

### Registering a voter

**Request**

> POST /voters/

```js
// structure
{
  "id": string,
  "firstName": string,
  "lastName": string,
  "email": string,
  "yearGroup": string,
  "major": string,
  "hasVoted": false
}

// example
{
  "id": "100",
  "firstName": "ama",
  "lastName": "alhaji",
  "email": "ama.alhaji@ashesi.edu.gh",
  "yearGroup": "2000",
  "major": "MIS",
  "hasVoted": false
}
```

**Response**

201 (OK)

```js

{
    "message": "voter successfully registered",
    "ok": true
}

// sample unsuccessful operaton
{
    "message": "voter not found",
    "ok": false
}
```

### De-registering a voter

**Request**

> DELETE /voters/:id

**Response**
200 (OK)

```js
{
    "message": "voter successfully de-registered",
    "ok": true
}
```

### Retrieving a voter

**Request**

> GET /voters/:id

**Response**
200 (OK)

```js
{
    "message": "voter successfully de-registered",
    "ok": true
}
```

### Updating a voter

**Request**

> PATCH /voters/:id

**Response**
200 (OK)

```js
// sample successful operation
{
    "message": "voter successfully updated",
    "ok": true
}
```

## ELECTION ROUTES

### Creating an election

**Request**

> POST /elections/

```js
{
    "electionId":"EID_SPRING_2024",
    "ballot": [
        {
            "candidateId": "222",
            "candidateName": "Elon Musk",
            "voteCount": 0
        },
         {
            "candidateId": "333",
            "candidateName": "Amon Kali",
            "voteCount": 0
        }
    ]
}
```

**Response**

201 (OK)

```js

// sample output
{
    "id": "EID_SPRING_2024",
    "message": "election successfully created",
    "ok": true
}

```

### Retrieving an election and its details

**Request**

> GET elections/:id/ -> elections/EID_SPRING_2024/

**Response**

200 (OK)

```js

{
    "ballot": [
        {
            "candidateId": "222",
            "candidateName": "Elon Musk",
            "voteCount": 2
        },
        {
            "candidateId": "333",
            "candidateName": "Amon Kali",
            "voteCount": 0
        }
    ],
    "electionId": "EID_SPRING_2024"
}
```

### Deleting an election

**Request**

> DELETE /elections/:id/ -> /elections/EID_SPRING_2024/

**Response**

200 (OK)

```js
{
    "id": "EID_SPRING_2024",
    "message": "election successfully deleted",
    "ok": true
}
```

## VOTING ROUTES

### Casting a vote

**Request**

> POST /vote/

```js
{
    "voterId": "100",
    "electionId": "EID_SPRING_2024",
    "candidateId": "222"
}
```

**Response**

201 (OK)

```js
{
    "id": "100",
    "message": "vote successfully cast",
    "ok": true
}
```
