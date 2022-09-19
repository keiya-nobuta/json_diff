# json_diff
experimental json tools

# installation

```
$ git clone https://github.com/keiya-nobuta/json_diff.git
$ pip install ./json_diff
```

# usage

show diff:
```
$ json_diff <json file a> <json file b>
```

example:
```
$ cat a.json
{
    "__id": "123456",
    "__rev": "1",
    "refs": [
        {"github.com": "https://github.com/keiya-nobuta"}
    ]
}
$ cat b.json
{
    "__id": "123456",
    "__rev": "2",
    "refs": [
        {"github.com": "https://github.com/keiya-nobuta"},
	{"example.com": "http://example.com"}
    ]
}
$ json_diff a.json b.json --indent=2
{
  "'__rev'": {
    "-": "1",
    "+": "2"
  },
  "'refs':1": {
    "+": {
      "example.com": "http://example.com"
    }
  }
}
$ json_diff b.json a.json --indent=2
{
  "'__rev'": {
    "-": "2",
    "+": "1"
  },
  "'refs':1": {
    "-": {
      "example.com": "http://example.com"
    }
  }
}
```
