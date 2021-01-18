# lolbot's database

lolbot uses [RethinkDB](https://rethinkdb.com) to store needed data.

## Tables

There is currently two tables:

- `config`
    - Used to store configuration for servers, and users
- `errors`
    - Used to store information in case of an error.

## Document format

`config`:
```js
{
    "id": int, // Representing the "Snowflake" IDs that Discord uses.
    "config": [
        {
            "property": string,
            "value": any // This can be a bool, int, string, whatever needs to be stored here
        },
        // ... this will go on for however many things are stored
    ]
}
```

`errors`:
```js
{
    "exception": string, // logging as a string is the easiest thing to do here
    "info": {
        "id": int // user's discord ID
        "command": string // name of command that user was doing
    }
}
```