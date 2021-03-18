# ALPHA project

```
docker-compose -f docker-compose.yml up -d
```



# WEBSOCKETS

```
URL: wss://localhost:5000/{token}
```

## 1.1 Structure of the commands

```
{
    "cmd": "type",
    "args": {
        "user_id": "123456789"
    }
}
```

# Types of commands

* NEW_MASSAGE

```
{
    "message_id": str("123456789")
}
```