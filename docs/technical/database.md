# lolbot's database

lolbot uses [RethinkDB](https://rethinkdb.com) to store needed data.

## Tables

There is currently only one table:

- `config`
    - Used to store configuration for servers, and users

## Document format

`config` (formatted):
```js
{
    id: int,
    config: [
        {
            "property": string,
            "value": any // This can be a bool, int, string, whatever needs to be stored here
        },
        ...
    ]
}
```